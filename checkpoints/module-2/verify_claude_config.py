"""Did Claude Desktop actually pick up your server?

Editing claude_desktop_config.json tells you nothing on its own. The only proof
is that Claude STARTED your server, and you can see that from a terminal without
opening the app or guessing at its interface.

    python3 verify_claude_config.py

Never prints the contents of your config. That file holds tokens for any server
that needs one, so it is not safe to put on a screen.
"""
import json
import os
import subprocess
import sys

MAC = "~/Library/Application Support/Claude/claude_desktop_config.json"
WIN = "~/AppData/Roaming/Claude/claude_desktop_config.json"


def main():
    path = next((p for p in (os.path.expanduser(MAC), os.path.expanduser(WIN))
                 if os.path.exists(p)), None)
    if not path:
        print("No config file yet. That is step 4 of lesson 3.")
        return 1

    print("1. WHAT HAVE YOU ASKED CLAUDE TO RUN?")
    try:
        servers = (json.load(open(path)).get("mcpServers") or {})
    except json.JSONDecodeError as err:
        print("   Your config is not valid JSON: %s" % err)
        print("   -> usually a missing comma or a stray bracket. Fix that first.")
        return 2
    if not servers:
        print("   nothing. The mcpServers section is empty.")
        return 1
    for name, cfg in servers.items():
        print("   %-14s %s" % (name, cfg.get("command", "?")))

    print("\n2. IS CLAUDE DESKTOP RUNNING?")
    running = subprocess.run(["pgrep", "-x", "Claude"], capture_output=True).returncode == 0
    print("   %s" % ("yes" if running else "no. Open it, then run this again."))
    if not running:
        return 1

    print("\n3. DID IT ACTUALLY START THEM?")
    ps = subprocess.run(["ps", "ax", "-o", "command"], capture_output=True, text=True).stdout
    started = []
    for name, cfg in servers.items():
        needle = next((a for a in cfg.get("args", []) if "/" in a and not a.startswith("-")), name)
        hit = needle.split("/")[-1] in ps
        started.append(hit)
        print("   %-14s %s" % (name, "started" if hit else "NOT started"))

    print()
    if all(started):
        print("RESULT: your config worked. Claude is running every server in it.")
        return 0
    print("RESULT: Claude is running, but not every server started.")
    print("  Quit Claude completely and open it again. Closing the window is not enough.")
    print("  Then check every path in the config is a full path from the top of your disk.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
