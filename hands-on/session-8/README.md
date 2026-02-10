# Session 8: Multi-Agent Systems — Hands-on Labs

## Prerequisites

- Session 7 completed (advanced LangGraph patterns working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Required packages installed:

```bash
pip install langgraph langchain-groq langchain-core python-dotenv
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs API? |
|-----|-------|-------------------|------------|
| 01 | Supervisor/Worker Basics | Central routing, specialized workers, state flow | No |
| 02 | Supervisor with LLM Routing | LLM-powered supervisor, dynamic worker selection | Yes |
| 03 | Peer-to-Peer Collaboration | Shared state, turn-based agents, iterative refinement | No |
| 04 | Agent Handoffs | Explicit handoff, context transfer, escalation chains | Yes |
| 05 | Task Decomposition | Breaking tasks into sub-tasks, parallel worker execution | Yes |
| 06 | Result Aggregation & Conflict | Merging outputs, voting, arbitrator pattern | Yes |
| 07 | Production Patterns | Specialization, fallback chains, audit trails | Yes |
| 08 | **Challenge** | Complete UniGPS Multi-Agent Support System | Yes |

## How to Run

```bash
cd hands-on/session-8

# Run a lab
python lab01_supervisor_worker.py

# Check the solution
python solutions/lab01_supervisor_worker.py
```

## Tips

- Labs 01 and 03 are pure Python logic — no API key needed!
- Labs 02, 04-08 use Groq API for LLM-powered agents
- Session 8 builds on Session 7 patterns (routing, reducers, HITL)
- Look for `# TODO` markers — that's where you write code
- Each lab has 2 TODOs with commented starter code
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
