"""Lesson 8: keep score, so the next run starts better than the last.

Lesson 7 remembered what happened. This one counts how often each approach
worked, and says which one to reach for next time.
"""
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from mcp.server import MCPServer

DATA = Path(__file__).parent / "learning_data.json"
mcp = MCPServer("learning-server")


def _load() -> list:
    if not DATA.exists():
        return []
    try:
        return json.loads(DATA.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save(items: list) -> None:
    DATA.write_text(json.dumps(items, indent=2), encoding="utf-8")


@mcp.tool()
def record_experience(task: str, approach: str, worked: bool, notes: str = "") -> str:
    """Record how one approach to a task turned out. Say whether it worked."""
    items = _load()
    items.append({
        "task": task,
        "approach": approach,
        "worked": worked,
        "notes": notes,
        "at": datetime.now().isoformat(timespec="seconds"),
    })
    _save(items)
    word = "experience" if len(items) == 1 else "experiences"
    return f"Recorded. There are now {len(items)} {word} for me to learn from."


@mcp.tool()
def get_learning_insights(task: str) -> str:
    """Say which approach has worked best for a task so far, and how sure we are."""
    runs = [i for i in _load() if i["task"].lower() == task.lower()]
    if not runs:
        return f"No experience recorded for {task} yet."

    tally: dict = defaultdict(lambda: [0, 0])   # approach -> [wins, total]
    for r in runs:
        tally[r["approach"]][1] += 1
        if r["worked"]:
            tally[r["approach"]][0] += 1

    lines = []
    for approach, (wins, total) in sorted(tally.items(), key=lambda kv: -kv[1][0] / kv[1][1]):
        rate = round(100 * wins / total)
        confidence = "reliable" if total >= 15 else "tentative" if total >= 5 else "too early to say"
        lines.append(f"{approach}: worked {wins} of {total} times ({rate}%), {confidence}")

    best = max(tally.items(), key=lambda kv: kv[1][0] / kv[1][1])[0]
    return "\n".join(lines) + f"\n\nStart with: {best}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
