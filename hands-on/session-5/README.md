# Session 5: LangChain Agents & Memory — Hands-on Labs

## Prerequisites

- Session 4 completed (Groq API working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Required packages installed:

```bash
pip install langchain-groq langchain-core langgraph python-dotenv
```

Verify your setup:
```bash
python -c "from langchain_groq import ChatGroq; print('ChatGroq OK')"
python -c "from langgraph.prebuilt import create_react_agent; print('LangGraph OK')"
python -c "from langchain_core.tools import tool; print('Tools OK')"
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Creating Tools | `@tool` decorator, tool anatomy, docstrings, direct invocation |
| 02 | Your First ReAct Agent | `create_react_agent()`, Think→Act→Observe loop, message trace |
| 03 | Function Calling | `bind_tools()`, structured tool calls, manual tool execution |
| 04 | Multi-Tool Agent | Multiple tools, agent orchestration, complex questions |
| 05 | Conversation Memory | Stateless vs stateful, message lists, multi-turn chat |
| 06 | Memory Strategies | Buffer, window, and summary memory, comparison |
| 07 | Session Management | `MemorySaver`, `thread_id`, multi-user sessions |
| 08 | **Challenge** | Build a complete UniGPS Employee Support Agent |

## How to Run

```bash
cd hands-on/session-5

# Run a lab
python lab01_tools_basics.py

# Check the solution
python solutions/lab01_tools_basics.py
```

## Important: Groq API Key

All labs (except Lab 01 which works without LLM calls) require a Groq API key.

```bash
# Quick check
echo $GROQ_API_KEY
```

If empty, create a `.env` file:
```
GROQ_API_KEY=gsk_your_key_here
```

## Tips

- Read the comments — they explain the *why*, not just the *what*
- Look for `# TODO` markers — that's where you write code
- Run labs frequently to see output at each step
- Lab 01 is tool-only (no API calls) — great for understanding tool anatomy
- Labs 02-04 focus on agents — watch the message traces!
- Labs 05-07 focus on memory — observe how context is preserved
- Lab 08 is the challenge — combine everything
- Compare your work with `solutions/` when you're done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
