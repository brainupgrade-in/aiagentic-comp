# Session 6: LangGraph Stateful Workflows — Hands-on Labs

## Prerequisites

- Session 5 completed (agents & memory working)
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

```bash
cd hands-on/session-6

# Run a lab
python lab01_first_graph.py

# Check the solution
python solutions/lab01_first_graph.py
```

## Tips

- Labs 01-04 are pure Python logic — no API key needed!
- Labs 05-08 use Groq API for LLM-powered nodes
- Read the comments — they explain graph concepts step by step
- Look for `# TODO` markers — that's where you write code
- Run labs frequently to see state changes at each node
- The graph always follows: define state → add nodes → add edges → compile → invoke
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
