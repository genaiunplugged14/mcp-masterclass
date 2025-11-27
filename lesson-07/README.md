# Lesson 7: Adding Shared Memory

This folder contains the complete working code for Lesson 7 of the MCP Masterclass. You'll add shared memory to the multi-agent system from Lesson 6, enabling agents to remember insights, build on past work, and improve over time.

## 📖 Read the Full Lesson

Before working with this code, read the complete lesson on Substack:  
**[Lesson 7: Adding Shared Memory](YOUR_LESSON_7_URL)**

The article explains all the concepts, provides detailed context, and walks through the memory patterns with clear explanations.

## 📁 What's in This Folder

- **`server.py`** - MCP server with three memory tools (save, read, search)
- **`shared_memory.json`** - Memory storage file (empty initially, populated by agents)
- **`check_setup.py`** - Script to verify your environment is ready
- **`requirements.txt`** - Python packages needed for this lesson
- **`conversation_templates.md`** - Prompts for memory-aware Researcher and Writer agents
- **`example_memory.json`** - Example showing what populated memory looks like
- **`README.md`** - This file with setup and usage instructions

## 🚀 Quick Start

### Prerequisites

You should have completed Lesson 6 (multi-agent collaboration) before starting this lesson. You'll be adding memory capabilities to that existing system.

### Step 1: Navigate to This Folder
```bash
cd lesson-07
```

### Step 2: Create Virtual Environment

**On macOS or Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
py -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Setup
```bash
python check_setup.py
```

You should see success messages confirming the MCP SDK is installed correctly.

### Step 5: Configure Claude Desktop

You need to tell Claude Desktop about your memory-enabled MCP server.

**Get your Python path:**

On macOS or Linux:
```bash
which python
```

On Windows:
```bash
where python
```

**Get your server.py path:**

On macOS or Linux:
```bash
pwd
```
Then add `/server.py` to the end.

On Windows:
```bash
cd
```
Then add `\server.py` to the end.

**Edit Claude Desktop's configuration:**

Open Claude Desktop, go to Settings → Developer → Edit Config. Add this configuration:
```json
{
  "mcpServers": {
    "memory-server": {
      "command": "/FULL/PATH/TO/YOUR/.venv/bin/python",
      "args": [
        "/FULL/PATH/TO/YOUR/server.py"
      ]
    }
  }
}
```

Replace the paths with your actual paths from the steps above.

**For Windows users:** Use double backslashes in paths:
```json
"command": "C:\\Users\\yourname\\mcp-masterclass\\lesson-07\\.venv\\Scripts\\python.exe"
```

Save and completely quit Claude Desktop, then restart it.

### Step 6: Verify Connection

After restarting Claude Desktop, start a new conversation. Look for the hammer icon at the bottom right. Click it and verify you see:
- **memory-server** listed
- Three tools available: **save_memory**, **read_memory**, **search_memory**

## 🧪 How to Use Memory-Enabled Agents

### Researcher Agent with Memory

Open a conversation in Claude Desktop and use this prompt:
```
You are a research specialist with memory capabilities.

Before starting any research task:
1. Use read_memory tool to check what you already know about the topic
2. Build on existing knowledge instead of starting from scratch

After completing research:
1. Use save_memory tool to store key insights, valuable sources, and learnings
2. Document what worked well and what to avoid next time

Your current task: Research how to choose a database (SQL vs NoSQL). 
Use your memory to see if you have any relevant past research, then complete this task 
and save what you learn.
```

### Writer Agent with Memory

Open a **separate conversation** (this is a different agent) and use this prompt:
```
You are a professional writer with memory capabilities.

Before starting any writing task:
1. Use read_memory tool to check past learnings about writing style and reader preferences
2. Apply successful patterns from previous work

After completing writing:
1. Use save_memory tool to store what worked well in this piece
2. Document reader feedback or insights about content structure

Your current task: Use read_memory to see if there's research on databases. 
If there is, write a clear article about choosing databases. 
After writing, save insights about what writing patterns you used.
```

### What You'll Observe

**First time running:**
- Memory is empty, agents work normally
- They save learnings after completing tasks
- `shared_memory.json` gets populated

**Second time running:**
- Agents read memory first
- They reference past findings
- Work completes faster with better quality
- New learnings are added to existing memory

**Third time running:**
- Rich memory context available
- Agents highly efficient
- Quality compounds over time

## 📝 Understanding the Code

### Memory Tools

**save_memory(content: str)**
- Accepts text content to remember
- Adds timestamp and stores in `shared_memory.json`
- Returns confirmation message

**read_memory()**
- Reads all memories from storage
- Returns formatted text of all entries
- Sorted by timestamp (most recent first)

**search_memory(query: str)**
- Searches memory content for matching terms
- Returns only relevant entries
- Case-insensitive matching

### Memory Storage Format

Each memory entry in `shared_memory.json` looks like:
```json
{
  "timestamp": "2025-01-15T14:30:00",
  "content": "Research completed on databases. Best sources: DB-Engines ranking, 
             PostgreSQL docs. Key insight: Choose SQL when data structure is consistent 
             and relationships matter. NoSQL when flexibility and scale are priorities."
}
```

Simple, readable, and effective.

## 🔧 Troubleshooting

### Memory file doesn't exist

The `shared_memory.json` file gets created automatically when the first memory is saved. If you want to start with an empty file, create it manually:
```bash
echo "[]" > shared_memory.json
```

### Agents aren't using memory tools

Make sure:
1. Claude Desktop shows the hammer icon with your memory-server
2. Your prompts explicitly tell agents to use memory tools
3. You're allowing tool usage when Claude asks for permission

### Memory isn't persisting across restarts

Check that:
1. The `shared_memory.json` file is in the same directory as `server.py`
2. The file has write permissions
3. You're not accidentally deleting the file between sessions

### Can't see previous memories

If `read_memory` returns empty when you know memories exist:
1. Check that `shared_memory.json` isn't empty (open it in a text editor)
2. Verify the file path in server.py points to the right location
3. Try restarting the MCP server (restart Claude Desktop)

## 💡 Experiments to Try

### Experiment 1: Memory Accumulation

Run the same research task 3 times and observe:
- Time taken decreases each iteration
- Quality improves as patterns emerge
- Agents reference specific past findings

### Experiment 2: Cross-Agent Learning

Have Researcher save detailed findings, then have Writer read them and create content. Notice how Writer can reference specific research points without you manually providing them.

### Experiment 3: Memory Search

Populate memory with several different topics, then use search_memory to find specific information. See how targeted retrieval works compared to reading all memories.

### Experiment 4: Adding a Third Agent

Create an Editor agent that reviews written content and stores quality feedback. Watch how Writer improves by reading editorial notes from memory.

## 🎯 What You Accomplished

After completing this lesson, you've built:

✅ An MCP server with persistent memory storage  
✅ Three memory management tools (save, read, search)  
✅ A multi-agent system where agents learn from experience  
✅ Institutional knowledge that compounds over time  
✅ The foundation for truly intelligent AI systems

This pattern scales to any workflow where learning from the past improves future performance.

## ⏭️ Next Steps

Once your memory-enabled agents are working smoothly, you're ready for Lesson 8: Continuous Learning Systems. You'll move beyond storing memories to actively learning from patterns, identifying what works, and automatically adjusting behavior.

Memory stores history. Learning changes behavior based on that history.

## 💬 Need Help?

If you're stuck, check:
1. The troubleshooting section above
2. The main repository's issues section
3. The example_memory.json file to see what successful memory looks like

Remember: Memory is the foundation of improvement. Take time to understand how agents use it, and you'll see why this capability transforms AI systems from tools into teammates.

Happy building!