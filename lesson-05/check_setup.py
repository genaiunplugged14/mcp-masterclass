"""
Environment Setup Verification Script

This script checks that all required MCP components are installed correctly.
Run this before starting the lesson to catch any installation issues early.

If you see errors, make sure you:
1. Activated the virtual environment
2. Ran 'pip install -r requirements.txt'
3. Are using Python 3.10 or higher
"""

try:
    # Try to import the core MCP components we'll use in this lesson
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    print("✓ MCP SDK is installed correctly!")
    print("✓ All required components are available")
    print("\nYou're ready to build your first MCP server!")
    
except ImportError as e:
    print("✗ MCP SDK installation issue detected:")
    print(f"  Error: {e}")
    print("\nPlease make sure you:")
    print("  1. Activated the virtual environment")
    print("  2. Ran: pip install -r requirements.txt")
    print("  3. Are using Python 3.10 or higher")
```

---

## **File 5: requirements.txt (Python Dependencies)**

This simple file lists all the Python packages needed for the lesson.
```
mcp>=1.0.0
