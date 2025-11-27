"""
Environment Setup Verification for Lesson 7

Checks that all required MCP components are installed correctly.
"""

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    import json
    from datetime import datetime
    
    print("✓ MCP SDK is installed correctly!")
    print("✓ All required components are available")
    print("✓ JSON and datetime modules working")
    print("\nYou're ready to build memory-enabled agents!")
    
except ImportError as e:
    print("✗ MCP SDK installation issue detected:")
    print(f"  Error: {e}")
    print("\nPlease make sure you:")
    print("  1. Activated the virtual environment")
    print("  2. Ran: pip install -r requirements.txt")
    print("  3. Are using Python 3.10 or higher")
```

---

## **File 4: requirements.txt**
```
mcp>=1.0.0