# Session 9: Multi-Agent Systems — Hands-on Labs

## Prerequisites

- Session 8 completed (advanced LangGraph patterns working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Required packages installed:

```bash
pip install langgraph langchain-groq langchain-core python-dotenv
```

Verify your setup:
```bash
python -c "from langgraph.graph import StateGraph; print('LangGraph OK')"
python -c "from langgraph.checkpoint.memory import MemorySaver; print('MemorySaver OK')"
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

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-9/
├── lab01_supervisor_worker.ipynb              ← Start here
├── lab02_supervisor_llm.ipynb
├── lab03_peer_to_peer.ipynb
├── lab04_agent_handoffs.ipynb
├── lab05_task_decomposition.ipynb
├── lab06_aggregation_conflict.ipynb
├── lab07_production_patterns.ipynb
├── lab08_challenge.ipynb
└── solutions/                                ← Completed versions
    ├── lab01_supervisor_worker.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the Python kernel (`~/.venv/bin/python`)
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01 and 03 are pure Python logic — no API key needed!
- Labs 02, 04-08 use Groq API for LLM-powered agents
- Session 9 builds on Session 8 patterns (routing, reducers, HITL)
- **Read the markdown cells** — they explain multi-agent concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change agent roles, routing logic, add new workers

## Estimated Time

~60-75 minutes for all labs (including the challenge)
