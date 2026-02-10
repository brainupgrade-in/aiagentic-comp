# Session 9: Production Application Development — Hands-on Labs

## Prerequisites

- Session 8 completed (multi-agent patterns working)
- `.env` file with `GROQ_API_KEY` in your working directory
- Required packages installed:

```bash
pip install langgraph langchain-groq langchain-core python-dotenv
pip install fastapi httpx uvicorn pytest
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs API? |
|-----|-------|-------------------|------------|
| 01 | FastAPI Basics | Pydantic models, endpoints, validation, TestClient | No |
| 02 | FastAPI + LangGraph | Agent endpoints, async handling, error responses | Yes |
| 03 | Streaming Responses | SSE streaming, progress events, real-time output | Yes |
| 04 | Unit Testing Nodes | Test routing, formatters, validators without LLM | No |
| 05 | Mocking LLM Calls | unittest.mock.patch, deterministic tests, error paths | No |
| 06 | Integration & API Testing | Full graph tests, TestClient, fallback validation | No |
| 07 | Performance Optimization | Caching, timing, model right-sizing | Yes |
| 08 | **Challenge** | Complete UniGPS Production Agent API | Yes |

## How to Run

```bash
cd hands-on/session-9

# Run a lab
python lab01_fastapi_basics.py

# Check the solution
python solutions/lab01_fastapi_basics.py

# Run pytest-based labs
python -m pytest lab04_unit_testing.py -v
python -m pytest solutions/lab04_unit_testing.py -v
```

## Tips

- Labs 01, 04, 05, 06 are pure Python — no Groq API key needed!
- Labs 02, 03, 07, 08 use Groq API for LLM-powered agents
- FastAPI labs use `TestClient` so you don't need to run a server
- Look for `# TODO` markers — that's where you write code
- Each lab has 2 TODOs with commented starter code
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
