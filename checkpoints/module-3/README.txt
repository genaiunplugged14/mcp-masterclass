MCP MASTERCLASS: MODULE 3 CHECKPOINT
====================================

Grab this before lesson 16. One bad afternoon should never end a course.

This is the START of module 3. scribe_server.py in here is the finished
module 2 server, exactly as lesson 14 left it: 2 tools, 2 resources and
1 prompt. If yours works, keep yours. If it does not, use this one.

WHAT IS IN HERE
---------------
scribe_server.py          Scribe as module 2 left it. Module 3 changes it.
break_it.py               Attacks your server 3 ways. Lesson 18. It always
                          answers no to the server's question, so nothing
                          in your Drive changes. Safe to run again and again.
prove_memory.py           Proves the server remembers across a restart.
                          Lesson 20. Nothing in your Drive changes.
claude_desktop_config.json  The settings entry for Scribe, unchanged from
                          module 2.
requirements.txt          Pinned package versions.

WHAT YOU STILL HAVE TO SUPPLY
-----------------------------
key.json                  Your own service account key from lesson 4. It is a
                          password, so it is not in here and never will be.
your folder id            The last part of the web address of your Drafts
                          folder in Drive.
draft.md                  The draft from lesson 4, in your Drafts folder.

START HERE
----------
Copy the 2 scripts into your scribe folder, next to scribe_server.py.
Then tell them where your folder and your key are.

Mac and Linux:
    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    python3 break_it.py
    python3 prove_memory.py

Windows, in PowerShell:
    $env:SCRIBE_FOLDER_ID="paste your folder id here"
    $env:SCRIBE_KEY="key.json"
    python break_it.py
    python prove_memory.py

On Windows the command is usually python rather than python3.

WHERE THE MEMORY LIVES
----------------------
Lesson 20 gives Scribe a memory. It is one file called memory.json, next to
scribe_server.py. Open it in any text editor. Delete a line to make Scribe
forget it. Delete the file to start again.

If you want the file somewhere else, set SCRIBE_MEMORY to a path before you
start the server.

THE QUESTION, TWO WAYS
----------------------
From lesson 17, Scribe asks you before every write. There are two kinds
of app:

- An app that can show a question (Claude Code today) shows a small form:
  tick Yes, then Accept. Or Decline.
- An app that cannot (Claude Desktop, as of 2026-09-30) gets the question
  back as a sentence. Claude reads it and asks you in the chat. Say yes,
  and Claude calls Scribe again with said_yes set to true. Say no, and
  nothing is written.

Either way the first call never writes. If you want a draft edited with
no question at all, tell Scribe to trust it (lesson 20).

WHAT YOU SHOULD SEE
-------------------
break_it.py ends on:      RESULT: your guard holds.
prove_memory.py ends on:  RESULT: Scribe remembers.

If either one fails, read the FAIL lines, then server.log in the same
folder, which holds the server's own messages.
