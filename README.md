# MCP Masterclass: Build Connected AI Systems from Scratch

Welcome to the complete code repository for the **MCP Masterclass**, a thirteen-lesson course that takes you from understanding the Model Context Protocol to building autonomous AI systems that can collaborate, remember, learn, and act.

This repository contains all the working code, starter templates, and resources you need to follow along with the course. Each lesson builds on the previous ones, gradually increasing in sophistication until you can design and deploy AI systems that operate with minimal human intervention.

## 📚 About This Course

The MCP Masterclass teaches you how to build AI systems that go beyond simple chat interfaces. You'll learn to create AI applications that can access real data, use custom tools, collaborate with other AI agents, maintain memory across conversations, and execute complex workflows autonomously.

**Who This Course Is For:**
- Developers who want to build practical AI automation systems
- AI enthusiasts curious about how modern AI applications actually work
- Automation engineers looking to level up their skills
- Anyone who wants to understand the infrastructure behind AI agents

**What You'll Build:**
By the end of this course, you'll have built multiple working projects including a local MCP server, a multi-agent research system, AI applications with persistent memory, autonomous execution loops, and integrations with real business tools like Slack and Notion. The final lesson brings everything together into a blueprint for an AI-powered autonomous enterprise.

## 🗺️ Course Structure

The course is organized into four phases, each building naturally on the previous one:

### **Phase 1: Foundation (Lessons 1-4)**

These lessons establish the mental models and core concepts you need to understand MCP deeply.

**Lesson 1: What is MCP?**  
Understand the foundation of the Model Context Protocol and how it acts as the universal remote for AI tools.  
📖 [Read Lesson 1](https://genaiunplugged.substack.com/p/what-is-mcp-model-context-protocol)  
📁 No code for this lesson (conceptual)

**Lesson 2: Why MCP Exists**  
Learn why AI integrations were broken and how MCP simplifies connections from M×N chaos to M+N harmony.  
📖 [Read Lesson 2](https://genaiunplugged.substack.com/p/why-mcp-was-created-full-course-lesson)  
📁 No code for this lesson (conceptual)

**Lesson 3: The Problem MCP Solves**  
See how MCP gives AI the power to act, turning passive models into proactive systems.  
📖 [Read Lesson 3](https://genaiunplugged.substack.com/p/inside-mcp-how-hosts-clients-and)  
📁 No code for this lesson (conceptual)

**Lesson 4: Inside the MCP Architecture**  
Get clarity on the Host-Client-Server model, the core structure behind every MCP-based workflow.  
📖 [Read Lesson 4](https://genaiunplugged.substack.com/p/the-three-superpowers-of-mcp-tools)  
📁 No code for this lesson (conceptual)

### **Phase 2: First Hands-On Project (Lesson 5)**

This is where theory becomes practice. You'll build your first working MCP server and see it in action.

**Lesson 5: Build Your First MCP Server with Claude Desktop**  
Step-by-step tutorial to create your own MCP server that Claude Desktop can use to read local files.  
📖 [Read Lesson 5](YOUR_SUBSTACK_LESSON_5_URL) *(Coming Soon)* 
📁 Code: [`/lesson-05`](./lesson-05) *(Coming Soon)* 

### **Phase 3: Advanced Concepts (Lessons 6-10)**

These lessons take you from simple tools to sophisticated AI systems with collaboration, memory, learning, and autonomy.

**Lesson 6: Multi-Agent Collaboration with MCP**  
Discover how multiple AI agents can work together like departments in a company, communicating through one protocol.  
📖 [Read Lesson 6](YOUR_SUBSTACK_LESSON_6_URL) *(Coming Soon)*  
📁 Code: [`/lesson-06`](./lesson-06) *(Coming Soon)*

**Lesson 7: Adding Shared Memory**  
Teach your AI to remember by storing outcomes, summaries, and history across runs.  
📖 Read Lesson 7 *(Coming Soon)*  
📁 Code: `/lesson-07` *(Coming Soon)*

**Lesson 8: Continuous Learning Systems**  
Move beyond memory and let your AI learn from mistakes and evolve automatically.  
📖 Read Lesson 8 *(Coming Soon)*  
📁 Code: `/lesson-08` *(Coming Soon)*

**Lesson 9: Goal Management & Planning**  
Give your AI the ability to set, prioritize, and manage goals without human prompting.  
📖 Read Lesson 9 *(Coming Soon)*  
📁 Code: `/lesson-09` *(Coming Soon)*

**Lesson 10: Autonomous Execution Loops**  
Build self-running loops that plan, act, and reflect with no manual triggers required.  
📖 Read Lesson 10 *(Coming Soon)*  
📁 Code: `/lesson-10` *(Coming Soon)*

### **Phase 4: Real-World Integration & Capstone (Lessons 11-13)**

The final phase connects your AI systems to actual business tools and brings everything together.

**Lesson 11: Connecting to Real Business Tools**  
Integrate your AI with Slack, Notion, CRMs, and databases safely through MCP.  
📖 Read Lesson 11 *(Coming Soon)*  
📁 Code: `/lesson-11` *(Coming Soon)*

**Lesson 12: Event Triggers & Real-Time Actions**  
Enable real-time reactions so your AI responds instantly to external events.  
📖 Read Lesson 12 *(Coming Soon)*  
📁 Code: `/lesson-12` *(Coming Soon)*

**Lesson 13: The Autonomous Enterprise Loop**  
Combine memory, planning, and action into one closed loop, the blueprint of an AI-run enterprise.  
📖 Read Lesson 13 *(Coming Soon)*  
📁 Code: `/lesson-13` *(Coming Soon)*

## 🚀 Getting Started

### **Prerequisites**

Before you begin, make sure you have the following:

**Technical Skills:**
- Basic Python programming knowledge (variables, functions, async/await)
- Comfort using the terminal or command line
- Familiarity with text editors or IDEs like VS Code or Cursor
- Willingness to experiment, debug, and learn from errors

**Software Requirements:**
- Python 3.10 or higher installed on your system
- Claude Desktop application (free download from [claude.ai](https://claude.ai/download))
- A code editor (VS Code, Cursor, PyCharm, or similar)
- Git installed for cloning this repository

**API Access (for some lessons):**
- A Claude account (free or paid) for using Claude Desktop
- Optional: OpenAI API key if you want to experiment with GPT models

**Important Note:** This course uses Claude Desktop as the MCP Host for simplicity and immediate results. All the patterns you learn work with any MCP-compatible host, but starting with Claude Desktop means you can see your code working in a real AI application right away.

### **Quick Setup**

Follow these steps to get your environment ready for the course:

**Step 1: Clone This Repository**

Open your terminal and run the following command to download all the course materials to your computer:
```bash
git clone https://github.com/genaiunplugged14/mcp-masterclass.git
cd mcp-masterclass
```

**Step 2: Install Claude Desktop**

If you haven't already, download and install Claude Desktop from [claude.ai/download](https://claude.ai/download). Choose the version for your operating system, whether macOS or Windows. Install the application and sign in with your Claude account. You'll use this as your MCP Host throughout the course.

**Step 3: Set Up Python Environment**

Each lesson has its own folder with its own Python environment. When you're ready to start a lesson, navigate to that lesson's folder and follow the setup instructions in its README file. For example, when you reach Lesson 5, you would run these commands:
```bash
cd lesson-05
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The lesson-specific README will guide you through any additional setup steps needed for that particular project.

**Step 4: Start with Lesson 5**

Lessons 1 through 4 are conceptual and don't require code. Read those lessons on Substack to build your understanding of MCP, then come back here when you're ready to start building in Lesson 5. The Lesson 5 folder contains complete working code, setup instructions, and troubleshooting tips to get you started with hands-on MCP development.

## 📂 Repository Structure

Here's how the code is organized to make navigation easy:
```
mcp-masterclass/
├── README.md                  # This file - your course hub
├── lesson-01/                 # Links and notes for Lesson 1
├── lesson-02/                 # Links and notes for Lesson 2
├── lesson-03/                 # Links and notes for Lesson 3
├── lesson-04/                 # Links and notes for Lesson 4
├── lesson-05/                 # First hands-on project
│   ├── README.md             # Setup instructions
│   ├── server.py             # Complete MCP server
│   ├── sample_note.txt       # Example data file
│   ├── check_setup.py        # Environment verification
│   └── requirements.txt      # Python dependencies
├── lesson-06/                 # Multi-agent collaboration (coming soon)
├── lesson-07/                 # Shared memory systems (coming soon)
├── lesson-08/                 # Continuous learning (coming soon)
├── lesson-09/                 # Goal management (coming soon)
├── lesson-10/                 # Autonomous loops (coming soon)
├── lesson-11/                 # Business tool integration (coming soon)
├── lesson-12/                 # Event triggers (coming soon)
├── lesson-13/                 # Autonomous enterprise (coming soon)
└── starter-kit/               # Reusable templates (coming soon)
    ├── base-server/          # Template for new MCP servers
    ├── common-tools/         # Frequently used tool implementations
    └── utilities/            # Helper functions and utilities
```

Each lesson folder that contains code has its own README with specific setup instructions, explanations of what the code does, and troubleshooting guidance for common issues. You can explore any lesson's code at any time, though working through them sequentially will give you the best learning experience.

## 💡 How to Use This Repository

This repository is designed to support your learning in several ways, and you can use it however works best for your learning style.

**As a Reference:** If you get stuck while following along with a lesson, you can check the repository code to see a working implementation. Sometimes comparing your code to a working version helps you spot the issue quickly.

**As a Starting Point:** Some lessons will reference starter templates in the repository that you can copy and modify. This lets you focus on learning the new concepts rather than rewriting boilerplate code you've already seen.

**As a Sandbox:** Feel free to experiment with the code in this repository. Try modifying tools, adding new features, or combining concepts from different lessons. The best learning often happens when you break things and figure out how to fix them.

**As a Portfolio:** Once you've completed the course, the projects in this repository become part of your portfolio. You can fork this repository, customize the projects, and showcase what you've built to potential employers or collaborators.

## 🤝 Contributing

Found a bug in the code or a typo in a README? Have an improvement suggestion or a better way to explain something? Contributions are welcome and appreciated.

Please open an issue if you encounter problems or have questions. You can also submit a pull request if you've fixed something or want to contribute an enhancement. Just make sure to explain what your change does and why it's helpful.

If you build something cool using the patterns from this course, consider sharing it in the discussions section. Seeing what others create helps everyone learn and get inspired.

## 📬 Stay Connected

This course is published as a series on Substack where each lesson is explained in detail with clear analogies, step-by-step instructions, and real-world context.

**Subscribe to the newsletter:** [https://genaiunplugged.substack.com/]  
You'll get notified when new lessons are published and receive bonus content that doesn't appear in the repository.

**Follow me on LinkedIn:** [https://www.linkedin.com/in/dheerajsharma14/]
**Subscribe to my YouTube channel:** [https://www.youtube.com/@genaiunplugged]


## 📄 License

This repository and all its code are provided for educational purposes. You're free to use, modify, and build upon this code for your own projects. If you share or publish work based on these lessons, a link back to the original course is appreciated but not required.

The goal is to help you learn and build amazing things with MCP. Take these patterns, make them your own, and create something that solves real problems for real people.

## 🙏 Acknowledgments

This course builds on the Model Context Protocol developed by Anthropic. The MCP specification and SDK make it possible to create these kinds of connected AI systems, and this course aims to make that technology accessible to everyone who wants to learn.

Special thanks to the students and readers who provide feedback, catch errors, and share their own implementations. Your engagement makes this course better for everyone who comes after you.

---

**Ready to start building?** Head to [Lesson 5](./lesson-05) to create your first MCP server, or read [Lesson 1](https://genaiunplugged.substack.com/p/what-is-mcp-model-context-protocol) if you're new to the course and want to start from the beginning.

Happy building! 🚀
