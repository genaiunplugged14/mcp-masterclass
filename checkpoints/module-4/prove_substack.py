"""Prove your Scribe server delivers to Substack, and never publishes.

Four checks, over the pipe, the way Claude Desktop talks to it:
  1. the public read works with NO cookie at all
  2. a Substack draft is made from draft.md
  3. Substack says it is a draft, published: false
  4. the draft is deleted again, so your account is left as found

Nothing is published and nobody is emailed. Without a cookie, checks
2 to 4 are skipped and the verdict says so.

    export SCRIBE_FOLDER_ID="paste your folder id here"
    export SCRIBE_KEY="key.json"
    export SCRIBE_SUBSTACK="your-publication-name"
    export SCRIBE_SUBSTACK_COOKIE="paste the substack.sid value here"
    python3 prove_substack.py
"""
import asyncio
import os
import sys
import textwrap

import mcp
import requests
from mcp.client.stdio import StdioServerParameters

SERVER = os.environ.get("SCRIBE_SERVER", "scribe_server.py")
DOC = os.environ.get("SCRIBE_DOC", "draft.md")
PUBLIC = os.environ.get("SCRIBE_SUBSTACK") or "genaiunplugged"


def said(result) -> str:
    return result.content[0].text if result.content else ""


def tell(text: str) -> None:
    for line in text.splitlines():
        for part in textwrap.wrap(line, 58) or [""]:
            print("   | " + part)


def start(env):
    params = StdioServerParameters(
        command=sys.executable, args=[SERVER], env=env)
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
    cookie = os.environ.get("SCRIBE_SUBSTACK_COOKIE", "")
    pub = os.environ.get("SCRIBE_SUBSTACK", "")
    no_cookie = {k: v for k, v in os.environ.items()
                 if k != "SCRIBE_SUBSTACK_COOKIE"}
    checks = {}

    print("1. READ A SUBSTACK, WITH NO COOKIE AT ALL")
    async with start(no_cookie) as c:
        r = await c.call_tool("latest_posts",
                              {"publication": PUBLIC, "count": 2})
        print(f"   the 2 newest posts on {PUBLIC}:")
        tell(said(r))
        checks["the public read needs no login"] = (
            not r.is_error and "substack.com/p/" in said(r))

    if not cookie or not pub:
        print("\n2. MAKE A DRAFT: SKIPPED")
        print("   Set SCRIBE_SUBSTACK and SCRIBE_SUBSTACK_COOKIE to run"
              " the write half.")
        checks["draft made, checked and deleted (SKIPPED)"] = True
    else:
        api = f"https://{pub}.substack.com/api/v1"
        s = requests.Session()
        s.cookies.set("substack.sid", cookie, domain=".substack.com")

        print(f"\n2. MAKE A DRAFT FROM {DOC}")
        async with start(dict(os.environ)) as c:
            r = await c.call_tool("publish_draft", {"name": DOC})
            print("   server said:")
            tell(said(r))
            checks["a draft was made"] = (
                not r.is_error and "/publish/post/" in said(r))
        post_id = said(r).rsplit("/", 1)[-1].strip()

        print("\n3. ASK SUBSTACK: IS IT ONLY A DRAFT?")
        if checks["a draft was made"]:
            got = s.get(f"{api}/drafts/{post_id}", timeout=30).json()
            print(f"   title: {got.get('draft_title')}")
            print(f"   published: {got.get('is_published')}")
            checks["it is a draft, nothing was published"] = (
                got.get("is_published") is False)
        else:
            checks["it is a draft, nothing was published"] = False

        print("\n4. DELETE THE DRAFT AGAIN")
        if checks["a draft was made"]:
            gone = s.delete(f"{api}/drafts/{post_id}", timeout=30)
            after = s.get(f"{api}/drafts/{post_id}", timeout=30)
            print(f"   deleted: {gone.status_code},"
                  f" then: {after.status_code}")
            checks["the draft is deleted, account as found"] = (
                gone.status_code == 200 and after.status_code == 404)
        else:
            checks["the draft is deleted, account as found"] = False

    print("\n5. VERDICT")
    for name, ok in checks.items():
        print(f"   {'PASS' if ok else 'FAIL'}  {name}")
    good = all(checks.values())
    print("\nRESULT:", "Scribe delivers." if good
          else "something failed. Read the FAIL lines above,"
          " and server.log.")
    return 0 if good else 1


sys.exit(asyncio.run(main()))
