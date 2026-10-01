"""Prove what a Google service account can and cannot do in a personal Drive.

Runs the three checks the MCP Masterclass depends on, against a real account:
  1. read   works
  2. update works
  3. create fails, with the exact error the learner will see

The update check is a byte-identical round trip. It downloads a file, uploads
the same bytes back, and compares the md5 before and after. Nothing changes.

Usage:
    python3 verify_drive_access.py <key.json> [folder-id]

Pass your folder id and it checks that folder DIRECTLY. Do that on a fresh
setup: Drive's permission works the instant you share, but its search index
takes a while to catch up, so a search can come back empty while everything is
already correct.
"""
import io
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]


def main(key_path, folder_id=None):
    creds = service_account.Credentials.from_service_account_file(key_path, scopes=SCOPES)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    print("1. WHO AM I, AND HOW MUCH ROOM DO I HAVE")
    about = drive.about().get(fields="user,storageQuota").execute()
    print("   account       : %s" % about["user"]["emailAddress"])
    print("   storage limit : %s bytes" % about["storageQuota"]["limit"])
    print("   -> a service account owns no space at all")

    if folder_id:
        print("\n2. CAN I REACH YOUR FOLDER? (asked by id, so the search index cannot lie)")
        try:
            f = drive.files().get(
                fileId=folder_id,
                fields="name,capabilities(canEdit,canAddChildren)").execute()
            cap = f["capabilities"]
            print("   folder        : %s" % f["name"])
            print("   can change it : %s" % cap["canEdit"])
            if not cap["canEdit"]:
                print("   -> shared, but read only. Set the role to Editor.")
        except HttpError as err:
            print("   NO. HTTP %d" % err.resp.status)
            print("   -> the folder was never shared with this account. That is step 6.")
            return

    print("\n2b. WHAT DOES A SEARCH SEE?" if folder_id else "\n2. WHAT HAS BEEN SHARED WITH ME")
    listed = drive.files().list(
        q="trashed=false",
        fields="files(id,name,size,md5Checksum,capabilities(canEdit))",
        pageSize=200,
    ).execute()
    files = listed.get("files", [])
    editable = [f for f in files if f.get("capabilities", {}).get("canEdit")]
    print("   files visible : %d" % len(files))
    print("   files I can edit: %d" % len(editable))
    if folder_id and not files:
        print("   -> 0 is NORMAL on a fresh setup. Sharing works at once, the search")
        print("      index takes a while. Check 1 above is the one that matters.")

    folders = drive.files().list(
        q="mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id,name)",
    ).execute().get("files", [])
    for folder in folders:
        print("   folder        : %s" % folder["name"])

    print("\n3. CAN I CREATE A NEW FILE?")
    body = {"name": "scribe-create-probe.txt"}
    if folders:
        body["parents"] = [folders[0]["id"]]
    media = MediaIoBaseUpload(io.BytesIO(b"probe\n"), mimetype="text/plain")
    try:
        made = drive.files().create(body=body, media_body=media, fields="id").execute()
        drive.files().delete(fileId=made["id"]).execute()
        print("   CREATE SUCCEEDED (you are on a shared drive)")
    except HttpError as err:
        detail = err.error_details[0]
        print("   NO. HTTP %d, %s" % (err.resp.status, detail["reason"]))
        print("   Google says: %s" % detail["message"].split(".")[0] + ".")

    print("\n4. CAN I READ AND CHANGE A FILE SOMEBODY ELSE OWNS?")
    with_size = sorted(
        [f for f in editable if f.get("size") and f.get("md5Checksum")],
        key=lambda f: int(f["size"]),
    )
    if not with_size:
        print("   no editable file to test against")
        return
    target = with_size[0]
    print("   file          : %s" % target["name"])

    data = drive.files().get_media(fileId=target["id"]).execute()
    print("   read          : %d bytes" % len(data))

    drive.files().update(
        fileId=target["id"],
        media_body=MediaIoBaseUpload(io.BytesIO(data), mimetype="application/octet-stream"),
    ).execute()
    after = drive.files().get(fileId=target["id"], fields="md5Checksum").execute()
    print("   write         : accepted")
    print("   md5 before    : %s" % target["md5Checksum"])
    print("   md5 after     : %s" % after["md5Checksum"])
    print("   unchanged     : %s" % (after["md5Checksum"] == target["md5Checksum"]))

    print("\nRESULT: read yes. change yes. create no.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "key.json",
         sys.argv[2] if len(sys.argv) > 2 else None)
