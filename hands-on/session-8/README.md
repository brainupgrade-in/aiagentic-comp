# Session 8: Advanced LangGraph Workflows — Hands-on Labs

## Prerequisites

- Session 7 completed (LangGraph fundamentals working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Required packages installed:

```bash
pip install langgraph langchain-groq langchain-core python-dotenv
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

```bash
cd hands-on/session-8

# Run a lab
python lab01_multi_branch.py

# Check the solution
python solutions/lab01_multi_branch.py
```

## Tips

- Labs 01-03 are pure Python logic — no API key needed!
- Labs 04-08 use Groq API for LLM-powered nodes
- Session 8 builds on Session 7 — review if needed
- Look for `# TODO` markers — that's where you write code
- Each lab has 2 TODOs with commented starter code
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
