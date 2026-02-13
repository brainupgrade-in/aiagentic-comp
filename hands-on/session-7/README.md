# Session 7: LangGraph Stateful Workflows — Hands-on Labs

## Prerequisites

- Session 6 completed (agents & memory working)
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
| 01 | Your First Graph | StateGraph, TypedDict, nodes, edges, START/END | No |
| 02 | Multi-Step Workflow | Chaining nodes, state flow, sequential processing | No |
| 03 | Conditional Routing | `add_conditional_edges()`, branching, routing functions | No |
| 04 | State Reducers | `Annotated[list, add]`, accumulating state, message history | No |
| 05 | Cycles & Retry Logic | Looping edges, retry patterns, max-attempt guards | Yes |
| 06 | Checkpointing | `MemorySaver`, `get_state()`, thread_id, state inspection | Yes |
| 07 | Human-in-the-Loop | `interrupt_before/after`, `update_state()`, resume | Yes |
| 08 | **Challenge** | Build a UniGPS Support Request Workflow | Yes |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-7/
├── lab01_first_graph.ipynb               ← Start here
├── lab02_multi_step_workflow.ipynb
├── lab03_conditional_routing.ipynb
├── lab04_state_reducers.ipynb
├── lab05_cycles_retry.ipynb
├── lab06_checkpointing.ipynb
├── lab07_human_in_loop.ipynb
├── lab08_challenge.ipynb
└── solutions/                            ← Completed versions
    ├── lab01_first_graph.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the Python kernel (`~/.venv/bin/python`)
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01-04 are pure Python logic — no API key needed!
- Labs 05-08 use Groq API for LLM-powered nodes
- **Read the markdown cells** — they explain graph concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- The graph always follows: define state → add nodes → add edges → compile → invoke
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change routing logic, add new nodes, try different state shapes

## Estimated Time

~60-75 minutes for all labs (including the challenge)
