# Session 11: Production Development & Deployment — Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- FastAPI and dependencies: `pip install fastapi uvicorn httpx python-dotenv`
- GROQ_API_KEY for labs 02 and 04

```bash
pip install fastapi uvicorn httpx python-dotenv
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs API Key? |
|-----|-------|-------------------|----------------|
| 01 | FastAPI Basics | Pydantic models, REST endpoints, error handling, TestClient | No |
| 02 | FastAPI + LangGraph Agent | Exposing LangGraph via REST, async handling | Yes |
| 03 | Health Checks & Probes | /health endpoint, Python async HealthChecker, signal handlers | No |
| 04 | Streaming Responses | SSE streaming, progress events, real-time agent output | Yes |
| 05 | Secrets Management | .env files, python-dotenv load_dotenv(), environment variables | No |
| 06 | Structured Logging | JSON logging, trace_id correlation, AI-specific fields | No |
| 07 | Production Checklist | Readiness categories, deployment order, resource sizing | No |
| 08 | **Challenge** | Complete production-ready API: FastAPI + health + logging + secrets | No |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-11/
├── lab01_fastapi_basics.ipynb             ← Start here
├── lab02_fastapi_langgraph.ipynb
├── lab03_health_probes.ipynb
├── lab04_streaming_responses.ipynb
├── lab05_secrets_management.ipynb
├── lab06_structured_logging.ipynb
├── lab07_production_checklist.ipynb
├── lab08_challenge.ipynb
└── solutions/                              ← Completed versions
    ├── lab01_fastapi_basics.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01-02 cover FastAPI basics and agent integration
- Labs 03-06 cover production patterns (health, secrets, logging)
- Lab 07 is the production checklist
- Lab 08 is the comprehensive challenge combining all patterns
- **Read the markdown cells** — they explain production concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Generated files appear in `/tmp/prod-lab-11-XX/` directories
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck

## Estimated Time

~60-75 minutes for all labs (including the challenge)
