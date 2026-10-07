MCP MASTERCLASS: MODULE 4 CHECKPOINT
====================================

Grab this before lesson 24. One bad afternoon should never end a course.

This is the START of module 4. scribe_server.py in here is the finished
module 3 server, exactly as lesson 22 left it: 5 tools, 2 resources and
1 prompt, with the guard, the question before every write, and the
memory working. If yours works, keep yours. If it does not, use this one.

WHAT IS IN HERE
---------------
scribe_server.py          Scribe as module 3 left it. Module 4 adds to it.
requirements.txt          Pinned package versions, now 4 lines. The fourth
                          one, requests, is what lesson 25 adds. Render
                          reads this file in lesson 28.
prove_substack.py         Proves the public read needs no login, makes a
                          Substack draft from draft.md, checks with Substack
                          that it is only a draft, and deletes it again.
                          Lesson 26. Nothing is published, nobody is
                          emailed. Safe to run again and again.
break_it.py               The 3 attacks from lesson 18. Run it after every
                          change you make to the server, including the
                          ones in this module.
claude_desktop_config.json  The settings entry for Scribe, with the 2 new
                          lines from lesson 25 (your Substack name and
                          your cookie).
.gitignore                The 3 lines lesson 28 needs before the code goes
                          on GitHub. It is a hidden file, so your file
                          browser may not show it. It is there.
REGISTRY-NOTES.txt        The MCP Registry pointer from lesson 28: the
                          server.json, the 4 commands, and the one rule.

WHAT YOU STILL HAVE TO SUPPLY
-----------------------------
key.json                  Your own service account key from lesson 4. It is a
                          password, so it is not in here and never will be.
your folder id            The last part of the web address of your Drafts
                          folder in Drive.
draft.md                  The draft from lesson 4, in your Drafts folder.
your Substack name        The part before .substack.com. Lesson 25.
your substack.sid cookie  From Chrome: DevTools, Application, Cookies,
                          https://substack.com, the row substack.sid. It is
                          a password. Lesson 25 says how to handle it.
a GitHub account          Lesson 28 only.
a Render account          Lesson 28 only. Free, no card.

The read half of module 4 needs none of the Substack lines. If you have
no Substack, build both tools anyway. The write tool tells you what it
needs, in a sentence, and waits.

START HERE
----------
Copy prove_substack.py and break_it.py into your scribe folder, next to
scribe_server.py. Then tell them where your folder, your key and your
Substack are.

Mac and Linux:
    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    export SCRIBE_SUBSTACK="your-publication-name"
    export SCRIBE_SUBSTACK_COOKIE="paste the substack.sid value here"
    python3 prove_substack.py
    python3 break_it.py

Windows, in PowerShell:
    $env:SCRIBE_FOLDER_ID="paste your folder id here"
    $env:SCRIBE_KEY="key.json"
    $env:SCRIBE_SUBSTACK="your-publication-name"
    $env:SCRIBE_SUBSTACK_COOKIE="paste the substack.sid value here"
    python prove_substack.py
    python break_it.py

On Windows the command is usually python rather than python3. Leave the
2 Substack lines out to run only the public read half.

THE NEW PACKAGE (lesson 25)
---------------------------
    uv add requests

Or with pip, inside your venv:
    pip install -r requirements.txt

THE WEB ADDRESS (lesson 27)
---------------------------
The same file serves the pipe (the default) or a web address:

Mac and Linux:
    export SCRIBE_TRANSPORT=http
    export PORT=8765
    python3 scribe_server.py

Windows, in PowerShell:
    $env:SCRIBE_TRANSPORT="http"
    $env:PORT="8765"
    python scribe_server.py

Open http://127.0.0.1:8765/ in a browser. You should see
"Scribe is up. Claude talks to /mcp". Claude Desktop cannot use this
address until the server is on the internet (lesson 28), because a
custom connector is reached from Anthropic's cloud, not from your
laptop.

PUTTING THE FOLDER ON GITHUB (lesson 28)
----------------------------------------
Make a new, empty repo on github.com first, then in your scribe folder:
    git init
    git add scribe_server.py requirements.txt .gitignore
    git commit -m "Scribe"
    git remote add origin https://github.com/YOUR-NAME/scribe.git
    git push -u origin main

Check the repo in the browser before you go to Render: key.json and
memory.json must NOT be in it. If they are, the .gitignore was missing.

RENDER, IN SHORT (lesson 28)
----------------------------
dashboard.render.com > New > Web Service > your GitHub repo.
    Name            scribe
    Language        Python
    Build command   pip install -r requirements.txt
    Start command   python scribe_server.py
    Instance type   Free
Environment variables:
    SCRIBE_FOLDER_ID         your folder id
    SCRIBE_SUBSTACK          your publication name
    SCRIBE_SUBSTACK_COOKIE   the substack.sid value
    SCRIBE_TRANSPORT         http
PORT is set by Render. Do not set it.
Secret Files: filename key.json, paste the whole key in. It lands next
to the server, so SCRIBE_KEY keeps its default.
Deploy. Wait for "Uvicorn running on http://0.0.0.0:10000" in the log.
Open https://scribe-SOMETHING.onrender.com/ in a browser: "Scribe is up".

Then in Claude: Customize > Connectors > + > Add custom connector,
URL https://scribe-SOMETHING.onrender.com/mcp > Add. In a chat, press +
and switch the connector on.

THREE THINGS ABOUT THE FREE HOST
--------------------------------
1. It sleeps after 15 minutes with no traffic and takes about a minute
   to wake. If Claude's first connect fails, open the address in a
   browser, wait for "Scribe is up", and try again.
2. The free host keeps no disk. memory.json is wiped on every sleep.
   remember and trust work until the next nap. On your laptop the memory
   is safe. Lesson 30 names the fix.
3. YOUR WEB ADDRESS IS THE PASSWORD. Scribe has no login of its own.
   Anyone with the address can read and edit your Drive folder, make
   drafts in your Substack, and read your memory. Never paste it
   anywhere public, and never list it in the registry (see
   REGISTRY-NOTES.txt). A real product puts OAuth in front of this.

Render's free plan: 750 instance hours a month, for hobby use. It is free
today. It is not "free forever", and it is not for something people pay
you for.

WHAT YOU SHOULD SEE
-------------------
prove_substack.py ends on:  RESULT: Scribe delivers.
break_it.py ends on:        RESULT: your guard holds.

If either one fails, read the FAIL lines, then server.log in the same
folder, which holds the server's own messages. If Substack says it did
not recognise the cookie, copy a fresh substack.sid from the browser. The
cookie lives about 30 days and changes when you change your password.
