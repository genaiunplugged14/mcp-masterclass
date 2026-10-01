# Conversation Templates for Memory-Enabled Agents

These templates show how to prompt agents to use memory effectively.

## Researcher Agent with Memory

Use this prompt in a Claude Desktop conversation:
```
You are a research specialist with memory capabilities.

BEFORE starting any research:
1. Use the read_memory tool to check what you already know about this topic
2. Review past findings and build on them instead of starting from scratch
3. Note which sources were valuable before

AFTER completing research:
1. Use save_memory to store:
   - Key insights discovered
   - Valuable sources found
   - What approaches worked well
   - What to avoid next time
2. Be specific so future research can build on this

Your task: [INSERT YOUR RESEARCH TASK HERE]

Remember: Check memory first, then research, then save what you learned.
```

## Writer Agent with Memory

Use this prompt in a **separate** Claude Desktop conversation:
```
You are a professional writer with memory capabilities.

BEFORE starting any writing:
1. Use read_memory to check:
   - Past writing style preferences
   - Successful article structures
   - Reader feedback from previous work
   - Common mistakes to avoid
2. Use search_memory if looking for something specific

AFTER completing writing:
1. Use save_memory to store:
   - What writing patterns worked well
   - Structure that felt effective
   - Tone and style choices made
   - Any feedback or insights

Your task: [INSERT YOUR WRITING TASK HERE]

Remember: Read memory for context, write the content, save what you learned.
```

## Editor Agent with Memory (Bonus)

Add a third agent for quality control:
```
You are an editorial specialist with memory capabilities.

BEFORE reviewing content:
1. Use read_memory to check:
   - Common quality issues from past reviews
   - Style guide preferences
   - Reader feedback patterns

AFTER reviewing:
1. Use save_memory to store:
   - Recurring issues found
   - Quality improvements suggested
   - Patterns in what makes content strong
   - Editorial preferences discovered

Your task: Review the content and provide editorial feedback.

Remember: Check past editorial notes, review carefully, save quality insights.
```

## Tips for Better Memory Usage

### For Researchers

Save memories like this:
```
"Research completed on [topic]. 
Best sources: [list 2-3 valuable sources].
Key insight: [main finding].
Approach that worked: [what was effective].
To avoid next time: [what wasted time]."
```

### For Writers

Save memories like this:
```
"Article completed on [topic].
Structure used: [outline approach].
Style choice: [tone and voice].
What resonated: [feedback or effectiveness].
To improve: [areas for growth]."
```

### For Editors

Save memories like this:
```
"Editorial review completed.
Common issue found: [pattern noticed].
Quality improvement: [suggestion made].
Strong element: [what worked well].
Style note: [preference discovered]."
```

## Example Workflow

**Day 1:**
1. Researcher: "Research programming languages" → saves findings
2. Writer: Reads researcher's memories → writes article → saves style notes

**Day 2:**
3. Researcher: "Research web frameworks" → reads past memories → builds on previous language research → 2x faster
4. Writer: Reads all memories → applies successful patterns → writes better article

**Day 3:**
5. Editor: Reviews Day 2 article → saves quality feedback
6. Writer: Reads editorial notes → applies improvements to next article

Each iteration compounds learning from all previous work.

## Troubleshooting Agent Behavior

**If agents aren't using memory:**
- Make sure you explicitly instruct them to use the tools
- Start prompts with "BEFORE starting..." to establish the pattern
- Confirm they have permission to use tools (click Allow when prompted)

**If memory isn't helpful:**
- Encourage agents to be more specific when saving
- Ask them to save actionable insights, not just facts
- Have them note "what to do differently next time"

**If memory is too cluttered:**
- Use search_memory instead of read_memory for focused retrieval
- Periodically review and summarize key patterns
- Consider starting fresh memory for different project types

The key is establishing the habit: Read before starting, save after completing. Once that pattern is set, agents naturally improve over time.