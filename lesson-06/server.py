"""
Lesson 6: Multi-Agent Collaboration MCP Server

This server demonstrates how multiple AI agents can collaborate by sharing
tools and data through a common MCP server. It provides three tools that
create a collaboration pipeline:

1. save_research: Lets a Researcher agent save findings
2. read_research: Lets any agent read those findings
3. save_draft: Lets a Writer agent save the final document

This is the same pattern as Lesson 5, just with multiple tools instead of one.
"""

import asyncio
from pathlib import Path
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Create the server instance with a descriptive name
server = Server("collaboration-hub")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    Define all tools this server provides.
    
    Each tool represents a capability that AI agents can use to collaborate.
    Notice how all three tools follow the same pattern, just with different
    purposes and file targets.
    """
    return [
        Tool(
            name="save_research",
            description="Save research findings to a file for other agents to read",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The research findings to save"
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="read_research",
            description="Read research findings saved by the Researcher agent",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        Tool(
            name="save_draft",
            description="Save a final draft document",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The final draft content to save"
                    }
                },
                "required": ["content"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute the requested tool.
    
    This handler routes tool calls to the appropriate logic based on the
    tool name. Each tool follows the same pattern: validate, execute, return.
    """
    
    # Get the base directory where this server lives
    base_dir = Path(__file__).parent
    
    # Route to the appropriate tool handler
    if name == "save_research":
        return await save_research_handler(arguments, base_dir)
    elif name == "read_research":
        return await read_research_handler(base_dir)
    elif name == "save_draft":
        return await save_draft_handler(arguments, base_dir)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def save_research_handler(arguments: dict, base_dir: Path) -> list[TextContent]:
    """
    Save research findings to a file.
    
    The Researcher agent uses this tool to store its work so other agents
    can access it later.
    """
    content = arguments.get("content")
    if not content:
        return [TextContent(
            type="text",
            text="Error: No content provided to save"
        )]
    
    # Save to research_findings.txt
    file_path = base_dir / "research_findings.txt"
    
    try:
        file_path.write_text(content, encoding="utf-8")
        return [TextContent(
            type="text",
            text=f"Research findings saved successfully to {file_path.name}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error saving research: {str(e)}"
        )]


async def read_research_handler(base_dir: Path) -> list[TextContent]:
    """
    Read research findings from the file.
    
    Any agent can use this tool to access what the Researcher saved.
    This is how agents share information.
    """
    file_path = base_dir / "research_findings.txt"
    
    if not file_path.exists():
        return [TextContent(
            type="text",
            text="No research findings found. The Researcher agent needs to save research first using the save_research tool."
        )]
    
    try:
        content = file_path.read_text(encoding="utf-8")
        return [TextContent(
            type="text",
            text=content
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error reading research: {str(e)}"
        )]


async def save_draft_handler(arguments: dict, base_dir: Path) -> list[TextContent]:
    """
    Save the final draft document.
    
    The Writer agent uses this tool to store the finished article.
    """
    content = arguments.get("content")
    if not content:
        return [TextContent(
            type="text",
            text="Error: No content provided to save"
        )]
    
    # Save to final_draft.txt
    file_path = base_dir / "final_draft.txt"
    
    try:
        file_path.write_text(content, encoding="utf-8")
        return [TextContent(
            type="text",
            text=f"Final draft saved successfully to {file_path.name}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error saving draft: {str(e)}"
        )]


async def main():
    """
    Start the MCP server and run it indefinitely.
    
    This is identical to Lesson 5. The only difference is we have more tools.
    """
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="collaboration-hub",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())