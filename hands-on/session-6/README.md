# Session 6: LangChain Agents & Memory — Hands-on Labs

## Prerequisites

- Session 5 completed (Groq API working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Setup complete (`source scripts/setup.sh` — installs everything for all 5 days)

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

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-6/
├── lab01_tools_basics.ipynb              ← Start here
├── lab02_react_agent.ipynb
├── lab03_function_calling.ipynb
├── lab04_multi_tool_agent.ipynb
├── lab05_conversation_memory.ipynb
├── lab06_memory_strategies.ipynb
├── lab07_session_management.ipynb
├── lab08_challenge.ipynb
└── solutions/                            ← Completed versions
    ├── lab01_tools_basics.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

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

- **Read the markdown cells** — each lab explains what's happening step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Lab 01 is tool-only (no API calls) — great for understanding tool anatomy
- Labs 02-04 focus on agents — watch the message traces!
- Labs 05-07 focus on memory — observe how context is preserved
- Lab 08 is the challenge — combine everything
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change prompts, add new tools, try different memory strategies

## Estimated Time

~60-75 minutes for all labs (including the challenge)
