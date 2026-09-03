"""Lesson 7: memory that outlives the chat it was made in.

Lesson 6 gave two agents a shared workspace, but every new chat still started
from nothing. These 3 tools let anything worth keeping survive the session.
"""
import json
from datetime import datetime
from pathlib import Path
from mcp.server import MCPServer

MEMORY = Path(__file__).parent / "shared_memory.json"
mcp = MCPServer("memory-server")


def _load() -> list:
    """Read the memory file. An empty or damaged file means no memories yet."""
    if not MEMORY.exists():
        return []
    try:
        return json.loads(MEMORY.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save(items: list) -> None:
    MEMORY.write_text(json.dumps(items, indent=2), encoding="utf-8")


def _format(items: list) -> str:
    return "\n".join(f"[{i['saved']}] {i['topic']}: {i['insight']}" for i in items)


@mcp.tool()
def save_memory(topic: str, insight: str) -> str:
    """Remember one insight about a topic, so a later chat can use it."""
    items = _load()
    items.append({
        "topic": topic,
        "insight": insight,
        "saved": datetime.now().isoformat(timespec="seconds"),
    })
    _save(items)
    thing = "thing" if len(items) == 1 else "things"
    return f"Saved. I now remember {len(items)} {thing}."


@mcp.tool()
def read_memory() -> str:
    """Read everything that has been remembered so far."""
    items = _load()
    if not items:
        return "Nothing has been remembered yet."
    return _format(items)


@mcp.tool()
def search_memory(term: str) -> str:
    """Find remembered insights that mention a word."""
    needle = term.lower()
    hits = [i for i in _load()
            if needle in i["topic"].lower() or needle in i["insight"].lower()]
    if not hits:
        return f"Nothing remembered mentions {term}."
    return _format(hits)


if __name__ == "__main__":
    mcp.run(transport="stdio")
