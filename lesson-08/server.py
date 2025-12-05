"""
MCP Server: Agent Learning & Experience Memory System

This server provides tools for AI agents to learn from their experiences,
identify patterns in what works, and automatically improve their strategies.

Tools provided:
1. record_experience - Track outcomes from agent actions
2. get_learning_insights - Retrieve patterns and recommendations
3. analyze_learning_patterns - Deep analysis of learning trends

Lesson 8 of the MCP Masterclass
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Storage file for experiences
LEARNING_DATA_FILE = "learning_data.json"

def load_experiences():
    """Load all recorded experiences from storage"""
    if not os.path.exists(LEARNING_DATA_FILE):
        return []
    
    try:
        with open(LEARNING_DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_experiences(experiences):
    """Save experiences to storage"""
    try:
        with open(LEARNING_DATA_FILE, 'w') as f:
            json.dump(experiences, f, indent=2)
        return True
    except IOError:
        return False

def calculate_success_rate(experiences):
    """Calculate success rate from a list of experiences"""
    if not experiences:
        return 0.0
    
    successful = sum(1 for exp in experiences if exp.get('success', False))
    return successful / len(experiences)

def identify_patterns(experiences, min_confidence=0.7):
    """
    Identify patterns in experiences
    
    Returns insights about which approaches work and which don't
    """
    if len(experiences) < 3:
        return {
            "insights": [],
            "message": "Need at least 3 experiences to identify patterns"
        }
    
    # Group by approach
    approach_outcomes = defaultdict(list)
    for exp in experiences:
        approach = exp.get('approach', 'unknown')
        approach_outcomes[approach].append(exp)
    
    insights = []
    
    for approach, exps in approach_outcomes.items():
        if len(exps) < 2:
            continue  # Need multiple attempts to establish pattern
        
        success_rate = calculate_success_rate(exps)
        confidence = min(1.0, len(exps) / 5)  # Confidence increases with more data
        
        if confidence >= min_confidence:
            insight = {
                "approach": approach,
                "success_rate": round(success_rate, 2),
                "attempts": len(exps),
                "confidence": round(confidence, 2),
                "recommendation": "use" if success_rate > 0.7 else "avoid"
            }
            insights.append(insight)
    
    # Sort by success rate
    insights.sort(key=lambda x: x['success_rate'], reverse=True)
    
    return {
        "insights": insights,
        "total_experiences": len(experiences)
    }

# Initialize MCP server
server = Server("learning-agent")

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools"""
    return [
        Tool(
            name="record_experience",
            description=(
                "Record an agent's experience for learning purposes. "
                "Tracks what the agent tried, what happened, and whether it worked. "
                "This builds a knowledge base that agents can learn from over time."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Identifier for the agent (e.g., 'researcher', 'writer')"
                    },
                    "task_type": {
                        "type": "string",
                        "description": "Category of task (e.g., 'research', 'writing', 'analysis')"
                    },
                    "context": {
                        "type": "string",
                        "description": "What the agent was trying to accomplish"
                    },
                    "approach": {
                        "type": "string",
                        "description": "The strategy or method the agent used"
                    },
                    "outcome": {
                        "type": "string",
                        "description": "What actually happened / the result"
                    },
                    "success": {
                        "type": "boolean",
                        "description": "Whether the approach worked well (true) or not (false)"
                    },
                    "metrics": {
                        "type": "object",
                        "description": "Optional quantitative metrics (time, quality score, etc.)",
                        "additionalProperties": True
                    }
                },
                "required": ["agent_id", "task_type", "context", "approach", "outcome", "success"]
            }
        ),
        Tool(
            name="get_learning_insights",
            description=(
                "Retrieve learning insights and patterns based on past experiences. "
                "Agents use this before taking action to see what has worked well previously. "
                "Returns patterns, success rates, and recommendations."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Optional: filter to specific agent's experiences"
                    },
                    "task_type": {
                        "type": "string",
                        "description": "Optional: filter to specific task type"
                    },
                    "min_confidence": {
                        "type": "number",
                        "description": "Minimum pattern confidence (0-1), defaults to 0.7",
                        "minimum": 0,
                        "maximum": 1
                    }
                }
            }
        ),
        Tool(
            name="analyze_learning_patterns",
            description=(
                "Provides deeper analysis of learning trends over time. "
                "Shows success rate evolution, most effective strategies, "
                "and areas needing improvement."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "agent_id": {
                        "type": "string",
                        "description": "Optional: analyze specific agent or all agents"
                    },
                    "time_range_days": {
                        "type": "number",
                        "description": "Number of days to look back, defaults to 30",
                        "minimum": 1,
                        "maximum": 365
                    }
                }
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    
    if name == "record_experience":
        # Load existing experiences
        experiences = load_experiences()
        
        # Create new experience record
        new_experience = {
            "timestamp": datetime.now().isoformat(),
            "agent_id": arguments["agent_id"],
            "task_type": arguments["task_type"],
            "context": arguments["context"],
            "approach": arguments["approach"],
            "outcome": arguments["outcome"],
            "success": arguments["success"],
            "metrics": arguments.get("metrics", {})
        }
        
        # Add to collection
        experiences.append(new_experience)
        
        # Save back to storage
        if save_experiences(experiences):
            result = {
                "status": "recorded",
                "experience_id": len(experiences),
                "total_experiences": len(experiences),
                "message": f"Experience recorded for {arguments['agent_id']} on {arguments['task_type']} task"
            }
        else:
            result = {
                "status": "error",
                "message": "Failed to save experience to storage"
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "get_learning_insights":
        # Load experiences
        experiences = load_experiences()
        
        # Apply filters
        filtered = experiences
        
        if "agent_id" in arguments and arguments["agent_id"]:
            filtered = [e for e in filtered if e.get("agent_id") == arguments["agent_id"]]
        
        if "task_type" in arguments and arguments["task_type"]:
            filtered = [e for e in filtered if e.get("task_type") == arguments["task_type"]]
        
        # Get minimum confidence threshold
        min_confidence = arguments.get("min_confidence", 0.7)
        
        # Identify patterns
        patterns = identify_patterns(filtered, min_confidence)
        
        # Format insights for readability
        if patterns["insights"]:
            result = {
                "status": "success",
                "total_experiences_analyzed": patterns["total_experiences"],
                "patterns_found": len(patterns["insights"]),
                "insights": patterns["insights"]
            }
        else:
            result = {
                "status": "insufficient_data",
                "message": patterns.get("message", "No strong patterns found yet"),
                "total_experiences_analyzed": patterns["total_experiences"],
                "suggestion": "Record more experiences to build stronger patterns"
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "analyze_learning_patterns":
        # Load experiences
        experiences = load_experiences()
        
        # Apply agent filter if specified
        if "agent_id" in arguments and arguments["agent_id"]:
            experiences = [e for e in experiences if e.get("agent_id") == arguments["agent_id"]]
        
        # Apply time range filter
        time_range_days = arguments.get("time_range_days", 30)
        cutoff_date = datetime.now() - timedelta(days=time_range_days)
        
        filtered_experiences = []
        for exp in experiences:
            try:
                exp_date = datetime.fromisoformat(exp.get("timestamp", ""))
                if exp_date >= cutoff_date:
                    filtered_experiences.append(exp)
            except (ValueError, TypeError):
                continue
        
        if not filtered_experiences:
            result = {
                "status": "no_data",
                "message": f"No experiences found in the last {time_range_days} days"
            }
        else:
            # Calculate overall success rate
            overall_success = calculate_success_rate(filtered_experiences)
            
            # Group by task type
            task_type_stats = defaultdict(list)
            for exp in filtered_experiences:
                task_type = exp.get("task_type", "unknown")
                task_type_stats[task_type].append(exp)
            
            task_analysis = {}
            for task_type, exps in task_type_stats.items():
                task_analysis[task_type] = {
                    "attempts": len(exps),
                    "success_rate": round(calculate_success_rate(exps), 2)
                }
            
            # Identify best and worst approaches
            all_patterns = identify_patterns(filtered_experiences, min_confidence=0.5)
            
            best_approaches = [
                p for p in all_patterns.get("insights", [])
                if p["success_rate"] > 0.7
            ][:3]  # Top 3
            
            worst_approaches = [
                p for p in all_patterns.get("insights", [])
                if p["success_rate"] < 0.4
            ][:3]  # Bottom 3
            
            result = {
                "status": "success",
                "time_range_days": time_range_days,
                "total_experiences": len(filtered_experiences),
                "overall_success_rate": round(overall_success, 2),
                "task_type_breakdown": task_analysis,
                "best_approaches": best_approaches,
                "worst_approaches": worst_approaches,
                "recommendation": (
                    "Continue using best approaches and avoid worst approaches. "
                    "Consider experimenting with new strategies in low-risk scenarios."
                )
            }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
