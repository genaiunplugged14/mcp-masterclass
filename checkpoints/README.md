# Checkpoints

One checkpoint per module. Each one holds the files you need at the **start** of that module, so a
bad afternoon in the previous one never ends the course. Grab the checkpoint before the module
begins, not after something breaks. Each folder has its own `README.txt` with the exact commands
and what the result lines should say.

The same files ship as zips from the course site:

| Module | Grab it before | Folder | Zip |
|---|---|---|---|
| 1 | Lesson 1 | [`module-1/`](module-1) | [scribe-checkpoint-m1.zip](https://www.genaiunplugged.com/academy/mcp-masterclass/checkpoints/scribe-checkpoint-m1.zip) |
| 2 | Lesson 11 | [`module-2/`](module-2) | [scribe-checkpoint-m2.zip](https://www.genaiunplugged.com/academy/mcp-masterclass/checkpoints/scribe-checkpoint-m2.zip) |
| 3 | Lesson 16 | [`module-3/`](module-3) | [scribe-checkpoint-m3.zip](https://www.genaiunplugged.com/academy/mcp-masterclass/checkpoints/scribe-checkpoint-m3.zip) |
| 4 | Lesson 24 | ships with Module 4 | ships with Module 4 |

## What is in each one

**Module 1** (`module-1/`): the Google setup and the first script.

- `verify_drive_access.py` checks your Google setup. Run it first when anything goes wrong. It
  should end on `RESULT: read yes. change yes. create no.`
- `verify_claude_config.py` checks whether Claude Desktop actually started the servers you
  configured. It never prints your config, because that file holds tokens in plain text.
- `draft.py` is the lesson 5 script. It reads a draft out of Drive. Paste your folder id into it.
- `draft.md` is a sample draft with a typo in it. Upload it to your Drive folder.
- `claude_desktop_config.json` is the lesson 6 settings file with the filesystem and memory servers.

**Module 2** (`module-2/`): the test scripts for the server you write in lessons 12 to 14. The
server itself is not in here on purpose; you write it.

- `drafts/` holds 3 sample drafts, each with a weak opening and a few spelling mistakes. Upload all
  3 into your Drafts folder in Drive.
- `what_can_it_do.py` asks your server what it offers (lessons 12 and 14).
- `prove_it.py` proves your server changed a real document in Drive (lessons 13 and 14). It should
  end on `RESULT: your server works.` After lesson 12 one line says FAIL, and it is meant to.
- `claude_desktop_config.json` adds the `scribe` entry next to the two servers from lesson 6.
- `verify_drive_access.py` and `verify_claude_config.py` are the module 1 checks, carried forward.
- `official-drive-server.txt` is the setup for the official Google Drive server, for the curious.
  The course does not need it.

**Module 3** (`module-3/`): Scribe as module 2 left it, plus two attack and memory checks.

- `scribe_server.py` is the finished module 2 server: 2 tools, 2 resources, 1 prompt. If yours
  works, keep yours. If it does not, use this one.
- `break_it.py` attacks your server 3 ways (lesson 18). It always answers no to the server's
  question, so nothing in your Drive changes. It should end on `RESULT: your guard holds.`
- `prove_memory.py` proves the server remembers across a restart (lesson 20). It should end on
  `RESULT: Scribe remembers.`
- `claude_desktop_config.json` is unchanged from module 2.

**Module 4**: ships with Module 4, which is in production.

## What you still have to supply

Every checkpoint needs two things that are yours and are never in the repo:

- `key.json`, your Google service account key from lesson 4. It is a password.
- Your Drive folder id, the last part of the folder's web address. Module 1 pastes it into
  `draft.py`; modules 2 and 3 read it from `SCRIBE_FOLDER_ID`.

Every `claude_desktop_config.json` carries `/FULL/PATH/TO/scribe` as a placeholder. Replace it with
the real path to your own folder, a full path from the top, then quit Claude Desktop completely and
reopen it. On Windows the Python inside the folder is `C:\\FULL\\PATH\\TO\\scribe\\.venv\\Scripts\\python.exe`,
with the backslashes doubled, since that is how the file format writes a single backslash.

## Running the checks

```bash
export SCRIBE_FOLDER_ID="paste your folder id here"
export SCRIBE_KEY="key.json"

python3 verify_drive_access.py key.json     # module 1 onward
python3 prove_it.py                         # module 2
python3 break_it.py && python3 prove_memory.py   # module 3
```

With `uv`, replace `python3 script.py` with `uv run script.py`. On Windows the command is usually
`python` rather than `python3`.

Every `requirements.txt` pins `mcp>=2.1,<3`. A lower bound alone is not a pin; the first version
of this course said `mcp>=1.0.0`, which later resolved to 2.x and broke every sample it shipped
with.
