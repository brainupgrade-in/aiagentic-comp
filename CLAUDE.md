# CLAUDE.md - Agentic AI Course (Oracle)

## Project Overview

5-day comprehensive Agentic AI training course delivered by Rajesh Gheware. Covers the full spectrum from LangChain fundamentals to production deployment with observability.

**Client:** Oracle
**Duration:** 5 days (4 sessions/day + hands-on labs)
**Course outline:** `course-outline-agentic-ai.pdf`

## Lab Environment

**Platform:** GitHub Codespaces (free tier)
- Each participant uses their own GitHub account
- **Machine spec:** 2-core / 8 GB RAM / 32 GB storage
- **Free tier budget:** 120 core-hours/month → 60 hours on 2-core → 40 hours needed for 5-day course
- Default codespace image includes Docker, Python, and common utilities

**Key constraint:** 8 GB RAM and 32 GB storage require careful resource management — never run all services simultaneously. Day-specific setup/cleanup scripts handle this.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM (Day 1) | Ollama + llama3.2:1b | Smallest model (~1.3 GB), sufficient for demos, removed after Day 1 |
| LLM (Days 2-5) | Groq free API | Offloads inference to cloud, saves ~2 GB RAM/storage. Each participant creates own Groq API key |
| Kubernetes | MicroK8s (brief demo) | Lighter than Kind/Minikube (~300-500 MB base). Installed for Day 4 demo only, then removed |
| Observability | Docker Compose (not K8s) | Lower overhead on 2-core. Prometheus, Grafana, LangFuse run as containers on Day 5 |
| Vector DB | ChromaDB | Open-source, lightweight, sufficient for course exercises |
| API framework | FastAPI | Lightweight, async-native, good fit for AI application serving |
| Base image | python:3.11-bookworm devcontainer | Pre-built, includes common dev tools |

## Resource Management Strategy

Resources are tight on the free tier. The course uses a sequential approach:

```
Day 1: Ollama + LangChain + ChromaDB (~5-6 GB RAM)
       → cleanup: remove Ollama completely

Day 2-3: LangChain + Groq API + ChromaDB (~3.5-4.5 GB RAM)
         → no cleanup needed

Day 4: Docker + MicroK8s brief demo (~5.5-7 GB RAM)
       → cleanup: remove MicroK8s completely

Day 5: Docker Compose observability stack (~5-7 GB RAM)
       → all containers have mem_limit set
       → cleanup: docker compose down + prune
```

## File Structure

```
Oracle/
├── course-outline-agentic-ai.pdf       Course outline (11 pages)
├── requirements.txt                     Python packages (LangChain, FastAPI, OTel, etc.)
├── CLAUDE.md                            This file
├── .devcontainer/
│   ├── devcontainer.json                Codespace config (2-core, port forwarding, extensions)
│   └── post-create.sh                   Auto-setup: venv, pip install, pre-pull Docker images
└── scripts/
    ├── day1-setup.sh                    Install Ollama + pull llama3.2:1b
    ├── day1-cleanup.sh                  Remove Ollama + model (~2 GB freed)
    ├── day4-setup.sh                    Install MicroK8s + enable addons
    ├── day4-cleanup.sh                  Remove MicroK8s (~2-3 GB freed)
    ├── day5-setup.sh                    Start observability stack via docker-compose
    ├── day5-cleanup.sh                  Tear down stack + docker prune
    ├── day5-docker-compose.yml          Prometheus + Grafana + LangFuse + PostgreSQL
    ├── prometheus.yml                   Scrape config for FastAPI app
    └── check-resources.sh              Memory/storage/container status monitor
```

## Course Day Breakdown

| Day | Theme | Key Technologies |
|-----|-------|-----------------|
| 1 | Agentic AI Foundations & LangChain | Ollama, LangChain, LCEL, ChromaDB |
| 2 | RAG Applications & LangChain Ecosystem | RAG pipelines, LangGraph, Groq API |
| 3 | Advanced Agents & Production Development | Multi-agent systems, FastAPI, LangGraph workflows |
| 4 | Docker & Kubernetes Deployment | Dockerfiles, MicroK8s demo, K8s manifests |
| 5 | Observability & Production Operations | OpenTelemetry, Prometheus, Grafana, LangFuse, Capstone |

## Key Ports

| Port | Service |
|------|---------|
| 8000 | FastAPI application |
| 3000 | Grafana |
| 9090 | Prometheus |
| 8080 | LangFuse |

## Docker Compose Memory Limits (Day 5)

All containers are memory-capped to prevent OOM on 8 GB:
- Prometheus: 256 MB (1-day retention, 256 MB storage cap)
- Grafana: 256 MB
- PostgreSQL (alpine): 256 MB
- LangFuse: 512 MB

## Groq API Notes

- Free tier: 30 requests/minute, 14,400 requests/day per API key
- Each participant must create their own key at https://console.groq.com
- Env var: `GROQ_API_KEY` in `~/workspace/.env`
- LangChain integration: `langchain-groq` package, `ChatGroq` class

## Course Outline Review Notes

Strengths identified:
- Strong logical 5-day progression (foundations → ecosystem → advanced → deploy → observe)
- 13 labs + capstone project
- Production-focused with real deployment and observability
- All open-source/free tooling — no vendor lock-in

Gaps to consider addressing:
- **Guardrails/safety** — no coverage of prompt injection defense or output validation
- **Agent evaluation** — no systematic eval/testing methodology
- **Legacy memory APIs** — ConversationBufferMemory/ConversationSummaryMemory are deprecated; LangGraph state is the modern approach
- **Cost management** — token budgeting, model selection trade-offs
- **CI/CD for AI apps** — relevant for the DevOps audience segment

## Commands

```bash
# Check resource usage anytime
bash scripts/check-resources.sh

# Day-specific setup
bash scripts/day1-setup.sh      # Ollama + model
bash scripts/day4-setup.sh      # MicroK8s
bash scripts/day5-setup.sh      # Observability stack

# Day-specific cleanup
bash scripts/day1-cleanup.sh    # Remove Ollama
bash scripts/day4-cleanup.sh    # Remove MicroK8s
bash scripts/day5-cleanup.sh    # Tear down Docker Compose
```
