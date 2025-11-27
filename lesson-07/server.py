"""
Lesson 7: MCP Server with Shared Memory

This server extends the collaboration server from Lesson 6 by adding memory capabilities.
Three new tools enable agents to:
- save_memory: Store insights and learnings
- read_memory: Retrieve all past memories
- search_memory: Find specific relevant memories

Memory is stored in a simple JSON file that all agents can access.
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Create the server instance
server = Server("memory-server")

# Path to the memory storage file
MEMORY_FILE = Path(__file__).parent / "shared_memory.json"


def load_memories() -> list:
    """
    Load all memories from the JSON storage file.
    Returns empty list if file doesn't exist yet.
    """
    if not MEMORY_FILE.exists():
        return []
    
    try:
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is corrupted, return empty list
        return []


def save_memories(memories: list) -> bool:
    """
    Save all memories to the JSON storage file.
    Returns True if successful, False otherwise.
    """
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving memories: {e}")
        return False


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """
    Define the tools this server provides.
    All three tools work with the shared memory storage.
    """
    return [
        Tool(
            name="save_memory",
            description="Store an insight, learning, or outcome in shared memory. "
                       "Use this after completing tasks to remember what you learned.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The memory to save. Include key insights, successful "
                                     "patterns, mistakes to avoid, or valuable sources discovered."
                    }
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="read_memory",
            description="Read all stored memories. Use this before starting work to see "
                       "what you already know about a topic and build on past learnings.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="search_memory",
            description="Search memories for specific content. Use this to find relevant "
                       "past learnings about a specific topic or keyword.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term to find in memories (case-insensitive)"
                    }
                },
                "required": ["query"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Execute the requested memory tool.
    """
    
    if name == "save_memory":
        # Extract content from arguments
        content = arguments.get("content", "").strip()
        
        if not content:
            return [TextContent(
                type="text",
                text="Error: Cannot save empty memory. Please provide content to remember."
            )]
        
        # Load existing memories
        memories = load_memories()
        
        # Create new memory entry with timestamp
        new_memory = {
            "timestamp": datetime.now().isoformat(),
            "content": content
        }
        
        # Add to memories and save
        memories.append(new_memory)
        
        if save_memories(memories):
            return [TextContent(
                type="text",
                text=f"Memory saved successfully. Total memories: {len(memories)}"
            )]
        else:
            return [TextContent(
                type="text",
                text="Error: Failed to save memory to storage."
            )]
    
    elif name == "read_memory":
        # Load all memories
        memories = load_memories()
        
        if not memories:
            return [TextContent(
                type="text",
                text="No memories stored yet. Memory is empty."
            )]
        
        # Format memories for reading (most recent first)
        formatted_memories = []
        for i, memory in enumerate(reversed(memories), 1):
            timestamp = memory.get("timestamp", "Unknown time")
            content = memory.get("content", "")
            formatted_memories.append(f"[{i}] {timestamp}\n{content}\n")
        
        result = f"Found {len(memories)} memories:\n\n" + "\n".join(formatted_memories)
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    elif name == "search_memory":
        # Extract search query
        query = arguments.get("query", "").strip().lower()
        
        if not query:
            return [TextContent(
                type="text",
                text="Error: Please provide a search term."
            )]
        
        # Load memories and search
        memories = load_memories()
        
        if not memories:
            return [TextContent(
                type="text",
                text="No memories to search. Memory is empty."
            )]
        
        # Find matching memories (case-insensitive)
        matches = []
        for memory in memories:
            content = memory.get("content", "").lower()
            if query in content:
                matches.append(memory)
        
        if not matches:
            return [TextContent(
                type="text",
                text=f"No memories found matching '{query}'. Try a different search term."
            )]
        
        # Format matching memories
        formatted_matches = []
        for i, memory in enumerate(matches, 1):
            timestamp = memory.get("timestamp", "Unknown time")
            content = memory.get("content", "")
            formatted_matches.append(f"[{i}] {timestamp}\n{content}\n")
        
        result = f"Found {len(matches)} memories matching '{query}':\n\n" + "\n".join(formatted_matches)
        
        return [TextContent(
            type="text",
            text=result
        )]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """
    Start the MCP server with memory capabilities.
    """
    # Ensure memory file exists (create empty if needed)
    if not MEMORY_FILE.exists():
        save_memories([])
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="memory-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())