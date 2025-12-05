"""
Environment Setup Verification Script for Lesson 8

This script checks that all required MCP components are installed correctly.
Run this before starting the lesson to catch any installation issues early.

If you see errors, make sure you:
1. Activated the virtual environment
2. Ran 'pip install -r requirements.txt'
3. Are using Python 3.10 or higher
"""

import sys

# Check Python version
python_version = sys.version_info
if python_version < (3, 10):
    print(f"✗ Python version {python_version.major}.{python_version.minor} detected")
    print("  MCP requires Python 3.10 or higher")
    print("  Please upgrade Python and try again")
    sys.exit(1)
else:
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro} detected")

# Check MCP SDK installation
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    print("✓ MCP SDK is installed correctly!")
    print("✓ All required components are available")
    print("\nYou're ready to build learning agents with MCP!")
    print("\nNext steps:")
    print("1. Configure Claude Desktop (see README.md)")
    print("2. Restart Claude Desktop")
    print("3. Start testing the learning tools")
    
except ImportError as e:
    print("✗ MCP SDK installation issue detected:")
    print(f"  Error: {e}")
    print("\nPlease make sure you:")
    print("  1. Activated the virtual environment")
    print("  2. Ran: pip install -r requirements.txt")
    print("  3. Are using Python 3.10 or higher")
    sys.exit(1)
