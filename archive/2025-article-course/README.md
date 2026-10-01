# The 2025 article course

This folder is the code for the first version of the MCP Masterclass: 8 lessons published as
Substack articles in 2025. The code was fixed for the MCP Python SDK v2 on 2026-09-03 and runs on
`mcp[cli]>=2.1,<3`. The last commit of that course is tagged `article-course-2025`, and
[MIGRATION.md](MIGRATION.md) explains what changed in the SDK and why.

It is superseded by the video masterclass at
[genaiunplugged.com/courses/mcp](https://www.genaiunplugged.com/courses/mcp/): 4 modules, 30
lessons, one server built end to end. The code for that course lives in the repo root and in
`checkpoints/`.

Two articles from the old course stay up as standalone reads, and their code is here:

| Article | Code |
|---|---|
| [Multi-agent AI collaboration tutorial](https://genaiunplugged.substack.com/p/multi-agent-ai-collaboration-tutorial) | [`lesson-06/`](lesson-06) |
| [AI agent memory and learning systems](https://genaiunplugged.substack.com/p/ai-agent-memory-learning-systems) | [`lesson-08/`](lesson-08) |

Nothing in here is maintained beyond the SDK v2 fix. If something breaks, open an issue and say
which folder.
