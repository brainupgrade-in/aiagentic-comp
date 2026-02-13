# Session 8: Advanced LangGraph Workflows — Hands-on Labs

## Prerequisites

- Session 7 completed (LangGraph fundamentals working)
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
| 01 | Multi-Branch Workflows | Fan-out, convergence, parallel paths | No |
| 02 | Parallel Execution | Parallel nodes with reducers, merge patterns | No |
| 03 | Custom Reducers | Sliding window, merge dicts, take max, add_messages | No |
| 04 | Error Handling | Errors in state, error-aware routing, fallback nodes | Yes |
| 05 | Retry with Backoff | Retry cycles, exponential backoff, max-attempt guards | Yes |
| 06 | Advanced Routing | Nested conditionals, LLM-powered routing, priority routing | Yes |
| 07 | Advanced Human-in-the-Loop | Multi-gate approvals, user input collection, timeout | Yes |
| 08 | **Challenge** | Production-Grade UniGPS Expense Approval System | Yes |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-8/
├── lab01_multi_branch.ipynb              ← Start here
├── lab02_parallel_execution.ipynb
├── lab03_custom_reducers.ipynb
├── lab04_error_handling.ipynb
├── lab05_retry_backoff.ipynb
├── lab06_advanced_routing.ipynb
├── lab07_advanced_hitl.ipynb
├── lab08_challenge.ipynb
└── solutions/                            ← Completed versions
    ├── lab01_multi_branch.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the Python kernel (`~/.venv/bin/python`)
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01-03 are pure Python logic — no API key needed!
- Labs 04-08 use Groq API for LLM-powered nodes
- Session 8 builds on Session 7 — review if needed
- **Read the markdown cells** — they explain graph concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change routing logic, add new nodes, try different state shapes

## Estimated Time

~60-75 minutes for all labs (including the challenge)
