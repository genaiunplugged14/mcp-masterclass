# Lesson 5: Build Your First MCP Server with Claude Desktop

> **Updated September 2026.** This code was rewritten for MCP Python SDK version 2, where
> `FastMCP` became `MCPServer`. If you cloned this repo before then, read
> [MIGRATION.md](../MIGRATION.md) first. Verified against mcp 2.1.1.


This folder contains the complete working code for Lesson 5 of the MCP Masterclass. You'll build a simple MCP server that exposes a tool for reading text files, then connect it to Claude Desktop so Claude can use your tool in real conversations.

## 📖 Read the Full Lesson

Before working with this code, read the complete lesson on Substack:  
**[Lesson 5: Build Your First MCP Server with Claude Desktop](#)**

The article explains all the concepts, provides detailed context, and walks through each step with clear explanations. This folder gives you the working code to implement what the lesson teaches.

## 📁 What's in This Folder

- **`server.py`** - The complete MCP server with the read_note tool
- **`notes/`** - Your notes folder. The `read_note` tool reads files from in here.
- **`check_setup.py`** - Script to verify your environment is ready
- **`requirements.txt`** - Python packages needed for this lesson
- **`claude_desktop_config.json.example`** - Template configuration for Claude Desktop
- **`README.md`** - This file with setup and troubleshooting instructions

## 🚀 Quick Start

Follow these steps to get the MCP server running on your machine.

### Step 1: Navigate to This Folder

Open your terminal and change into the lesson-05 directory:
```bash
cd lesson-05
```

Make sure you're in the right place by running `pwd` on macOS or Linux, or `cd` on Windows. You should see a path ending in `lesson-05`.

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

After activation, you should see `(.venv)` at the start of your terminal prompt. This indicates the virtual environment is active and any packages you install will be isolated to this project.

### Step 3: Install Dependencies

With the virtual environment active, install the required packages:
```bash
pip install -r requirements.txt
```

This installs the MCP SDK, which contains everything you need to build MCP servers in Python. The installation might take a minute or two as it downloads and installs the necessary components.

### Step 4: Verify Your Setup

Run the verification script to confirm everything is installed correctly:
```bash
python check_setup.py
```

You should see success messages with checkmarks indicating that all required MCP components are available. If you see any errors at this point, make sure you activated the virtual environment in Step 2 and that the pip install in Step 3 completed without errors.

### Step 5: Configure Claude Desktop

Now you need to tell Claude Desktop about your MCP server. This is the connection that lets Claude use your custom tool.

First, find the full path to your Python executable and your server file. You need these exact paths for the configuration.

**Get your Python path:**

On macOS or Linux, run:
```bash
which python
```

On Windows, run:
```bash
where python
```

Copy the full path that gets printed. It will look something like `/Users/yourname/mcp-masterclass/lesson-05/.venv/bin/python` on macOS or `C:\Users\yourname\mcp-masterclass\lesson-05\.venv\Scripts\python.exe` on Windows.

**Get your server.py path:**

On macOS or Linux, run:
```bash
pwd
```
Then add `/server.py` to the end of what it prints.

On Windows, run:
```bash
cd
```
Then add `\server.py` to the end.

**Edit Claude Desktop's configuration:**

Open Claude Desktop and navigate to Settings. Click on the Developer tab, then click Edit Config. This opens the `claude_desktop_config.json` file in your default text editor.

Add this configuration, replacing the placeholder paths with your actual paths from above:
```json
{
  "mcpServers": {
    "note-reader": {
      "command": "/FULL/PATH/TO/YOUR/.venv/bin/python",
      "args": [
        "/FULL/PATH/TO/YOUR/server.py"
      ]
    }
  }
}
```

**Important for Windows users:** Use double backslashes in your paths. For example: `C:\\Users\\john\\mcp-masterclass\\lesson-05\\.venv\\Scripts\\python.exe`

Save the file and completely quit Claude Desktop. Don't just close the window, actually quit the application entirely. On macOS, press Cmd+Q. On Windows, right-click the system tray icon and choose Quit. Then restart Claude Desktop fresh.

### Step 6: Test Your MCP Server

After restarting Claude Desktop, start a new conversation. Look at the bottom right corner of the message input area. You should see a hammer icon. Click it and verify that you see the note-reader server listed with the read_note tool available.

Now ask Claude to use your tool. Try this message:

> "Can you use the read_note tool to read rules.txt?"

Claude will ask for permission to use the tool. Click "Allow for This Chat" and watch as your MCP server runs in the background, reads the file, and returns the content to Claude. You just successfully built and deployed your first MCP server.

## 🧪 Experiment and Learn

Now that you have a working MCP server, try these experiments to deepen your understanding:

**Create a second note file:** Add a new file called `project_notes.txt` with some different content. Ask Claude to read this new file. You'll see that your tool works with any text file in the folder, not just the sample.

**Ask for summaries:** Instead of just reading the file, ask Claude to read it and then summarize it in one sentence. This shows how Claude uses your tool's output to accomplish more complex tasks.

**Try multiple files:** Ask Claude to "read both rules.txt and pricing.txt and compare them." Watch it call your tool twice in one conversation to gather everything it needs.

**Break something on purpose:** Change a line in server.py and save it. Restart Claude Desktop and see what happens. Learning to read error messages and debug issues is an essential skill. The troubleshooting section below will help you fix common problems.

## 🔧 Troubleshooting

### The hammer icon doesn't appear in Claude Desktop

This usually means Claude Desktop couldn't connect to your server. Check these things in order:

First, verify you completely quit and restarted Claude Desktop after editing the config file. Just closing the window isn't enough. The application needs to fully restart to load the new configuration.

Second, check your configuration file paths. Open the config file again and verify that the Python path and server.py path are correct and point to actual files on your system. One wrong character in either path will prevent the connection.

Third, try running your Python path in the terminal to verify it works. Copy the exact path from your config file and run it in your terminal. It should start Python without errors.

Fourth, check the Claude Desktop logs for error messages. On macOS, logs are in `~/Library/Logs/Claude/`. On Windows, they're in `%APPDATA%\Claude\logs\`. Look for files with `mcp` in the name and open the most recent one. Error messages here will tell you exactly what went wrong.

### Claude says the file wasn't found

This happens when the file name is wrong, or the file is not where the server expects it. The server looks inside the `notes/` folder that sits next to `server.py`. Make sure your file is in there.

You can check by opening your terminal in the lesson-05 folder and running `ls notes` on macOS or Linux, or `dir notes` on Windows. Your file should be listed.

### The tool appears but crashes when I use it

If the hammer icon shows your server but using the tool produces an error, the server code might have a syntax error or other issue. Try running the server manually to see the full error message.

In your terminal, with the virtual environment active, run:
```bash
python server.py
```

The server should start without printing any errors. It won't print anything at all if it's working correctly, it just waits silently for requests. If you see a Python error or traceback, that tells you what's wrong with the code. Fix the error, save the file, and restart Claude Desktop to try again.

Press Ctrl+C to stop the manually running server.

### Virtual environment issues

If you're having trouble with the virtual environment, make sure you see `(.venv)` at the start of your terminal prompt before running any pip or python commands. If you don't see it, the virtual environment isn't active, and commands will affect your system Python instead of the isolated environment.

To activate it again, run the activation command from Step 2 above. You need to activate the virtual environment every time you open a new terminal window.

## 📚 Understanding the Code

The server.py file is heavily commented to explain how each part works. Open it in your code editor and read through the comments to understand the structure. The key concepts are:

`MCPServer("desk")` creates the server and gives it a name Claude Desktop can see. The `@mcp.tool()` decorator marks a function as something Claude is allowed to call. The type hints on that function become the tool's schema, so there is no JSON to write by hand, and the docstring becomes the description Claude reads when it decides whether to use the tool. `mcp.run(transport="stdio")` starts it and connects it to Claude Desktop. Under SDK version 1 this same server needed separate `list_tools` and `call_tool` handlers plus a hand-written schema, which is why it used to be 165 lines instead of 14.

These same patterns appear in every MCP server you'll build throughout this course. Master them here in Lesson 5, and you'll be ready for the more complex servers in later lessons.

## 🎯 What You Accomplished

You've successfully created your first MCP server, connected it to Claude Desktop, and watched Claude use your custom tool to read local files. This is the foundational pattern that everything else in this course builds upon.

In Lesson 6, you'll extend these concepts to create multi-agent systems where multiple AI agents collaborate through shared MCP servers. The structure you learned here remains the same, you'll just add more sophistication on top of this solid base.

## 💬 Need Help?

If you're stuck and the troubleshooting section didn't help, check the main repository's issues section. Someone else might have encountered the same problem and found a solution. If not, open a new issue describing what's happening, what you expected to happen, and what error messages you're seeing. Include your operating system and Python version to help others help you more effectively.

## ⏭️ Next Steps

Once your MCP server is working perfectly and you've experimented with the suggestions above, you're ready for Lesson 6. Head back to the main repository README to find the link to Lesson 6, or subscribe to the Substack newsletter to be notified when new lessons are published.

The journey from here gets increasingly exciting as you build systems with memory, learning, autonomy, and real-world integrations. Everything you learned in this lesson forms the foundation for all of that.

Happy building!
