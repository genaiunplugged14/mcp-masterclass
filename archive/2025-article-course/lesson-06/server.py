"""Lesson 6: a shared workspace that two agents can both reach.

One Claude chat plays the researcher and saves findings. A second chat plays
the writer, reads those findings, and saves a draft. The server is nothing but
the shared filing cabinet they both use.
"""
from pathlib import Path
from mcp.server import MCPServer

WORK = Path(__file__).parent / "workspace"
WORK.mkdir(exist_ok=True)
mcp = MCPServer("collaboration-hub")


@mcp.tool()
def save_research(findings: str) -> str:
    """Save research findings so another agent can read them later."""
    (WORK / "research.md").write_text(findings, encoding="utf-8")
    return "Research saved. The writer can read it now."


@mcp.tool()
def read_research() -> str:
    """Read the research findings that were saved earlier."""
    f = WORK / "research.md"
    if not f.exists():
        return "There is no research saved yet."
    return f.read_text(encoding="utf-8")


@mcp.tool()
def save_draft(draft: str) -> str:
    """Save a finished draft that was written from the research."""
    (WORK / "draft.md").write_text(draft, encoding="utf-8")
    return "Draft saved."


if __name__ == "__main__":
    mcp.run(transport="stdio")
