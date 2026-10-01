"""Scribe v2. Claude can read and change your drafts, browse the
whole folder, and run a job you saved.

v1 gave Claude 2 tools. v2 adds 2 resources and 1 prompt. Nothing
from v1 was changed to make room for them.

Run it yourself:
    export SCRIBE_FOLDER_ID=your-folder-id
    export SCRIBE_KEY=key.json
    python3 scribe_server.py
"""
import io
import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

FOLDER = os.environ["SCRIBE_FOLDER_ID"]
KEY = os.environ.get("SCRIBE_KEY", "key.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=SCOPES)
drive = build("drive", "v3", credentials=creds,
              cache_discovery=False)

mcp = MCPServer("scribe")


def _find(name: str) -> str:
    q = (f"name = '{name}' and '{FOLDER}' in parents"
         " and trashed = false")
    found = drive.files().list(q=q, fields="files(id)").execute()
    if not found["files"]:
        raise ToolError(
            f"There is no draft called {name} in your folder.")
    return found["files"][0]["id"]


def _text(file_id: str) -> str:
    raw = drive.files().get_media(fileId=file_id).execute()
    return raw.decode()


@mcp.tool()
def read_doc(name: str) -> str:
    """Read one draft from the Scribe folder in Google Drive."""
    return _text(_find(name))


@mcp.tool()
def edit_doc(name: str, find: str, replace: str) -> str:
    """Replace some text inside one draft in the Scribe folder."""
    file_id = _find(name)
    text = _text(file_id)
    if find not in text:
        return f"That text is not in {name}. Nothing changed."
    new = text.replace(find, replace).encode()
    body = MediaIoBaseUpload(io.BytesIO(new),
                             mimetype="text/markdown")
    drive.files().update(fileId=file_id,
                         media_body=body).execute()
    return f"Changed {text.count(find)} spot(s) in {name}."


@mcp.resource("drafts://folder")
def folder() -> str:
    """The name of every draft in the Scribe folder."""
    q = (f"'{FOLDER}' in parents and trashed = false"
         " and mimeType contains 'text/'")
    found = drive.files().list(q=q, fields="files(name)",
                               orderBy="name").execute()
    return "\n".join(f["name"] for f in found["files"])


@mcp.resource("drafts://{name}")
def draft(name: str) -> str:
    """One draft from the Scribe folder, by its name."""
    return _text(_find(name))


@mcp.prompt()
def tidy_draft(name: str) -> str:
    """Fix the spelling and tighten the opening of one draft."""
    return (f"Read the draft called {name}. Fix every spelling"
            " mistake. Make the opening line shorter and"
            " stronger. Keep my voice, and change nothing else."
            " Use edit_doc for each change.")


if __name__ == "__main__":
    mcp.run()
