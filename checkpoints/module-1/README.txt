MCP MASTERCLASS: MODULE 1 CHECKPOINT
====================================

Grab this before you need it. One bad afternoon should never end a course.

WHAT IS IN HERE
---------------
verify_drive_access.py    Checks your Google setup. Run this first when
                          anything goes wrong. Give it your folder id too.
verify_claude_config.py   Checks whether Claude Desktop actually started the
                          servers you configured. Never prints your config,
                          because that file holds tokens in plain text.
draft.py                  The lesson 5 script. It reads a draft out of Drive.
draft.md                  A sample draft with a typo in it. Upload this to your
                          Drive folder.
claude_desktop_config.json  The lesson 6 settings, with both servers in it.
requirements.txt          Pinned package versions.

WHAT YOU STILL HAVE TO SUPPLY
-----------------------------
key.json                  Your own service account key from lesson 4. It is a
                          password, so it is not in here and never will be.
your folder id            Open your Drive folder and copy the last part of the
                          web address. Paste it into draft.py.

START HERE
----------
    pip install -r requirements.txt
    python3 verify_drive_access.py key.json

You want to see this at the bottom:

    RESULT: read yes. change yes. create no.

If you see that, your setup is correct and every lesson in module 1 will run.
If a read fails, you almost certainly missed the sharing step in lesson 4.
Sharing the folder with the service account email is what grants access. Roles
set in the Cloud console do not.

If draft.py finds nothing, check that you pasted your folder id into it. A
search by name alone comes back empty for a file reached through a shared
folder, even though the file is right there.

CONFIG NOTES
------------
In claude_desktop_config.json, replace /FULL/PATH/TO/scribe with the real path
to your own folder. It must be a full path from the top, and Claude Desktop has
to be fully quit and opened again after you edit it.
