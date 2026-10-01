"""Lesson 5: the obvious way. A script that reads a draft out of Google Drive.

It works. Run it and see. Then try to make Claude Desktop run it, and watch
where the obvious way stops.

    python3 draft.py
"""
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Paste your Drive folder id here. It is the last part of the folder's web address.
FOLDER = "paste your folder id here"

creds = service_account.Credentials.from_service_account_file(
    "key.json", scopes=["https://www.googleapis.com/auth/drive"])
drive = build("drive", "v3", credentials=creds)


def read_draft(name):
    # The folder matters. A search by name alone comes back empty for a file
    # your service account reaches through a shared folder.
    q = f"name = '{name}' and '{FOLDER}' in parents and trashed = false"
    hits = drive.files().list(q=q, fields="files(id)").execute()["files"]
    return drive.files().get_media(fileId=hits[0]["id"]).execute().decode()


print(read_draft("draft.md"))
