"""Ask your Scribe server what it offers.

This starts scribe_server.py as its own program and talks to it
over the pipe, which is exactly what Claude Desktop does. So the
list you see here is the list Claude sees.

Set your folder id and your key first, then run it:

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    python3 what_can_it_do.py
"""
import asyncio
import os
import sys

import mcp
from mcp.client.stdio import StdioServerParameters

SERVER = os.environ.get("SCRIBE_SERVER", "scribe_server.py")


def need(name: str) -> None:
    if not os.environ.get(name):
        sys.exit(f"{name} is not set. See the top of this file.")


def inputs_of(schema: dict) -> list:
    must = set(schema.get("required") or [])
    rules = schema.get("properties") or {}
    lines = []
    for name, rule in rules.items():
        kind = rule.get("type", "anything")
        tail = "required" if name in must else "optional"
        lines.append(f"    input: {name} ({kind}, {tail})")
    return lines or ["    input: none"]


async def main() -> None:
    need("SCRIBE_FOLDER_ID")
    os.environ.setdefault("SCRIBE_KEY", "key.json")
    if not os.path.exists(SERVER):
        sys.exit(f"Cannot find {SERVER}. Run this from your scribe"
                 " folder.")
    params = StdioServerParameters(
        command=sys.executable, args=[SERVER],
        env=dict(os.environ))
    async with mcp.Client(params) as c:
        tools = (await c.list_tools()).tools
        print("TOOLS")
        for t in tools:
            print(f"  {t.name}")
            print(f"    {t.description}")
            for line in inputs_of(t.input_schema):
                print(line)
        if not tools:
            print("  none yet")

        res = (await c.list_resources()).resources
        found = await c.list_resource_templates()
        tpl = found.resource_templates
        if res or tpl:
            print("\nRESOURCES")
            for r in res:
                print(f"  {r.uri}")
                print(f"    {r.description}")
            for t in tpl:
                print(f"  {t.uri_template}")
                print(f"    {t.description}")

        prompts = (await c.list_prompts()).prompts
        if prompts:
            print("\nPROMPTS")
            for p in prompts:
                print(f"  {p.name}")
                print(f"    {p.description}")
                for a in (p.arguments or []):
                    print(f"    input: {a.name}")


asyncio.run(main())
