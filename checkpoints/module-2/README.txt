MCP MASTERCLASS: MODULE 2 CHECKPOINT
====================================

Grab this before lesson 12. One bad afternoon should never end a course.

This is the START of module 2. You write scribe_server.py yourself in
lessons 12 to 14, so it is not in here. The finished server ships in the
module 3 checkpoint.

WHAT IS IN HERE
---------------
drafts/                   3 sample drafts, each with a weak opening and a
                          few spelling mistakes. Upload all 3 into your
                          Drafts folder in Google Drive.
what_can_it_do.py         Asks your server what it offers. Lessons 12 and 14.
prove_it.py               Proves your server changed a real document in
                          Drive. Lessons 13 and 14. Safe to run again and
                          again.
claude_desktop_config.json  The settings entry for Scribe, next to the 2
                          servers from lesson 6.
verify_drive_access.py    The setup check from module 1. Lesson 13 runs it
                          again to watch Google refuse a new file.
verify_claude_config.py   Checks whether Claude Desktop started your servers.
official-drive-server.txt The steps for the official Google Drive server,
                          for the curious. You do not need it for the course.
requirements.txt          Pinned package versions.

WHAT YOU STILL HAVE TO SUPPLY
-----------------------------
key.json                  Your own service account key from lesson 4. It is a
                          password, so it is not in here and never will be.
your folder id            The last part of the web address of your Drafts
                          folder in Drive.
draft.md                  The draft from lesson 4, with the typo in it. It
                          should already be in your Drafts folder.

START HERE
----------
Copy the 2 scripts into your scribe folder, next to scribe_server.py.
Then tell them where your folder and your key are.

Mac and Linux:

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"

Windows, in PowerShell:

    $env:SCRIBE_FOLDER_ID = "paste your folder id here"
    $env:SCRIBE_KEY = "key.json"

Then run them. With uv:

    uv run what_can_it_do.py
    uv run prove_it.py

With pip, inside your virtual environment:

    python3 what_can_it_do.py
    python3 prove_it.py

On Windows the command is usually python rather than python3.

You want to see this at the bottom of prove_it.py:

    RESULT: your server works.

After lesson 12, one line says FAIL, and it is meant to. Lesson 13 shows
you why, and you fix it there with 2 small changes.

THE SETTINGS FILE
-----------------
In claude_desktop_config.json, replace /FULL/PATH/TO/scribe with the real
path to your own folder. Every path must be a full path from the top. Quit
Claude Desktop fully and open it again after you edit the file.

On Windows, the Python inside your scribe folder lives here instead:

    C:\\FULL\\PATH\\TO\\scribe\\.venv\\Scripts\\python.exe

Backslashes are doubled inside that file. That is how the file format
writes a single backslash.

IF SOMETHING FAILS
------------------
prove_it.py cannot read draft.md
    Your folder id is wrong, or draft.md is not in the folder, or the
    folder was never shared with your service account. Run
    verify_drive_access.py with your key and your folder id.

Claude Desktop does not show scribe
    Run verify_claude_config.py. A short path in the settings file is the
    usual cause.

A sample from an older article fails on inputSchema
    The package today spells it input_schema. Check the date on the
    article before you check your own code.
