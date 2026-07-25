# Agentic AI: Comprehensive Course

A 5-day hands-on training covering the full spectrum of Agentic AI development — from LangChain fundamentals to production deployment with enterprise-grade observability.

**Trainer:** Rajesh Gheware | **Duration:** 5 Days | **Labs:** 119 hands-on exercises

---

## Quick Start

One setup run covers all five days — there are no per-day setup scripts.

### Linux / macOS

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp

# Installs uv + Python 3.12, creates .venv, installs every package for all 5 days,
# registers the Jupyter kernel, configures all notebooks, installs Ollama + llama3.2:1b
source scripts/setup.sh

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here  (get one free at https://console.groq.com)
```

### Windows

One script, in PowerShell from the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
```

It installs Git for Windows (Git Bash + curl), `uv`, and Ollama, then runs
`scripts/setup.sh` under Git Bash. Use Git Bash for everything afterwards.

### Verify any time

```bash
bash scripts/setup.sh --verify
```

---

## Course Structure

### Day 1: Foundations & AI-Assisted Development

| Session | Topic | Labs |
|---------|-------|------|
| 1 | Introduction to Agentic AI | 6 |
| 2 | AI Coding Assistants & Vibe Coding | 9 |
| 3 | Reasoning, Planning & Tool Use | 7 |

### Day 2: LangChain, RAG & Agents

| Session | Topic | Labs |
|---------|-------|------|
| 4 | LangChain Fundamentals | 8 |
| 5 | Building RAG Applications | 8 |
| 6 | LangChain Agents & Memory | 8 |

### Day 3: LangGraph & Multi-Agent Systems

| Session | Topic | Labs |
|---------|-------|------|
| 7 | LangGraph Stateful Workflows | 8 |
| 8 | Advanced LangGraph Workflows | 8 |
| 9 | Multi-Agent Systems | 8 |

### Day 4: Observability & Production

| Session | Topic | Labs |
|---------|-------|------|
| 10 | Observability Fundamentals | 8 |
| 11 | Production Development & Deployment | 8 |
| 12 | LangFuse Observability | 9 |

### Day 5: MCP, Safety & Capstone

| Session | Topic | Labs |
|---------|-------|------|
| 13 | Model Context Protocol (MCP) | 8 |
| 14 | AI Safety & Guardrails | 8 |
| 15 | Capstone Project (2 time slots) | 8 |

**Total: 15 sessions, 119 labs, 119 solutions**

---

## Repository Layout

```
.
├── presentation/              15 HTML slide decks
│   ├── session1-introduction-to-agentic-ai.html
│   ├── session2-ai-coding-assistants-vibe-coding.html
│   ├── ...
│   ├── session14-ai-safety-guardrails.html
│   └── session15-capstone-project.html
│
├── hands-on/                  15 session directories (Jupyter notebooks)
│   ├── session-1/             6 labs + solutions + README (.ipynb)
│   ├── session-2/             9 labs + solutions + README (.ipynb)
│   ├── session-3/             7 labs + solutions + README (.ipynb)
│   ├── session-12/            9 labs + solutions + README (.ipynb)
│   └── session-4 to session-11, session-13 to session-15/  8 labs + solutions + README each (.ipynb)
│
├── scripts/                   Setup, cleanup, and utility scripts
│   ├── bootstrap.ps1          Windows: Git Bash + uv + Ollama, then setup.sh
│   ├── setup.sh               One-time setup for all 5 days (--verify, --kernel-only)
│   ├── cleanup.sh             End-of-day cleanup: cleanup.sh [1-5|all]
│   ├── configure-notebooks.py Point every notebook at the course kernel
│   ├── langfuse-server.sh     start | stop | status (Day 4 Session 12 Lab 09)
│   ├── submit-lab.sh          Submit a lab to GitHub Issues
│   └── check-resources.sh     Monitor memory/storage/processes
│
├── requirements.txt           Python dependencies
├── .env.example               Environment variable template
├── PARTICIPANT-INSTRUCTIONS.md    Setup & workflow guide for participants
└── LICENSE                        Proprietary license
```

---

## Running Labs

All labs are Jupyter notebooks (.ipynb). Open them in VS Code — the kernel auto-selects after setup:

```bash
# Open a student lab (has TODO sections to fill in)
code hands-on/session-4/lab01_hello_langchain.ipynb

# Compare with the solution
code hands-on/session-4/solutions/lab01_hello_langchain.ipynb
```

Labs validate your answers with `[PASS]/[FAIL]` checks. Look for `# TODO` markers and `"___"` placeholders in code cells.

---

## Day-by-Day

No per-day setup — `scripts/setup.sh` already installed everything for all five days.
Each morning, just activate the venv:

```bash
source .venv/bin/activate       # Windows Git Bash: source .venv/Scripts/activate
```

| Day | Topics | Anything extra to run |
|-----|--------|-----------------------|
| 1 | Ollama local LLM, vibe coding (OpenCode, Claude CLI), multi-provider (Groq/OpenRouter/Big Pickle) | — |
| 2 | LangChain + RAG + Agents | — |
| 3 | LangGraph + Multi-Agent | — |
| 4 | OpenTelemetry + LangFuse + FastAPI + Docker/Kubernetes | `bash scripts/langfuse-server.sh start` for Session 12 Lab 09 |
| 5 | MCP + Safety + Capstone | — |

End-of-day cleanup is optional — it removes that day's `/tmp` lab dirs and stops
the servers the course started. The `.venv` is never touched.

```bash
bash scripts/cleanup.sh 4          # end of Day 4 (stops LangFuse, drops its DB)
bash scripts/cleanup.sh            # all days (end of course)
bash scripts/setup.sh --verify     # check the environment
bash scripts/check-resources.sh    # memory / storage / processes
```

---

## Technology Stack

| Category | Tools |
|----------|-------|
| **LLM providers (multi-provider, vendor-agnostic)** | Ollama (local, Day 1), Groq (Days 2-5), OpenRouter, Big Pickle, Claude, OpenAI GPT |
| **AI coding assistants (vibe coding)** | OpenCode, Claude CLI |
| **AI framework** | LangChain, LangGraph |
| **Agent protocol** | MCP (Model Context Protocol) Python SDK |
| **Vector DB** | ChromaDB |
| **API** | FastAPI, Uvicorn |
| **Observability** | OpenTelemetry, LangFuse (self-hostable) |
| **Cloud-native deployment** | Docker, Kubernetes (Deployments, Services, Ingress, HPA, Secrets, NetworkPolicies) |

---

## Prerequisites

- Basic Python programming
- Basic understanding of APIs and REST
- Familiarity with command line / terminal
- Linux (Ubuntu recommended), macOS, or Windows with Git Bash — all with 16 GB RAM

---

## Key Ports

| Port | Service | Day |
|------|---------|-----|
| 11434 | Ollama | Day 1 only |
| 8000 | FastAPI App | Day 4 |
| 3000 | LangFuse local server (optional) | Day 4, Session 12 Lab 09 |

---

## License

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.

This material is licensed for use solely by authorized training participants. See [LICENSE](LICENSE) for details.
