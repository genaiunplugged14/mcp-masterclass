# Lesson 6: Multi-Agent Collaboration with MCP

This folder contains the complete working code for Lesson 6 of the MCP Masterclass. You'll build a multi-agent system where a Researcher agent and a Writer agent collaborate through a shared MCP server to create well-researched, well-written content.

## 📖 Read the Full Lesson

Before working with this code, read the complete lesson on Substack:  
**[Lesson 6: Multi-Agent Collaboration with MCP](YOUR_LESSON_6_URL)**

The article explains all the concepts, provides detailed context, and walks through the collaboration pattern with clear examples. This folder gives you the working code to implement what the lesson teaches.

## 📁 What's in This Folder

- **`server.py`** . The MCP server with three collaboration tools
- **`research_findings.txt`** . Example output from the Researcher agent
- **`final_draft.txt`** . Example output from the Writer agent
- **`check_setup.py`** . Script to verify your environment is ready
- **`requirements.txt`** . Python packages needed for this lesson
- **`conversation_templates.md`** . Example prompts for your agents
- **`README.md`** . This file with setup and usage instructions

## 🚀 Quick Start

Follow these steps to get the multi-agent system running.

### Step 1: Navigate to This Folder

Open your terminal and change into the lesson-06 directory:
```bash
cd lesson-06
```

### Step 2: Create a Virtual Environment

Create an isolated Python environment for this project:

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

You should see `(.venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

With the virtual environment active, install the required packages:
```bash
pip install -r requirements.txt
```

### Step 4: Verify Your Setup

Run the verification script:
```bash
python check_setup.py
```

You should see success messages confirming all MCP components are available.

### Step 5: Configure Claude Desktop

You need to update your Claude Desktop configuration to include this new server. The server has a different name (`collaboration-hub`) and different tools than the Lesson 5 server.

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

Open Claude Desktop, go to Settings, Developer tab, click Edit Config.

Add this new server to your configuration (keep your existing note-reader server from Lesson 5):
```json
{
  "mcpServers": {
    "note-reader": {
      "command": "/path/to/lesson-05/.venv/bin/python",
      "args": ["/path/to/lesson-05/server.py"]
    },
    "collaboration-hub": {
      "command": "/FULL/PATH/TO/lesson-06/.venv/bin/python",
      "args": ["/FULL/PATH/TO/lesson-06/server.py"]
    }
  }
}
```

Replace the paths with your actual paths. On Windows, remember to use double backslashes.

Save the file and completely quit and restart Claude Desktop.

### Step 6: Test Your Multi-Agent System

After restarting Claude Desktop, verify you see the collaboration-hub server with three tools: `save_research`, `read_research`, and `save_draft`.

Now let's run the collaboration workflow:

**Conversation 1 (Researcher Agent):**

Open a new conversation in Claude Desktop and say:

> "You are a research specialist. Research the topic: 'How to choose a programming language.' Cover key considerations like project type, performance needs, learning curve, community support, and job market. Organize your findings clearly, then use the save_research tool to save them."

Claude will act as a researcher, organize information, and save it using your tool.

**Conversation 2 (Writer Agent):**

Open a separate new conversation (this is important, it's a different agent) and say:

> "You are a professional writer. Use the read_research tool to read the research findings about choosing a programming language, then write a clear, engaging article for beginners. Make it practical and easy to understand. When done, use the save_draft tool to save it."

Claude will act as a writer, read the research, create an article, and save it.

**Check the Results:**

Navigate to your lesson-06 folder and open `final_draft.txt`. You'll see the complete article created through agent collaboration.

## 🧪 Understanding Multi-Agent Collaboration

The key insight is that both conversations (agents) connect to the same MCP server. They share tools and data through that server. This creates a collaboration pipeline:
```
Researcher Agent
  → Uses save_research tool
  → Saves to research_findings.txt
  
Writer Agent
  → Uses read_research tool
  → Reads research_findings.txt
  → Uses save_draft tool
  → Saves to final_draft.txt
```

Each agent focuses on its specialty. The MCP server coordinates their work. You orchestrate by giving each agent clear instructions.

## 🎯 Experiments to Try

**Add a Third Agent (Editor):**

Create a third conversation where Claude acts as an editor. Ask it to read the final draft (you might need to manually copy the content or add a read_draft tool) and suggest improvements.

**Different Topics:**

Try researching and writing about completely different topics. The same tools work for any content.

**Specialized Instructions:**

Give more specific guidance to each agent. Tell the Researcher to focus on technical accuracy. Tell the Writer to use a conversational tone. See how specialization improves results.

**Reverse the Workflow:**

Have the Writer create an outline first, then have the Researcher fill in details. Your MCP system handles any workflow order.

## 🔧 Troubleshooting

### Tools don't appear in Claude Desktop

Make sure you:
- Completely quit and restarted Claude Desktop after editing the config
- Used the correct paths for this lesson's virtual environment and server
- Named the server "collaboration-hub" in your config (matching the server code)

### "File not found" errors

The `read_research` tool looks for `research_findings.txt` in the lesson-06 folder. Make sure:
- You ran the Researcher Agent first to create the file
- The file was actually saved (check your lesson-06 folder)
- You're in the correct folder when running commands

### Agent doesn't use the tools

Make sure you explicitly mention the tool names in your instructions. Claude needs clear direction like "use the save_research tool" rather than just "save your findings."

### Multiple servers conflict

If you have both note-reader (Lesson 5) and collaboration-hub (Lesson 6) configured, that's fine. They're separate servers with different tools. When you talk to Claude, it will see all available tools from all configured servers.

## 📚 Understanding the Code

Open `server.py` and read through the comments. You'll see the same patterns from Lesson 5, just with three tools instead of one:

- `save_research` writes to research_findings.txt
- `read_research` reads from research_findings.txt  
- `save_draft` writes to final_draft.txt

Each tool follows the exact same structure: validate inputs, perform action, return result. Once you understand one tool, you understand them all.

## 💬 Need Help?

Check the main repository's issues section if you're stuck. Open a new issue if you encounter problems not covered in this troubleshooting guide.

## ⏭️ Next Steps

Once your multi-agent collaboration is working smoothly, you're ready for Lesson 7 where you'll add shared memory to your agents. They'll remember past conversations and build on previous work, transforming simple collaboration into true teamwork.

Head back to the main repository README to find Lesson 7, or subscribe to the Substack newsletter for notifications when new lessons are published.