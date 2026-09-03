# MCP Masterclass

Working code for the **MCP Masterclass**, a free course on building Model Context Protocol servers.
Read the lessons at [genaiunplugged.substack.com](https://genaiunplugged.substack.com/p/what-is-mcp-model-context-protocol).

---

> ### If you cloned this before September 2026, the code has changed
>
> The MCP Python SDK went to version 2 and renamed the server class. Every file here was written
> against version 1 and stopped importing. It is fixed, and everything now runs on **mcp 2.1.1**.
>
> **[Read MIGRATION.md](MIGRATION.md)** for what changed and the one-line update.

---

## What this repo holds

Every file was run before it was pushed. Every tool was called and its output checked.

| Folder | Server | Tools | Status |
|---|---|---|---|
| [`lesson-05/`](lesson-05) | **Desk**, the course artifact | `read_note` | runs on mcp 2.1.1 |
| [`lesson-06/`](lesson-06) | Collaboration hub | `save_research`, `read_research`, `save_draft` | runs on mcp 2.1.1 |
| [`lesson-07/`](lesson-07) | Shared memory | `save_memory`, `read_memory`, `search_memory` | runs on mcp 2.1.1 |
| [`lesson-08/`](lesson-08) | Keeping score | `record_experience`, `get_learning_insights` | runs on mcp 2.1.1 |

Folder names are kept as they are so that links in the published lessons keep working.

## The course

The course is being rebuilt around **one artifact instead of four separate servers**. You build a
single thing called Desk and every lesson is a new version of it, so the course reads as one build
rather than a pile of toy projects.

| # | Lesson | |
|---|---|---|
| 1 | What is MCP, and why it had to exist | [read](https://genaiunplugged.substack.com/p/what-is-mcp-model-context-protocol) |
| 2 | Build your first MCP server | [read](https://genaiunplugged.substack.com/p/how-to-build-an-mcp-server-and-connect) |
| 3 | Tools, Resources and Prompts | [read](https://genaiunplugged.substack.com/p/the-three-superpowers-of-mcp-tools) |
| 4 | Give the desk a pen: write tools, and the risk they bring | in progress |
| 5 | The quiet mistake, and how to make a server ask first | in progress |
| 6 | Give the desk a memory | [read](https://genaiunplugged.substack.com/p/give-your-ai-agents-memory-mcp-shared) |
| 7 | Take the desk off your laptop | in progress |
| 8 | Publish it, and what to build next | in progress |

Two earlier lessons, on multi-agent collaboration and on learning from experience, are becoming
standalone articles instead. Their code is in `lesson-06` and `lesson-08` and it works.

## Getting started

**You need:** Python 3.10 or newer, and [Claude Desktop](https://claude.ai/download). A free Claude
account is enough.

```bash
git clone https://github.com/genaiunplugged14/mcp-masterclass.git
cd mcp-masterclass/lesson-05

uv venv && source .venv/bin/activate     # or: python3 -m venv .venv && source .venv/bin/activate
uv pip install -r requirements.txt       # or: pip install -r requirements.txt

python check_setup.py
```

`check_setup.py` tells you whether your Python, your SDK and your notes folder are ready. Fix
anything it marks FAIL, then run it again.

### Point Claude Desktop at it

Settings, then Developer, then Edit Config:

```json
{
  "mcpServers": {
    "desk": {
      "command": "/ABSOLUTE/PATH/TO/python",
      "args": ["/ABSOLUTE/PATH/TO/mcp-masterclass/lesson-05/server.py"]
    }
  }
}
```

Both paths must be **absolute**. This is the single most common reason a server does not appear.
Run `which python` inside your activated environment to find the first one. Then quit Claude Desktop
completely, which means the whole app and not just the window, and reopen it.

Faster alternative, which writes that config for you:

```bash
uv run mcp install server.py
```

### Test without Claude Desktop

```bash
uv run mcp dev server.py
```

That opens the MCP Inspector in your browser and talks to your server directly. If your server works
here but not in Claude Desktop, the problem is your config rather than your code.

## A habit worth stealing

Every `requirements.txt` here used to say `mcp>=1.0.0`. That is a floor, and a floor lets every
future major version through. When version 2 arrived, a fresh install started pulling code these
lessons could not run against, and the install still reported success.

They now pin a range:

```
mcp[cli]>=2.1,<3
```

Pin the range you actually tested. It matters most in anything you hand to somebody else.

## Questions and fixes

Open an issue if something does not work. Pull requests are welcome, especially if you spot code
that has drifted out of date again.

## License

See [LICENSE](LICENSE). Use this code for your own projects freely.
