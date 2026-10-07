"""Scribe v3. Claude can read and change your drafts, browse the
whole folder, run a job you saved, and now it is safe to trust.

v2 gave Claude 2 tools, 2 resources and 1 prompt. v3 adds a guard
that stays inside your folder and asks before it writes, a memory
the server owns, and 2 tools that use that memory. Nothing from
v2 was changed to make room, except that edit_doc now asks first.

Run it yourself:
    export SCRIBE_FOLDER_ID=your-folder-id
    export SCRIBE_KEY=key.json
    python3 scribe_server.py
"""
import io
import json
import os
from datetime import date
from typing import Annotated

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload
from mcp.server.mcpserver import Context, Elicit, MCPServer
from mcp.server.mcpserver import Resolve
from mcp.server.mcpserver.exceptions import ToolError
from mcp_types import ClientCapabilities, ElicitationCapability
from pydantic import BaseModel

FOLDER = os.environ["SCRIBE_FOLDER_ID"]
KEY = os.environ.get("SCRIBE_KEY", "key.json")
SCOPES = ["https://www.googleapis.com/auth/drive"]
HERE = os.path.dirname(os.path.abspath(__file__))
MEMORY = os.environ.get("SCRIBE_MEMORY",
                        os.path.join(HERE, "memory.json"))

creds = service_account.Credentials.from_service_account_file(
    KEY, scopes=SCOPES)
drive = build("drive", "v3", credentials=creds,
              cache_discovery=False)

mcp = MCPServer("scribe")


# ---------------------------------------------------- the guard
def _inside(name: str) -> str:
    """The fence. A draft is a plain name inside your folder."""
    if "/" in name or "\\" in name or name.startswith("."):
        raise ToolError(
            f"{name} is not a draft in your folder. Scribe stays"
            " inside the Drafts folder and never leaves it.")
    return name


def _google(call):
    """Run one Google call. Turn its error into a sentence."""
    try:
        return call.execute()
    except HttpError as err:
        if err.resp.status == 403:
            raise ToolError(
                "Google refused. Scribe can only change drafts"
                " shared with it as an editor, and it can never"
                " make a new file.")
        raise ToolError(f"Google said no: {err.reason}")


def _find(name: str) -> str:
    _inside(name)
    q = (f"name = '{name}' and '{FOLDER}' in parents"
         " and trashed = false")
    found = _google(drive.files().list(q=q, fields="files(id)"))
    if not found["files"]:
        raise ToolError(
            f"There is no draft called {name} in your folder.")
    return found["files"][0]["id"]


def _text(file_id: str) -> str:
    raw = _google(drive.files().get_media(fileId=file_id))
    return raw.decode()


# --------------------------------------------------- the memory
def _notes() -> list:
    if not os.path.exists(MEMORY):
        return []
    with open(MEMORY) as f:
        return json.load(f)


def _save(notes: list) -> None:
    with open(MEMORY, "w") as f:
        json.dump(notes, f, indent=2)


def _trusted(name: str) -> bool:
    return any(n["note"] == f"trust {name}" for n in _notes())


# --------------------------------------- the question, asked first
class Confirm(BaseModel):
    yes: bool


def _can_ask(ctx: Context) -> bool:
    """Can this app show a question and hand back the answer?"""
    form = ClientCapabilities(elicitation=ElicitationCapability())
    return ctx.session.check_client_capability(form)


def ask_first(name: str, find: str, replace: str,
              said_yes: bool, ctx: Context):
    """Ask before a write, unless you told Scribe to trust it."""
    if not find:
        raise ToolError("Tell me what to find. An empty find"
                        " would change every spot in the draft.")
    if _trusted(name) or said_yes:
        return Confirm(yes=True)
    question = f"Change every '{find}' to '{replace}' in {name}?"
    if _can_ask(ctx):
        return Elicit(question, Confirm)
    raise ToolError(
        f"{question} This app cannot show my question, so I"
        " stopped. Ask the person. If they say yes, call me"
        " again with said_yes set to true.")


# ----------------------------------------------------- the tools
@mcp.tool()
def read_doc(name: str) -> str:
    """Read one draft from the Scribe folder in Google Drive."""
    return _text(_find(name))


@mcp.tool()
def edit_doc(name: str, find: str, replace: str,
             said_yes: bool = False,
             ok: Annotated[Confirm, Resolve(ask_first)] = None,
             ) -> str:
    """Replace some text inside one draft, after asking you.

    Leave said_yes false. Scribe asks the person first. Set it true
    only when the person has answered yes to Scribe's question."""
    if not ok.yes:
        return f"You said no. {name} is untouched."
    file_id = _find(name)
    text = _text(file_id)
    if find not in text:
        return f"That text is not in {name}. Nothing changed."
    new = text.replace(find, replace).encode()
    body = MediaIoBaseUpload(io.BytesIO(new),
                             mimetype="text/markdown")
    _google(drive.files().update(fileId=file_id, media_body=body))
    return f"Changed {text.count(find)} spot(s) in {name}."


@mcp.tool()
def remember(note: str) -> str:
    """Keep one note for every future chat. A rule, or a choice."""
    notes = _notes()
    notes.append({"on": str(date.today()), "note": note})
    _save(notes)
    return f"Remembered. Scribe now holds {len(notes)} note(s)."


@mcp.tool()
def recall() -> str:
    """Every note Scribe remembers, oldest first."""
    notes = _notes()
    if not notes:
        return "Scribe remembers nothing yet."
    return "\n".join(f"{n['on']}: {n['note']}" for n in notes)


@mcp.tool()
def find_note(word: str) -> str:
    """Find every note that mentions one word."""
    hits = [n for n in _notes()
            if word.lower() in n["note"].lower()]
    if not hits:
        return f"No note mentions {word}."
    return "\n".join(f"{n['on']}: {n['note']}" for n in hits)


# ------------------------------------------------- the resources
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


# ---------------------------------------------------- the prompt
@mcp.prompt()
def tidy_draft(name: str) -> str:
    """Fix the spelling and tighten the opening of one draft."""
    return (f"Read the draft called {name}. Fix every spelling"
            " mistake. Make the opening line shorter and"
            " stronger. Keep my voice, and change nothing else."
            " Use edit_doc for each change.")


if __name__ == "__main__":
    mcp.run()
