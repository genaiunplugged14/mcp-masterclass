"""Prove your Scribe server changes a real document in Drive.

This starts scribe_server.py as its own program and talks to it
over the pipe, which is exactly what Claude Desktop does.

It is safe to run again and again. It puts the typo back before it
starts, so there is always something to fix.

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    python3 prove_it.py            # uses draft.md
    python3 prove_it.py other.md   # or name another draft

The draft needs the typo from lesson 4 in it, the words "Ths line".
"""
import asyncio
import os
import sys
import textwrap

import mcp
from mcp.client.stdio import StdioServerParameters

SERVER = os.environ.get("SCRIBE_SERVER", "scribe_server.py")
DOC = sys.argv[1] if len(sys.argv) > 1 else "draft.md"
WRONG, RIGHT = "Ths line", "This line"


def said(result) -> str:
    return result.content[0].text if result.content else ""


def tell(result) -> None:
    print("   server said:")
    for line in textwrap.wrap(said(result), 58):
        print("   | " + line)


def show(text: str) -> None:
    for line in text.strip().splitlines():
        print("   | " + line)


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
    # The server keeps its own log. Send it to a file, so a crash
    # inside the server does not spill a traceback over this proof.
    log = open("server.log", "w")
    os.dup2(log.fileno(), 2)
    checks = {}
    async with mcp.Client(params) as c:
        tools = {t.name for t in (await c.list_tools()).tools}
        checks["both tools are offered"] = (
            {"read_doc", "edit_doc"} <= tools)

        first = await c.call_tool("read_doc", {"name": DOC})
        if first.is_error:
            print(f"Could not read {DOC}. The server said:")
            show(said(first))
            return 1
        if WRONG not in said(first) and RIGHT in said(first):
            await c.call_tool("edit_doc", {
                "name": DOC, "find": RIGHT, "replace": WRONG})

        print(f"1. READ {DOC} FROM DRIVE")
        before = said(await c.call_tool("read_doc", {"name": DOC}))
        show(before)

        print("\n2. FIX THE TYPO")
        r = await c.call_tool("edit_doc", {
            "name": DOC, "find": WRONG, "replace": RIGHT})
        tell(r)

        print("\n3. READ IT BACK FROM DRIVE")
        after = said(await c.call_tool("read_doc", {"name": DOC}))
        show(after)
        checks["typo was there before"] = WRONG in before
        checks["typo is gone after"] = WRONG not in after
        checks["the draft changed on Drive"] = before != after

        print("\n4. ASK FOR WORDS THAT ARE NOT IN THE DRAFT")
        r = await c.call_tool("edit_doc", {
            "name": DOC, "find": "words that are not in there",
            "replace": "anything"})
        tell(r)
        still = said(await c.call_tool("read_doc", {"name": DOC}))
        checks["missing words change nothing"] = still == after

        print("\n5. ASK FOR A DRAFT THAT IS NOT THERE")
        r = await c.call_tool("read_doc", {"name": "not-here.md"})
        tell(r)
        print("   (the server's own log is in server.log)")
        checks["a missing draft is explained"] = (
            "no draft called" in said(r))

        res = (await c.list_resources()).resources
        if res:
            print("\n6. BROWSE THE FOLDER")
            got = await c.read_resource("drafts://folder")
            listing = got.contents[0].text
            names = [n for n in listing.splitlines() if n]
            for n in names:
                print("   | " + n)
            checks["the folder lists your draft"] = DOC in names

            print("\n7. READ ONE DRAFT AS A RESOURCE")
            got = await c.read_resource(f"drafts://{DOC}")
            show(got.contents[0].text)
            checks["the resource matches the tool"] = (
                got.contents[0].text == after)

        prompts = (await c.list_prompts()).prompts
        if prompts:
            print("\n8. FETCH THE SAVED JOB")
            got = await c.get_prompt("tidy_draft", {"name": DOC})
            words = got.messages[0].content.text
            for line in textwrap.wrap(words, 58):
                print("   | " + line)
            checks["the saved job names your draft"] = DOC in words

    print("\nVERDICT")
    for name, ok in checks.items():
        print(f"   {'PASS' if ok else 'FAIL'}  {name}")
    good = all(checks.values())
    print("\nRESULT:", "your server works." if good
          else "read the FAIL lines above.")
    return 0 if good else 1


sys.exit(asyncio.run(main()))
