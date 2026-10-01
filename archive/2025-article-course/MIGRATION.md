# The SDK changed, and this repo has caught up

**Read this if you started the course before September 2026.**

## What happened

The MCP Python SDK went to version 2. The high-level server class was **renamed**, and the old import
path was removed rather than deprecated:

```python
from mcp.server.fastmcp import FastMCP   # version 1. Gone.
from mcp.server import MCPServer         # version 2. Current.
```

The low-level `Server` class that the original lesson code used was rebuilt with a different
signature, so `@server.list_tools()` and `@server.call_tool()` no longer exist in that form.

Every `server.py` in this repo was written against version 1. As of the version 2 release they all
failed on import, and `lesson-05/server.py` had a second, unrelated problem: markdown from the README
had been pasted into it, so it was not valid Python at all.

That is fixed. Every file here now runs on **mcp 2.1.1**, and every tool was called and checked before
this was pushed.

## What you need to do

Update the SDK and re-pull:

```bash
git pull
cd lesson-05
uv add "mcp[cli]>=2.1,<3"     # or: pip install "mcp[cli]>=2.1,<3"
python check_setup.py
```

Your Claude Desktop config does not change. The file paths are the same.

## What the code looks like now

The whole of lesson 5 used to be 165 lines. Here it is:

```python
"""Desk: an MCP server that lets Claude read your notes."""
from pathlib import Path
from mcp.server import MCPServer

NOTES = Path(__file__).parent / "notes"
mcp = MCPServer("desk")


@mcp.tool()
def read_note(name: str) -> str:
    """Read one note from the notes folder. Give the file name, like ideas.txt."""
    note = NOTES / name
    if not note.exists():
        return f"There is no note called {name}."
    return note.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

There is no hand-written JSON schema any more. `name: str` **is** the schema, and the docstring is
the description Claude reads. That is the whole difference between 165 lines and 14.

## The habit that would have caught this

Every `requirements.txt` here used to say:

```
mcp>=1.0.0
```

That is a floor, and a floor lets every future major version through. When version 2 shipped, a fresh
`pip install -r requirements.txt` started pulling code that these lessons cannot run against, and the
install still succeeded, which is what made it confusing.

They now say:

```
mcp[cli]>=2.1,<3
```

Pin the range you tested. This applies to anything you hand to somebody else.

## Other things that moved

Worth knowing if you read the spec or older tutorials.

- **HTTP+SSE transport is deprecated.** Use stdio locally and Streamable HTTP on a server.
- **Sampling, Roots and Logging are deprecated** as of protocol revision 2026-07-28. Do not build on
  them. Pass paths as tool arguments, call your LLM provider directly, and log to stderr.
- **The protocol is stateless now.** There is no `initialize` handshake and no session. The SDK hides
  this, so your tool code does not change.
- **Asking the user a question mid-tool-call** is new and supported. Look up `Resolve` and `Elicit`.
