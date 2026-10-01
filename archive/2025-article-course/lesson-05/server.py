"""Desk: an MCP server that lets Claude read your notes."""
from pathlib import Path
from mcp.server import MCPServer

NOTES = Path(__file__).parent / "notes"
mcp = MCPServer("desk")


@mcp.tool()
def read_note(name: str) -> str:
    """Read one note from the notes folder. Give the file name, like ideas.txt."""
    note = NOTES / name
    if not note.exists():
        return f"There is no note called {name}."
    return note.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
