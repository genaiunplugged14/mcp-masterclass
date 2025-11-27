"""
Environment Setup Verification Script for Lesson 6

Verifies that all required MCP components are installed correctly.
"""

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    
    print("✓ MCP SDK is installed correctly!")
    print("✓ All required components are available")
    print("\nYou're ready to build your multi-agent collaboration system!")
    
except ImportError as e:
    print("✗ MCP SDK installation issue detected:")
    print(f"  Error: {e}")
    print("\nPlease make sure you:")
    print("  1. Activated the virtual environment")
    print("  2. Ran: pip install -r requirements.txt")
    print("  3. Are using Python 3.10 or higher")
```

---

### **File 4: requirements.txt**
```
mcp>=1.0.0