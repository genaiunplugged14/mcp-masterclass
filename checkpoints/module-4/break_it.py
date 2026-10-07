"""Try to break your own Scribe server, 3 ways. It should hold.

This starts scribe_server.py as its own program and talks to it
over the pipe, exactly the way Claude Desktop does. It answers the
server's question for you, and it always answers no, so nothing in
your Drive changes.

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    python3 break_it.py            # uses draft.md
    python3 break_it.py other.md   # or name another draft
"""
import asyncio
import io
import os
import sys
import textwrap

import mcp
import mcp_types as types
from mcp.client.stdio import StdioServerParameters

SERVER = os.environ.get("SCRIBE_SERVER", "scribe_server.py")
DOC = sys.argv[1] if len(sys.argv) > 1 else "draft.md"


def said(result) -> str:
    return result.content[0].text if result.content else ""


def tell(text: str) -> None:
    for line in textwrap.wrap(text, 58):
        print("   | " + line)


async def say_no(context, params):
    """The question Scribe asks. This script always says no."""
    print("   Scribe asked:")
    tell(params.message)
    print("   you said: no")
    return types.ElicitResult(action="accept",
                              content={"yes": False})


async def main() -> int:
    if not os.environ.get("SCRIBE_FOLDER_ID"):
        sys.exit("SCRIBE_FOLDER_ID is not set. See the top of this"
                 " file.")
    os.environ.setdefault("SCRIBE_KEY", "key.json")
    if not os.path.exists(SERVER):
        sys.exit(f"Cannot find {SERVER}. Run this from your scribe"
                 " folder.")
    params = StdioServerParameters(
        command=sys.executable, args=[SERVER],
        env=dict(os.environ))
    log = open("server.log", "w")
    os.dup2(log.fileno(), 2)
    checks = {}
    client = mcp.Client(params, elicitation_callback=say_no)
    async with client as c:
        print("1. ASK FOR A FILE OUTSIDE THE FOLDER")
        r = await c.call_tool("read_doc",
                              {"name": "../secrets.md"})
        print("   server said:")
        tell(said(r))
        checks["it stayed inside the folder"] = (
            r.is_error and "stays inside" in said(r))

        print("\n2. ASK IT TO FIND NOTHING, AND REPLACE IT")
        r = await c.call_tool("edit_doc", {
            "name": DOC, "find": "", "replace": "x"})
        print("   server said:")
        tell(said(r))
        checks["an empty find was refused"] = (
            r.is_error and "empty find" in said(r))

        print("\n3. ASK FOR A REAL CHANGE, AND SAY NO")
        before = said(await c.call_tool("read_doc", {"name": DOC}))
        r = await c.call_tool("edit_doc", {
            "name": DOC, "find": "the", "replace": "THE"})
        print("   server said:")
        tell(said(r))
        after = said(await c.call_tool("read_doc", {"name": DOC}))
        checks["it asked before writing"] = "untouched" in said(r)
        checks["no meant no"] = before == after

    print("\n4. VERDICT")
    for name, ok in checks.items():
        print(f"   {'PASS' if ok else 'FAIL'}  {name}")
    good = all(checks.values())
    print("\nRESULT:", "your guard holds." if good
          else "something failed. Read the FAIL lines above,"
          " and server.log.")
    return 0 if good else 1


sys.exit(asyncio.run(main()))
