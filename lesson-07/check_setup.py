"""Run this before you start. It tells you whether your setup is ready."""
import importlib.util
import sys
from pathlib import Path

ok = True

if sys.version_info < (3, 10):
    print(f"FAIL  Python is {sys.version_info.major}.{sys.version_info.minor}. You need 3.10 or newer.")
    ok = False
else:
    print(f"OK    Python {sys.version_info.major}.{sys.version_info.minor}")

try:
    from mcp.server import MCPServer  # noqa: F401
    print("OK    The mcp package is installed, and MCPServer imports.")
except ImportError as e:
    print(f"FAIL  {e}")
    print('      Run: pip install "mcp[cli]>=2.1,<3"')
    print("      If you see the name FastMCP anywhere, you are on the old version 1.")
    print("      Read MIGRATION.md in the top folder of this repo.")
    ok = False

try:
    spec = importlib.util.spec_from_file_location("server", Path(__file__).parent / "server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "mcp"):
        print("OK    server.py loads and the server is set up.")
    else:
        print("FAIL  server.py loaded but has no server object called mcp.")
        ok = False
except Exception as e:
    print(f"FAIL  server.py did not load: {type(e).__name__}: {e}")
    ok = False

print()
print("You are ready." if ok else "Fix the FAIL lines above, then run this again.")
sys.exit(0 if ok else 1)
