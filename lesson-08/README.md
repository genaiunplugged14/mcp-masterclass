# Lesson 8: Agent Learning & Experience Memory Systems

This folder contains the complete working code for Lesson 8 of the MCP Masterclass. You'll build agents that learn from their experiences, remember what works, and automatically improve their strategies over time.

## What You'll Build

A learning system where AI agents:
- Track outcomes from every action they take
- Identify patterns in what works and what doesn't
- Store insights that persist across sessions
- Automatically adjust their approaches based on experience
- Share learning between different specialized agents

## Prerequisites

Before starting this lesson, make sure you've completed:
- Lesson 5 (Basic MCP server implementation)
- Lesson 6 (Multi-agent collaboration)
- Lesson 7 (Shared memory systems)

You should be comfortable with:
- Running Python MCP servers
- Configuring Claude Desktop
- Using multiple agent conversations
- Basic JSON data structures

## Quick Start

### 1. Set Up Your Environment

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

Run the setup verification script:

```bash
python check_setup.py
```

You should see success messages confirming all MCP components are installed.

### 3. Configure Claude Desktop

Edit your Claude Desktop config file (see `claude_desktop_config.json.example` for the template):

**On macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**On Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

Add this configuration (replace paths with your actual paths):

```json
{
  "mcpServers": {
    "learning-agent": {
      "command": "/FULL/PATH/TO/YOUR/.venv/bin/python",
      "args": [
        "/FULL/PATH/TO/YOUR/server.py"
      ]
    }
  }
}
```

**Important for Windows:** Use double backslashes in paths, for example:
```
C:\\Users\\yourname\\mcp-masterclass\\lesson-08\\.venv\\Scripts\\python.exe
```

### 4. Restart Claude Desktop

Completely quit and restart Claude Desktop for the configuration to take effect.

## How to Use the Learning System

### Testing the Learning Agent

Start a new conversation in Claude Desktop and try this:

```
You are a Research Agent that learns from experience.

Use the record_experience tool to track the outcome of this research task:
- Research topic: "Benefits of morning routines"
- Strategy used: "Focus on scientific studies first"
- Result: "Found 5 peer-reviewed studies, high-quality data"

Then use get_learning_insights to see what patterns you should follow.
```

Watch as the agent:
1. Records its experience
2. Retrieves past learning insights
3. Adjusts its approach based on patterns

### Creating Multiple Learning Agents

**Content Researcher Agent:**
```
You are a Content Researcher who learns from experience. 
Before starting any research, use get_learning_insights to see what approaches have worked best.
After completing research, use record_experience to track the outcome.
Always learn from patterns and adjust your strategy.
```

**Writer Agent:**
```
You are a Writer who learns from experience.
Before writing, check get_learning_insights to see what writing styles have been most effective.
After completing content, use record_experience to track engagement and quality metrics.
Continuously improve based on what works.
```

### Example Learning Workflow

1. **Initial Task (No Prior Learning):**
   ```
   Research "productivity tips" and save findings.
   Strategy: Start with general Google search.
   Outcome: Found surface-level content, low depth.
   ```

2. **Record the Experience:**
   ```
   record_experience(
     task="productivity research",
     approach="general search",
     outcome="low depth",
     success=false
   )
   ```

3. **Next Task (Learning Applied):**
   ```
   Before researching "time management," check insights.
   Insight found: "General searches produce low depth - prioritize academic sources."
   New strategy: Start with Google Scholar and peer-reviewed studies.
   Outcome: High-quality, evidence-based content.
   ```

4. **Record Success:**
   ```
   record_experience(
     task="time management research",
     approach="academic sources first",
     outcome="high quality evidence-based",
     success=true
   )
   ```

5. **Pattern Emerges:**
   After 3-4 research tasks, the system identifies:
   "Academic sources consistently produce higher quality than general searches."
   This insight automatically guides future research.

## The Learning Tools

### 1. record_experience

**Purpose:** Tracks what happened when an agent tried something

**Parameters:**
- `agent_id` (string): Name of the agent (e.g., "researcher", "writer")
- `task_type` (string): Category of task (e.g., "research", "writing", "analysis")
- `context` (string): What the agent was trying to do
- `approach` (string): Strategy or method used
- `outcome` (string): What actually happened
- `success` (boolean): Whether it worked well
- `metrics` (object, optional): Quantitative measures (time, quality score, etc.)

**Example:**
```python
record_experience(
    agent_id="content-researcher",
    task_type="research",
    context="Finding statistics about remote work",
    approach="Started with government data sources",
    outcome="Found authoritative, recent statistics",
    success=True,
    metrics={"sources_found": 8, "quality_score": 9}
)
```

### 2. get_learning_insights

**Purpose:** Retrieves patterns and recommendations based on past experiences

**Parameters:**
- `agent_id` (string, optional): Get insights for specific agent, or all agents if omitted
- `task_type` (string, optional): Filter to specific type of task
- `min_confidence` (number, optional): Minimum pattern strength (0-1), defaults to 0.7

**Returns:** 
- Patterns identified from past experiences
- Success/failure rates for different approaches
- Specific recommendations for improvement

**Example:**
```python
get_learning_insights(
    agent_id="content-researcher",
    task_type="research",
    min_confidence=0.75
)

# Returns insights like:
# "Academic sources have 90% success rate (9/10 attempts)"
# "General web searches have 30% success rate (3/10 attempts)"
# "Recommendation: Prioritize academic sources for research tasks"
```

### 3. analyze_learning_patterns

**Purpose:** Provides deeper analysis of learning trends

**Parameters:**
- `agent_id` (string, optional): Analyze specific agent or all
- `time_range_days` (number, optional): Look back N days, defaults to 30

**Returns:**
- Success rate trends over time
- Most effective strategies
- Areas needing improvement
- Confidence levels in recommendations

**Example:**
```python
analyze_learning_patterns(
    agent_id="writer",
    time_range_days=14
)

# Returns analysis like:
# "Writing style 'conversational with examples' shows 85% success"
# "Listicle format has declining effectiveness (was 80%, now 60%)"
# "Recommend experimenting with story-driven openings"
```

## File Structure

```
lesson-08/
├── README.md                           # This file
├── server.py                          # Complete MCP server with learning tools
├── requirements.txt                   # Python dependencies
├── check_setup.py                     # Verify installation
├── claude_desktop_config.json.example # Configuration template
├── learning_data.json                 # Stores experiences (auto-generated)
└── examples/
    ├── researcher_agent_example.txt   # Example conversation for researcher
    └── writer_agent_example.txt       # Example conversation for writer
```

## Understanding the Learning System

### How Learning Works

1. **Experience Recording:** Every time an agent completes a task, it records:
   - What it was trying to do (context)
   - How it approached the task (strategy)
   - What happened (outcome)
   - Whether it worked (success/failure)

2. **Pattern Detection:** The system analyzes recorded experiences to find:
   - Which approaches consistently succeed
   - Which strategies consistently fail
   - Conditions that affect outcomes

3. **Insight Generation:** Patterns become actionable insights:
   - "Approach X works 90% of the time for task Y"
   - "Strategy Z consistently fails when condition W is present"

4. **Automatic Improvement:** Agents query insights before acting:
   - Check what worked in similar situations
   - Adjust strategy based on patterns
   - Try new approaches when old ones plateau

### The Learning Loop

```
Task → Strategy Decision (check insights) 
     → Execute (try approach)
     → Record Experience (what happened)
     → Update Patterns (learn from outcome)
     → [Loop repeats with improved strategy]
```

### Why This Matters

Traditional AI agents start fresh every time. They make the same mistakes repeatedly because they don't remember what didn't work.

Learning agents:
- Build expertise over time
- Avoid repeating failures
- Automatically optimize their approaches
- Share learning across similar tasks
- Get better without your intervention

This is the foundation for truly autonomous systems.

## Troubleshooting

### Tool not appearing in Claude Desktop

1. Verify your config file paths are correct (use absolute paths)
2. Make sure you completely quit and restarted Claude Desktop
3. Check the hammer icon (🔨) in Claude Desktop to see connected servers
4. Look for the `learning-agent` server in the list

### Learning data not persisting

1. Check that `learning_data.json` was created in the lesson-08 folder
2. Verify the server has write permissions to the directory
3. Make sure you're using the same server configuration between sessions

### Insights not appearing

1. Record at least 3-5 experiences before expecting strong patterns
2. Lower the `min_confidence` parameter if patterns are weak
3. Check that `success` flags are set correctly in recorded experiences
4. Verify `task_type` categories match between recording and retrieval

### Performance issues

1. The system stores unlimited experiences by default
2. For production use, implement experience pruning (keep last 1000)
3. Consider adding indexing if you have thousands of experiences
4. Use specific `agent_id` and `task_type` filters to speed up queries

## Advanced Usage

### Custom Metrics

Add domain-specific metrics to track:

```python
record_experience(
    agent_id="sales-agent",
    task_type="outreach",
    context="Cold email campaign",
    approach="Personalized with company research",
    outcome="12% response rate",
    success=True,
    metrics={
        "emails_sent": 100,
        "responses": 12,
        "response_rate": 0.12,
        "meetings_booked": 3,
        "time_spent_minutes": 45
    }
)
```

### Multi-Agent Learning

Different agents can learn from each other:

```python
# Writer learns from Researcher's findings
get_learning_insights(
    task_type="content-creation",
    # Pulls patterns from both researcher and writer experiences
)
```

### Confidence Thresholds

Adjust pattern confidence based on risk:

```python
# High-stakes tasks: require strong patterns (0.9)
get_learning_insights(min_confidence=0.9)

# Exploration mode: accept weaker patterns (0.5)
get_learning_insights(min_confidence=0.5)
```

### Time-Based Analysis

Track how strategies evolve:

```python
# Recent learning (last 7 days)
analyze_learning_patterns(time_range_days=7)

# Historical comparison (last 90 days)
analyze_learning_patterns(time_range_days=90)
```

## What's Next

In Lesson 9, you'll add **Goal Management & Planning** to these learning agents. They'll be able to:
- Set their own goals based on what they've learned
- Break complex objectives into steps
- Autonomously work toward multi-step outcomes
- Adjust plans based on experience

Learning makes agents better at executing tasks. Goals make them capable of managing entire projects.

## Full Course

This is Lesson 8 of the MCP Masterclass. For the complete course:
- [Course Overview](YOUR_COURSE_URL)
- [Previous Lesson: Shared Memory](YOUR_LESSON_7_URL)
- [Next Lesson: Goal Management](YOUR_LESSON_9_URL)

All code is available in the [MCP Masterclass GitHub Repository](YOUR_GITHUB_REPO_URL).

## Getting Help

If you get stuck:
1. Check the troubleshooting section above
2. Review the example conversations in the `examples/` folder
3. Compare your code to the working version in this repository
4. Ask questions in the course community (link in main README)

## License

MIT License - Feel free to use this code for learning and building your own projects.
