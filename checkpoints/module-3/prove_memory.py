"""Prove your Scribe server remembers across a restart.

It tells the server one note, stops the server, starts it again,
and asks what it remembers. Nothing in your Drive changes.

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    python3 prove_memory.py
"""
import asyncio
import os
import sys
import textwrap

import mcp
from mcp.client.stdio import StdioServerParameters

SERVER = os.environ.get("SCRIBE_SERVER", "scribe_server.py")
NOTE = "Keep my openings under 12 words."


def said(result) -> str:
    return result.content[0].text if result.content else ""


def tell(text: str) -> None:
    for line in text.splitlines():
        for part in textwrap.wrap(line, 58) or [""]:
            print("   | " + part)


def start():
    params = StdioServerParameters(
        command=sys.executable, args=[SERVER],
        env=dict(os.environ))
    return mcp.Client(params)


async def main() -> int:
    if not os.environ.get("SCRIBE_FOLDER_ID"):
        sys.exit("SCRIBE_FOLDER_ID is not set. See the top of this"
                 " file.")
    os.environ.setdefault("SCRIBE_KEY", "key.json")
    if not os.path.exists(SERVER):
        sys.exit(f"Cannot find {SERVER}. Run this from your scribe"
                 " folder.")
    log = open("server.log", "w")
    os.dup2(log.fileno(), 2)
    checks = {}
    print("1. TELL IT ONE THING")
    async with start() as c:
        r = await c.call_tool("remember", {"note": NOTE})
        print("   server said:")
        tell(said(r))
        checks["it took the note"] = "Remembered" in said(r)

    print("\n2. STOP THE SERVER. START IT AGAIN.")
    async with start() as c:
        r = await c.call_tool("recall", {})
        print("   server said:")
        tell(said(r))
        checks["the note survived the restart"] = NOTE in said(r)

    print("\n3. LOOK AT THE FILE IT KEPT")
    memory = os.environ.get("SCRIBE_MEMORY", "memory.json")
    if os.path.exists(memory):
        with open(memory) as f:
            tell(f.read())
        checks["memory is a plain file you can read"] = True
    else:
        print(f"   {memory} is missing")
        checks["memory is a plain file you can read"] = False

    print("\n4. VERDICT")
    for name, ok in checks.items():
        print(f"   {'PASS' if ok else 'FAIL'}  {name}")
    good = all(checks.values())
    print("\nRESULT:", "Scribe remembers." if good
          else "something failed. Read the FAIL lines above,"
          " and server.log.")
    return 0 if good else 1


sys.exit(asyncio.run(main()))
