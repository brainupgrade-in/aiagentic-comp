# Agentic AI Course (Oracle)

## Project Overview

5-day comprehensive Agentic AI training course delivered by Rajesh Gheware. Covers the full spectrum from LangChain fundamentals to production deployment with observability.

**Client:** Oracle
**Duration:** 5 days (17 sessions, ~4 sessions/day + hands-on labs)
**Course outline:** `course-outline-agentic-ai.pdf`
**Slides:** 17 HTML presentations in `presentation/`
**Hands-on:** 133 labs + 133 solutions in `hands-on/session-1/` through `session-17/`

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
| Base image | python:3.13-bookworm devcontainer | Pre-built, includes common dev tools |

## Runtime

- **Python:** 3.13 (via `mcr.microsoft.com/devcontainers/python:3.13-bookworm`)
- Some LangChain packages may lag behind on 3.13 support — test `pip install -r requirements.txt` before the course and pin versions if needed

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
├── README.md                            GitHub landing page
├── COURSE-OUTLINE.md                    Full course outline (markdown version)
├── INSTRUCTOR-GUIDE.md                  Teaching notes, schedule, day-session mapping
├── LICENSE                              Gheware UniGPS Solutions LLP, All Rights Reserved
├── requirements.txt                     Python packages (LangChain, FastAPI, OTel, etc.)
├── .env.example                         Environment variable template (all 5 days)
├── course-outline-agentic-ai.pdf        Course outline PDF (gitignored)
├── CLAUDE.md                            This file
├── .devcontainer/
│   ├── devcontainer.json                Codespace config (2-core, port forwarding, extensions)
│   └── post-create.sh                   Auto-setup: venv, pip install, pre-pull Docker images
├── presentation/                        17 HTML slide decks (one per session)
│   ├── session1-introduction-to-agentic-ai.html
│   ├── ...
│   └── session17-capstone-production-readiness.html
├── hands-on/                            17 session directories with labs + solutions
│   ├── session-1/                       6 labs + 6 solutions + README
│   ├── session-2/                       7 labs + 7 solutions + README
│   ├── session-3/ through session-17/   8 labs + 8 solutions + README each
│   └── (session-1 has lab01-lab06, session-2 has lab01-lab07, sessions 3-17 have lab01-lab08)
└── scripts/
    ├── day1-setup.sh                    Install Ollama + pull llama3.2:1b
    ├── day1-cleanup.sh                  Remove Ollama + model (~2 GB freed)
    ├── day2-setup.sh                    Verify Groq API key + LangChain packages
    ├── day2-cleanup.sh                  Clean ChromaDB containers + temp files
    ├── day3-setup.sh                    Verify FastAPI packages + pull ChromaDB
    ├── day3-cleanup.sh                  Stop servers + clean up for Day 4
    ├── day4-setup.sh                    Install MicroK8s + enable addons
    ├── day4-cleanup.sh                  Remove MicroK8s (~2-3 GB freed)
    ├── day5-setup.sh                    Start observability stack via docker-compose
    ├── day5-cleanup.sh                  Tear down stack + docker prune
    ├── day5-docker-compose.yml          Prometheus + Grafana + LangFuse + PostgreSQL (note: in scripts/, not project root)
    ├── prometheus.yml                   Scrape config for FastAPI app
    └── check-resources.sh              Memory/storage/container status monitor
```

## Course Day Breakdown

| Day | Theme | Sessions | Key Technologies |
|-----|-------|----------|-----------------|
| 1 | Agentic AI Foundations | 1-4 | Ollama, LangChain, LCEL, RAG, ChromaDB |
| 2 | Advanced Patterns | 5-7 | Agents, Memory, LangGraph, Stateful Workflows |
| 3 | Production Development | 8-9 | Multi-agent systems, FastAPI, Production patterns |
| 4 | Containerization & K8s | 10-13 | Docker, Kubernetes, Deployments, Operations |
| 5 | Observability & Capstone | 14-17 | OpenTelemetry, Prometheus, Grafana, LangFuse, Production Readiness |

## Session-by-Session Details

| Session | Title | Labs | Topics |
|---------|-------|------|--------|
| 1 | Introduction to Agentic AI | 6 | AI agents, reasoning, tool use, architectures |
| 2 | Reasoning, Planning & Tool Use | 7 | ReAct, chain-of-thought, tool calling |
| 3 | LangChain Fundamentals | 8 | LCEL, chains, prompts, output parsers |
| 4 | Building RAG Applications | 8 | Document loaders, embeddings, vector stores, retrieval |
| 5 | LangChain Agents & Memory | 8 | Agent types, memory patterns, conversation management |
| 6 | LangGraph Stateful Workflows | 8 | StateGraph, nodes, edges, conditional routing |
| 7 | Advanced LangGraph Workflows | 8 | Human-in-the-loop, subgraphs, parallel execution |
| 8 | Multi-Agent Systems | 8 | Supervisor pattern, agent collaboration, orchestration |
| 9 | Production Application Development | 8 | FastAPI, error handling, testing, deployment patterns |
| 10 | Docker for AI Applications | 8 | Dockerfiles, multi-stage builds, compose, optimization |
| 11 | Kubernetes Fundamentals | 8 | Pods, Deployments, Services, ConfigMaps, Secrets |
| 12 | Deploying AI Stack on K8s | 8 | StatefulSets, PVCs, Ingress, Helm, production manifests |
| 13 | Kubernetes Operations | 8 | Debugging, resource management, scaling, troubleshooting |
| 14 | Observability Fundamentals | 8 | Three pillars, metric types, structured logging, OTel |
| 15 | Prometheus & Grafana | 8 | PromQL, alerting, dashboard design (RED/USE), kube-prometheus |
| 16 | LangFuse Observability | 8 | Trace hierarchy, CallbackHandler, feedback, cost tracking |
| 17 | Capstone & Production Readiness | 8 | Health probes, HPA, secrets, alerting, backup, full deployment |

## Key Ports

| Port | Service | Days Active |
|------|---------|-------------|
| 8000 | FastAPI application | 3-5 |
| 8080 | LangFuse | 5 |
| 9090 | Prometheus | 5 |
| 3000 | Grafana | 5 |
| 11434 | Ollama | 1 only |
| 8001 | ChromaDB (if containerized) | 1-4 |

**Port conflict note:** ChromaDB defaults to port 8000, which conflicts with FastAPI. When both are needed, run ChromaDB on port 8001 or use it as an in-process library (no port needed).

## Docker Compose Memory Limits (Day 5)

All containers are memory-capped to prevent OOM on 8 GB:
- Prometheus: 256 MB (1-day retention, 256 MB storage cap)
- Grafana: 256 MB
- PostgreSQL (alpine): 256 MB
- LangFuse: 512 MB

## OpenCode — AI Coding Assistant

[OpenCode](https://opencode.ai/) is pre-installed in the devcontainer so participants can use AI-assisted coding directly in the terminal during labs and assignments.

- **Install:** `curl -fsSL https://opencode.ai/install | bash` (done automatically in post-create.sh)
- **Launch:** `opencode` (TUI mode) or `opencode 'your prompt'` (non-interactive)
- **Auth:** Run `/connect` inside OpenCode and select GitHub Copilot (works with Copilot Pro/Business/Enterprise subscriptions), or set `GROQ_API_KEY` in environment for Groq models
- **Agents:** `build` (default, full access) and `plan` (read-only analysis) — switch with Tab
- **Use cases:** Fix TODO sections in labs, debug failing code, generate YAML configs, explain concepts
- **Note:** Verify the install URL and auth flow work before the course begins, as OpenCode updates may change the setup process

## Groq API Notes

- Free tier: 30 requests/minute, 14,400 requests/day per API key
- Each participant must create their own key at https://console.groq.com
- Env var: `GROQ_API_KEY` in `.env` (copy from `.env.example` at project root)
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

## Hands-on Lab Pattern

All labs follow a consistent Python-based pattern (no K8s cluster required):

```bash
# Run a student lab (has TODO markers to fill in)
python hands-on/session-NN/labXX_topic.py

# Run the completed solution (all checks pass)
python hands-on/session-NN/solutions/labXX_topic.py
```

**Lab structure:**
- Educational Steps (tables, code examples, architecture diagrams)
- TODO sections with `"___"` placeholders for answers
- Validation with `[PASS]/[FAIL]` string matching and scoring
- Generated YAML/config files saved to `/tmp/k8s-lab-NN-XX/`
- Labs build progressively within each session; the final lab is always a comprehensive challenge

**Totals:** 133 labs + 133 solutions across 17 sessions (~60-75 min per session)

## Error Recovery (Constrained Environment)

Common failure modes on the 8 GB Codespace and how to fix them:

- **OOM (container or process killed):** Run `bash scripts/check-resources.sh` to see what's consuming memory. Stop unused containers with `docker stop $(docker ps -q)`. If Ollama is still running on Day 2+, run `bash scripts/day1-cleanup.sh`.
- **Disk full (32 GB limit):** Run `docker system prune -af` to reclaim image/layer space. Check for leftover models: `rm -rf ~/.ollama/models` if Day 1 cleanup was incomplete.
- **Docker daemon unresponsive:** Restart with `sudo systemctl restart docker` (Codespace) or rebuild the Codespace from the GitHub UI.
- **ChromaDB connection refused:** Verify it's running (`docker ps | grep chroma`) or switch to in-process mode (no server needed for small datasets).
- **Groq rate limit (429):** Wait 60 seconds and retry. If the entire class hits limits simultaneously, stagger lab start times by a few minutes.

## Commands

```bash
# Check resource usage anytime
bash scripts/check-resources.sh

# Day-specific setup
bash scripts/day1-setup.sh      # Ollama + model
bash scripts/day2-setup.sh      # Verify Groq API + packages
bash scripts/day3-setup.sh      # Verify FastAPI + ChromaDB
bash scripts/day4-setup.sh      # MicroK8s
bash scripts/day5-setup.sh      # Observability stack

# Day-specific cleanup
bash scripts/day1-cleanup.sh    # Remove Ollama
bash scripts/day2-cleanup.sh    # Clean temp files
bash scripts/day3-cleanup.sh    # Stop servers
bash scripts/day4-cleanup.sh    # Remove MicroK8s
bash scripts/day5-cleanup.sh    # Tear down Docker Compose
```

## Git Remote

- **Repository:** https://github.com/brainupgrade-in/aiagentic-comp.git
- **Branch:** main
- **Auth:** `gh auth login -h github.com` (token may need refresh)
