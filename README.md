# Agentic AI: Comprehensive Course

A 5-day hands-on training covering the full spectrum of Agentic AI development — from LangChain fundamentals to production deployment with enterprise-grade observability.

**Trainer:** Rajesh Gheware | **Duration:** 5 Days | **Labs:** 119 hands-on exercises

---

## Quick Start

### Local Setup (Linux / macOS / Windows Git Bash)

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp

# One command: creates .venv, installs all packages, registers Jupyter kernel,
# configures all notebooks, and activates the venv in your shell
source scripts/initial-setup.sh

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here  (get one free at https://console.groq.com)

# Run day-specific setup
bash scripts/day1-setup.sh
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
│   ├── initial-setup.sh       One-time setup (venv + packages + kernel + notebooks)
│   ├── day1-setup.sh          Install Ollama + llama3.2:1b
│   ├── day1-cleanup.sh        Remove Ollama (~2 GB freed)
│   ├── day2-setup.sh          Verify Groq API + packages
│   ├── day2-cleanup.sh        Clean temp files
│   ├── day3-setup.sh          Verify LangGraph packages
│   ├── day3-cleanup.sh        Stop servers + clean up
│   ├── day4-setup.sh          Verify OTel + LangFuse + FastAPI packages
│   ├── day4-cleanup.sh        Clean temp files
│   ├── day5-setup.sh          MCP SDK + verify env
│   ├── day5-cleanup.sh        Final cleanup
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

## Day-by-Day Setup

Run the setup script at the start of each day and cleanup at the end:

```bash
# Day 1: Ollama + Local LLM + Vibe Coding (OpenCode, Claude CLI) + Multi-provider (Groq/OpenRouter/Big Pickle)
bash scripts/day1-setup.sh
bash scripts/day1-cleanup.sh    # End of day

# Day 2: LangChain + RAG + Agents
bash scripts/day2-setup.sh
bash scripts/day2-cleanup.sh    # End of day

# Day 3: LangGraph + Multi-Agent
bash scripts/day3-setup.sh
bash scripts/day3-cleanup.sh    # End of day

# Day 4: Observability (OpenTelemetry + LangFuse) + FastAPI + Cloud-Native Deployment (Docker + Kubernetes)
bash scripts/day4-setup.sh
bash scripts/day4-cleanup.sh    # End of day

# Day 5: MCP + Safety + Capstone
bash scripts/day5-setup.sh
bash scripts/day5-cleanup.sh    # End of day

# Check resources anytime
bash scripts/check-resources.sh
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

---

## License

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.

This material is licensed for use solely by authorized training participants. See [LICENSE](LICENSE) for details.
