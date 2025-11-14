"""
Lesson 5: Simple MCP Server with File Reading Tool

This server demonstrates the core patterns of MCP server development:
- Creating a server instance with a name
- Defining tools that AI models can use
- Handling tool execution requests
- Communicating with MCP clients through stdio

The server exposes a single tool called 'read_note' that reads text files
from the local filesystem and returns their content.
"""

import asyncio
from pathlib import Path
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Create the server instance with a unique name
# This name identifies your server to MCP clients like Claude Desktop
server = Server("note-reader")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    Tell MCP clients what tools this server provides.
    
    This handler is called when a client (like Claude Desktop) connects
    and asks "what can you do?" The response defines each tool's name,
    description, and what arguments it accepts.
    
    The inputSchema uses JSON Schema format to describe the tool's parameters.
    This lets the AI model know what information it needs to provide when
    calling the tool.
    """
    return [
        Tool(
            name="read_note",
            description="Read a text file from the local filesystem",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Name of the file to read (e.g., 'sample_note.txt')"
                    }
                },
                "required": ["filename"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute a tool when the AI model requests it.
    
    This handler receives:
    - name: The tool name the AI wants to use
    - arguments: The parameters the AI provided for that tool
    
    It should:
    1. Validate that the tool name is recognized
    2. Extract and validate the arguments
    3. Execute the requested action
    4. Return the results in a format the AI can understand
    
    All responses must be wrapped in TextContent objects, which is how
    MCP standardizes communication between servers and clients.
    """
    
    # Verify we recognize this tool name
    if name != "read_note":
        raise ValueError(f"Unknown tool: {name}")
    
    # Extract the filename argument
    # We check if it exists because even required fields should be validated
    filename = arguments.get("filename")
    if not filename:
        raise ValueError("Missing required argument: filename")
    
    # Build the file path
    # __file__ is the path to this server.py file
    # .parent gets the directory containing it (the lesson-05 folder)
    # / filename adds the requested filename to that path
    file_path = Path(__file__).parent / filename
    
    # Check if the file actually exists
    # It's better to give a clear error message than to crash
    if not file_path.exists():
        return [TextContent(
            type="text",
            text=f"Error: File '{filename}' not found in the server directory."
        )]
    
    # Read and return the file content
    try:
        content = file_path.read_text(encoding="utf-8")
        return [TextContent(
            type="text",
            text=content
        )]
    except Exception as e:
        # If anything goes wrong during reading (permissions, encoding issues, etc.)
        # return a helpful error message instead of crashing
        return [TextContent(
            type="text",
            text=f"Error reading file: {str(e)}"
        )]


async def main():
    """
    Start the MCP server and run it indefinitely.
    
    This function sets up the stdio transport, which is how Claude Desktop
    communicates with your server. The server reads requests from stdin
    and writes responses to stdout.
    
    The server runs until the client disconnects or the process is terminated.
    """
    # stdio_server() creates the communication channel
    # It returns read and write streams that the server uses to communicate
    async with stdio_server() as (read_stream, write_stream):
        # Start the server with those streams and initialization options
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="note-reader",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


# This is the entry point when the script is run
if __name__ == "__main__":
    # Run the async main function
    # The server will keep running until stopped with Ctrl+C or by the client disconnecting
    asyncio.run(main())
```

---

## **File 3: sample_note.txt (Example Data)**

This is the text file that the MCP tool will read. It should contain content that makes sense when Claude reads and responds to it.
```
This is my first MCP server.

MCP lets Claude Desktop connect to tools I create.
Those tools can read data, write data, or trigger actions.

Now Claude can use my custom tools to help me get work done.
This opens up endless possibilities for automation and AI assistance.

The patterns I'm learning in this lesson will scale to much more complex systems.
