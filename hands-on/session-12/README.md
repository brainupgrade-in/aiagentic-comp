# Session 12: Production Development & Deployment — Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- FastAPI and dependencies: `pip install fastapi uvicorn httpx python-dotenv`
- GROQ_API_KEY for labs 02 and 04

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

```bash
cd hands-on/session-12

# Run a lab
python lab01_fastapi_basics.py

# Check the solution
python solutions/lab01_fastapi_basics.py
```

## Tips

- Labs 01-02 cover FastAPI basics and agent integration
- Labs 03-06 cover production patterns (health, secrets, logging)
- Lab 07 is the production checklist
- Lab 08 is the comprehensive challenge combining all patterns
- Generated files appear in `/tmp/prod-lab-12-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
