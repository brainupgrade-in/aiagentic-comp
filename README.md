# Agentic AI: Comprehensive Course

A 5-day hands-on training covering the full spectrum of Agentic AI development -- from LangChain fundamentals to production deployment with enterprise-grade observability.

**Trainer:** Rajesh Gheware | **Duration:** 5 Days | **Labs:** 117 hands-on exercises

---

## Quick Start

### Option 1: GitHub Codespaces (Recommended)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&repo=brainupgrade-in/aiagentic-comp)

The Codespace auto-configures Python 3.13, Docker, and all dependencies. After launch:

```bash
# 1. Copy environment template
cp ~/workspace/.env.template ~/workspace/.env

# 2. Add your Groq API key (https://console.groq.com)
nano ~/workspace/.env

# 3. Run day-specific setup
bash scripts/day1-setup.sh
```

### Option 2: Local Setup

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

---

## Course Structure

### Day 1: Agentic AI Foundations & LangChain

| Session | Topic | Labs |
|---------|-------|------|
| 1 | Introduction to Agentic AI | 6 |
| 2 | Reasoning, Planning & Tool Use | 7 |
| 3 | LangChain Fundamentals | 8 |

### Day 2: RAG, Agents & LangGraph

| Session | Topic | Labs |
|---------|-------|------|
| 4 | Building RAG Applications | 8 |
| 5 | LangChain Agents & Memory | 8 |
| 6 | LangGraph Stateful Workflows | 8 |

### Day 3: Advanced Patterns & Production

| Session | Topic | Labs |
|---------|-------|------|
| 7 | Advanced LangGraph Workflows | 8 |
| 8 | Multi-Agent Systems | 8 |
| 9 | Production Application Development | 8 |

### Day 4: AI Coding Agents & MCP

| Session | Topic | Labs |
|---------|-------|------|
| 10 | AI Coding Agents & Vibe Coding | 8 |
| 11 | Model Context Protocol (MCP) | 8 |
| 12 | Building Custom AI Dev Tools | 8 |

### Day 5: Observability & Production Operations

| Session | Topic | Labs |
|---------|-------|------|
| 13 | Observability Fundamentals | 8 |
| 14 | AI-Specific Observability with LangFuse | 8 |
| 15 | Capstone & Production Readiness | 8 |

**Total: 15 sessions, 117 labs, 117 solutions**

---

## Repository Layout

```
.
├── presentation/              15 HTML slide decks
│   ├── session1-introduction-to-agentic-ai.html
│   ├── ...
│   └── session15-capstone-production-readiness.html
│
├── hands-on/                  15 session directories
│   ├── session-1/             6 labs + solutions + README
│   ├── session-2/             7 labs + solutions + README
│   ├── session-3/             8 labs + solutions + README
│   ├── ...
│   └── session-15/            8 labs + solutions + README
│
├── scripts/                   Day-specific automation
│   ├── day1-setup.sh          Install Ollama + llama3.2:1b
│   ├── day1-cleanup.sh        Remove Ollama (~2 GB freed)
│   ├── day2-setup.sh          Verify Groq API + packages
│   ├── day2-cleanup.sh        Clean temp files
│   ├── day3-setup.sh          Verify FastAPI + pull ChromaDB
│   ├── day3-cleanup.sh        Stop servers + clean up
│   ├── day4-setup.sh          MCP SDK + AI coding tools
│   ├── day4-cleanup.sh        Clean up MCP servers + temp files
│   ├── day5-setup.sh          Start observability stack
│   ├── day5-cleanup.sh        Tear down Docker Compose
│   ├── day5-docker-compose.yml
│   ├── prometheus.yml
│   └── check-resources.sh     Monitor memory/storage/containers
│
├── .devcontainer/             GitHub Codespaces config
│   ├── devcontainer.json      2-core, 8 GB RAM, Python 3.13
│   └── post-create.sh         Auto-setup script
│
├── requirements.txt           Python dependencies
├── .env.example               Environment variable template
├── COURSE-OUTLINE.md          Full course outline
├── INSTRUCTOR-GUIDE.md        Teaching notes & schedule
└── LICENSE                    Proprietary license
```

---

## Running Labs

Each session has a README with lab details. The general pattern:

```bash
# Navigate to a session
cd hands-on/session-3

# Run a student lab (has TODO sections to fill in)
python lab01_lcel_basics.py

# Check your work against the solution
python solutions/lab01_lcel_basics.py
```

Labs validate your answers with `[PASS]/[FAIL]` checks. Look for `# TODO` markers.

---

## Day-by-Day Setup

Run the setup script at the start of each day and cleanup at the end:

```bash
# Day 1: Ollama + Local LLM
bash scripts/day1-setup.sh
bash scripts/day1-cleanup.sh    # End of day

# Day 2: LangChain + Groq API
bash scripts/day2-setup.sh
bash scripts/day2-cleanup.sh    # End of day

# Day 3: Production Development
bash scripts/day3-setup.sh
bash scripts/day3-cleanup.sh    # End of day

# Day 4: AI Coding Agents + MCP
bash scripts/day4-setup.sh
bash scripts/day4-cleanup.sh    # End of day

# Day 5: Observability Stack
bash scripts/day5-setup.sh
bash scripts/day5-cleanup.sh    # End of day

# Check resources anytime
bash scripts/check-resources.sh
```

---

## AI Coding Assistant

[OpenCode](https://opencode.ai/) is pre-installed in the Codespace for AI-assisted coding during labs:

```bash
opencode                    # Launch TUI
opencode 'fix this error'  # Non-interactive mode
```

Inside OpenCode, type `/connect` and select GitHub Copilot to authenticate.

---

## Technology Stack

| Category | Tools |
|----------|-------|
| **LLM** | Ollama (Day 1), Groq API (Days 2-5) |
| **AI Framework** | LangChain, LangGraph |
| **Vector DB** | ChromaDB |
| **API** | FastAPI, Uvicorn |
| **AI Dev Tools** | MCP Python SDK, AI Coding Agents |
| **Observability** | OpenTelemetry, Prometheus, Grafana, LangFuse |

---

## Prerequisites

- Basic Python programming
- Basic understanding of APIs and REST
- Familiarity with command line / terminal
- Familiarity with AI coding assistants helpful but not required
- GitHub account (for Codespaces)

---

## Key Ports

| Port | Service |
|------|---------|
| 8000 | FastAPI App |
| 3000 | Grafana |
| 9090 | Prometheus |
| 8080 | LangFuse |

---

## License

Copyright (c) 2026 Gheware UniGPS Solutions LLP. All Rights Reserved.

This material is licensed for use solely by authorized training participants. See [LICENSE](LICENSE) for details.
