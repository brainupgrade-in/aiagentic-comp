# Agentic AI Course

## Project Overview

5-day comprehensive Agentic AI training course delivered by Rajesh Gheware. Covers the full spectrum from LangChain fundamentals to production deployment with observability.

**Client:** Enterprise client
**Duration:** 5 days (15 sessions, ~3 sessions/day + hands-on labs)
**Course outline:** `course-outline-agentic-ai.pdf`
**Slides:** 15 HTML presentations in `presentation/`
**Hands-on:** 119 labs + 119 solutions in `hands-on/session-1/` through `session-15/`

## Lab Environment

**Platform:** Native Ubuntu Linux installation (NOT GitHub Codespaces)

**Instructor machine:**
- **CPU:** 12 threads
- **RAM:** 16 GB
- **OS:** Ubuntu Linux

**Participant machines:**
- **CPU:** At least 8 threads (minimum)
- **RAM:** 16 GB (minimum)
- **OS:** Ubuntu Linux (recommended) or Windows with WSL2/Ubuntu VM

**GitHub Codespaces:** Out of scope for this training. The `.devcontainer/` configuration is maintained in the repository for other use cases but is not used for this course delivery.

**Key benefits:** With 16 GB RAM, all services can run simultaneously without resource constraints. Ollama can stay installed throughout the course if desired. Multiple LLMs can be loaded for comparison. Setup/cleanup scripts are optional but still recommended for clean state between days.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM (Day 1) | Ollama + llama3.2:1b or larger models | Can use larger models (llama3.2:3b, llama3.3:70b) with 16GB RAM. Ollama can stay installed throughout course |
| LLM (Days 2-5) | Groq free API (primary) + optional local Ollama | Groq for consistency and speed. Ollama optional for offline demos. Each participant creates own Groq API key |
| MCP SDK | MCP Python SDK (`mcp>=1.0`) | Standard protocol for AI tool integration. Lightweight, no infrastructure overhead |
| Observability | Python-based LangFuse server + SQLite | No Docker needed. Labs 01-08 use MockLangFuse (JSON files), Lab 09 uses real LangFuse server (Python FastAPI + SQLite) on port 3000 |
| Vector DB | ChromaDB | Open-source, lightweight, sufficient for course exercises. Runs in-process |
| API framework | FastAPI | Lightweight, async-native, good fit for AI application serving |
| Base environment | Python 3.13 on Ubuntu Linux | Native Python installation, faster than containers for this use case |

## Runtime

- **Python:** 3.13 (native Ubuntu installation via `apt` or `pyenv`)
- **Virtual environment:** `.venv/` created with `python3 -m venv .venv`
- **Package management:** `pip install -r requirements.txt`
- Some LangChain packages may lag behind on 3.13 support — test `pip install -r requirements.txt` before the course and pin versions if needed

## Resource Management Strategy

With 16 GB RAM and 8+ CPU threads, resource management is straightforward. All services can run concurrently if needed.

**Estimated RAM usage by day:**

```
Day 1: Ollama + LangChain + Vibe Coding (~3-6 GB RAM depending on model)
       → cleanup: optional (can keep Ollama for offline demos)

Day 2: LangChain + Groq API + ChromaDB (~2-3 GB RAM)
       → cleanup: optional (temp files only)

Day 3: LangGraph + Multi-Agent (~3-4 GB RAM)
       → cleanup: optional (stop servers to free ports)

Day 4: Python OTel + LangFuse server + FastAPI (~2-3 GB RAM)
       → LangFuse server (Python FastAPI + SQLite) runs on port 3000
       → Labs 01-08: MockLangFuse (JSON files), Lab 09: Real server
       → cleanup: Stop LangFuse server, remove DB and logs

Day 5: MCP SDK + AI Safety + Capstone (~3-4 GB RAM)
       → lightweight, no containers needed
       → cleanup: optional (final cleanup recommended)
```

**Peak concurrent usage:** ~6-8 GB RAM with all services running
**Available headroom:** 8-10 GB for browser, IDE, and other applications

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
├── .gitignore                           Git ignore rules
├── .claudeignore                        Claude Code ignore rules
├── INSTRUCTOR-SUMMARY.md               Condensed instructor reference
├── PARTICIPANT-INSTRUCTIONS.md          Setup & workflow guide for participants
├── PARTICIPANT-QUICK-REFERENCE.md       One-page cheat sheet for participants
├── LAB-TRACKING-COMMENT-BASED.md        Lab submission tracking via GitHub Issues
├── co2-aiagenticavin.txt                Course order reference
├── .github/                             GitHub Issues templates, workflows
├── .devcontainer/                       (Not used for this training - GitHub Codespaces only)
│   ├── devcontainer.json                Dev container config for VS Code
│   └── post-create.sh                   Auto-setup: venv, pip install
├── reporting/                           Lab progress reporting & dashboards
├── todo/                                Task tracking notes
├── presentation/                        15 HTML slide decks + shared resources
│   ├── index.html                       Course landing page
│   ├── template.html                    Template for new sessions
│   ├── session1-introduction-to-agentic-ai.html
│   ├── session2-ai-coding-assistants-vibe-coding.html
│   ├── ... (sessions 3-14)
│   ├── session15-capstone-project.html
│   ├── shared.css                       Cybernetic theme styles (~2,700 lines)
│   ├── shared.js                        JavaScript enhancements
│   ├── reveal-init.js                   Reveal.js configuration
│   ├── presentation-header-footer.js    Auto-updating HUD interface
│   ├── code-blocks-enhanced.js          Cyberpunk terminal code block enhancements
│   ├── performance-optimizations.css    Performance tuning styles
│   ├── print.css                        Print stylesheet for slide decks
│   ├── print.js                         Print support JavaScript
│   ├── add-print-to-all.sh             Batch add print support to all sessions
│   ├── apply-print-support.sh          Apply print CSS/JS to presentations
│   ├── verify-print-support.sh         Verify print support is applied
│   ├── README.md                        Presentation documentation
│   ├── PRINT-GUIDE.md                  Print/export guide for slides
│   └── PRINT-QUICK-REFERENCE.md        Quick reference for printing
├── hands-on/                            15 session directories with .ipynb labs + solutions
│   ├── session-1/                       6 labs + 6 solutions + README (.ipynb)
│   ├── session-2/                       9 labs + 9 solutions + README (.ipynb)
│   ├── session-3/                       7 labs + 7 solutions + README (.ipynb)
│   ├── session-4/ through session-15/   8 labs + 8 solutions + README each (.ipynb)
│   └── (session-1 has 6, session-2 has 9, session-3 has 7, session-12 has 9, all others have 8)
└── scripts/                             Both .sh (Linux/macOS) and .ps1 (Windows) provided
    ├── initial-setup.sh / .ps1          One-time setup: Python, venv, packages, .env
    ├── install-notebook.sh / .ps1       VS Code Jupyter extension + ipykernel
    ├── install-jupyter-kernel.sh / .ps1 Named kernel spec for the course
    ├── check-resources.sh / .ps1        Memory/storage/process status monitor
    ├── submit-lab.sh / .ps1             Lab submission to GitHub Issues
    ├── test-langfuse-server.sh / .ps1   LangFuse server verification (instructor)
    ├── day1-setup.sh / .ps1             Install Ollama + pull llama3.2:1b
    ├── day1-cleanup.sh / .ps1           Remove Ollama + model (~2 GB freed)
    ├── day2-setup.sh / .ps1             Verify Groq API key + LangChain packages
    ├── day2-cleanup.sh / .ps1           Clean temp files
    ├── day3-setup.sh / .ps1             Verify LangGraph packages
    ├── day3-cleanup.sh / .ps1           Stop servers + clean up for Day 4
    ├── day4-setup.sh / .ps1             Verify OTel + LangFuse + FastAPI + start server
    ├── day4-cleanup.sh / .ps1           Stop LangFuse + FastAPI + clean temp files
    ├── day5-setup.sh / .ps1             Install MCP SDK, verify env
    ├── day5-cleanup.sh / .ps1           Final cleanup
    ├── langfuse-server.py               LangFuse server implementation (FastAPI + SQLite)
    ├── populate_langfuse_data.py         Seed LangFuse with sample trace data
    ├── configure-all-notebooks.py        Configure kernel for all .ipynb files
    ├── configure-notebook-kernels.py     Set kernel specs per session
    ├── setup-notebook-kernel.py          Install named Jupyter kernel
    ├── create-lab-issues.py              Create GitHub Issues for lab tracking
    ├── track-lab-comments.py             Parse lab submission comments
    ├── README.md                         Scripts documentation
    ├── README-langfuse-server.md         LangFuse server setup guide
    └── SUBMIT-LAB-GUIDE.md              Lab submission instructions
```

## Course Day Breakdown

| Day | Theme | Sessions | Key Technologies |
|-----|-------|----------|-----------------|
| 1 | Foundations & AI-Assisted Dev | 1-3 | Ollama, Vibe Coding, ReAct, Chain-of-Thought |
| 2 | LangChain, RAG & Agents | 4-6 | LangChain, LCEL, ChromaDB, RAG, Agents, Memory |
| 3 | LangGraph & Multi-Agent | 7-9 | LangGraph, StateGraph, Multi-Agent, Orchestration |
| 4 | Observability & Production | 10-12 | OTel, LangFuse, FastAPI, Health Probes, Secrets |
| 5 | MCP, Safety & Capstone | 13-15 | MCP, JSON-RPC 2.0, AI Safety, Capstone Integration |

## Session-by-Session Details

| Session | Title | Labs | Topics |
|---------|-------|------|--------|
| 1 | Introduction to Agentic AI | 6 | AI agents, reasoning, tool use, architectures |
| 2 | AI Coding Assistants & Vibe Coding | 9 | Agent loop, context management, vibe coding, safety, iterative refinement |
| 3 | Reasoning, Planning & Tool Use | 7 | ReAct, chain-of-thought, tool calling |
| 4 | LangChain Fundamentals | 8 | LCEL, chains, prompts, output parsers |
| 5 | Building RAG Applications | 8 | Document loaders, embeddings, vector stores, retrieval |
| 6 | LangChain Agents & Memory | 8 | Agent types, memory patterns, conversation management |
| 7 | LangGraph Stateful Workflows | 8 | StateGraph, nodes, edges, conditional routing |
| 8 | Advanced LangGraph Workflows | 8 | Human-in-the-loop, subgraphs, parallel execution |
| 9 | Multi-Agent Systems | 8 | Supervisor pattern, agent collaboration, orchestration |
| 10 | Observability Fundamentals | 8 | Three pillars, metric types, structured logging, OTel |
| 11 | Production Development & Deployment | 8 | FastAPI, health probes, secrets, structured logging, production checklist |
| 12 | LangFuse Observability | 9 | Trace hierarchy, CallbackHandler, feedback, cost tracking, **production integration (Lab 09)** |
| 13 | Model Context Protocol (MCP) | 8 | MCP architecture, enterprise use cases, ecosystem discovery, client config, LangChain bridge, security & governance |
| 14 | AI Safety & Guardrails | 8 | Prompt injection, output validation, jailbreak defense, guardrails, red teaming |
| 15 | Capstone Project | 8 | Architecture design, integration, deployment, testing (2 time slots) |

## Key Ports

| Port | Service | Days Active |
|------|---------|-------------|
| 3000 | LangFuse server (Python + SQLite) | 4 (Session 12 Lab 09) |
| 8000 | FastAPI application | 4 (Session 11 labs) |
| 11434 | Ollama | 1 only |

## OpenCode — AI Coding Assistant

[OpenCode](https://opencode.ai/) is pre-installed in the devcontainer so participants can use AI-assisted coding directly in the terminal during labs and assignments.

- **Install:** `curl -fsSL https://opencode.ai/install | bash` (done automatically in post-create.sh)
- **Launch:** `opencode` (TUI mode) or `opencode 'your prompt'` (non-interactive)
- **Auth:** Run `/connect` inside OpenCode and select GitHub Copilot (works with Copilot Pro/Business/Enterprise subscriptions), or set `GROQ_API_KEY` in environment for Groq models
- **Agents:** `build` (default, full access) and `plan` (read-only analysis) — switch with Tab
- **Use cases:** Fix TODO sections in labs, debug failing code, generate YAML configs, explain concepts
- **Note:** Verify the install URL and auth flow work before the course begins, as OpenCode updates may change the setup process

## Groq API Notes

- Free tier: ~1,000 requests/minute, ~250K tokens/minute per API key
- Each participant must create their own key at https://console.groq.com
- Env var: `GROQ_API_KEY` in `.env` (copy from `.env.example` at project root)
- LangChain integration: `langchain-groq` package, `ChatGroq` class

## Course Outline Review Notes

Strengths identified:
- Strong logical 5-day progression (foundations → LangChain → LangGraph → observability+production → MCP+capstone)
- 119 labs + 15 challenge labs across 15 sessions
- Production-focused with observability and capstone
- All open-source/free tooling — no vendor lock-in
- Vibe coding on Day 1 means students use AI assistants for 4 more days
- Observability directly after multi-agent (Day 4) for natural flow into production
- Extended capstone (2 time slots) on Day 5 for comprehensive integration

Gaps to consider addressing:
- **Agent evaluation** — no systematic eval/testing methodology
- **Legacy memory APIs** — ConversationBufferMemory/ConversationSummaryMemory are deprecated; LangGraph state is the modern approach
- **Cost management** — token budgeting, model selection trade-offs
- **CI/CD for AI apps** — relevant for the DevOps audience segment

## Hands-on Lab Pattern

All labs are Jupyter notebooks (.ipynb) — no standalone .py scripts. Open them in VS Code, JupyterLab, or any notebook-compatible environment:

```bash
# Open a student lab (has TODO markers to fill in)
hands-on/session-NN/labXX_topic.ipynb

# Open the completed solution (all checks pass)
hands-on/session-NN/solutions/labXX_topic.ipynb
```

**Lab structure:**
- Educational Steps (tables, code examples, architecture diagrams) in markdown cells
- TODO sections with `"___"` placeholders for answers in code cells
- Validation with `[PASS]/[FAIL]` string matching and scoring
- Generated files saved to:
  - `/tmp/k8s-lab-NN-XX/` (sessions 1, 3-10, 12)
  - `/tmp/aidev-lab-NN-XX/` (sessions 2, 13)
  - `/tmp/prod-lab-11-XX/` (session 11)
  - `/tmp/safety-lab-14-XX/` (session 14)
  - `/tmp/capstone-lab-15-XX/` (session 15)
- Labs build progressively within each session; the final lab is always a comprehensive challenge

**Totals:** 119 labs + 119 solutions across 15 sessions (~60-75 min per session, ~90-120 min for session 15, session 12 now ~90-115 min with Lab 09)

## Presentation System

All 15 session presentations use Reveal.js 4.6.1 with a custom **Cybernetic HUD Interface** system.

### Key Features

**Header (Fixed Top):**
- Home button (links to `index.html`)
- Course title "AGENTIC AI"
- Auto-detected session number & day (from page `<title>`)
- Animated scanline effect
- Pulsing live indicator

**Footer (Fixed Bottom):**
- Auto-updating slide counter (e.g., "5/45")
- Trainer name "Rajesh Gheware"
- brainupgrade.in branding
- Pulsing status indicator

**Shared Resources:**
- `shared.css` (~2,700 lines) — Cybernetic theme, components, animations
- `shared.js` — JavaScript enhancements (index link, keyboard shortcuts)
- `reveal-init.js` — Standardized Reveal.js configuration
- `presentation-header-footer.js` — Auto-updating HUD interface
- `code-blocks-enhanced.js` — Cyberpunk terminal code block enhancements

**Code Blocks - Cyberpunk Terminal Interface:**
- HUD-style corner brackets with pulsing glow animations
- Terminal header bar with language badges and status indicators
- Animated scanlines creating CRT monitor effect
- Enhanced syntax highlighting with electric glow effects
- Production-grade copy buttons with success feedback
- Holographic shimmer effects on hover
- Auto-enhancement via JavaScript (runs on all presentations)
- Fallback support for older browsers

**Design System:**
- Electric teal (#00ffcc) primary accent
- Dark cybernetic theme with gradient backgrounds
- HUD-style corner brackets and glowing effects
- Typography: Inter (body) + JetBrains Mono (code/data)
- 30+ reusable components (cards, diagrams, callouts, quiz styles)
- 5 animation types (scanline, pulse, card reveal, glow, hover)

**Responsive:**
- 1920×1080 base resolution with automatic scaling
- Browser zoom support without layout breaking
- Works on desktop, laptop, tablet, mobile

**Print Support:**
- `print.css` + `print.js` — Print/export slides to PDF
- `add-print-to-all.sh` — Batch apply print support
- `PRINT-GUIDE.md` / `PRINT-QUICK-REFERENCE.md` — Print documentation

**Documentation:**
- `presentation/README.md` — Complete system documentation

**View Presentations:**
```bash
# Open course index
firefox presentation/index.html

# Open specific session
firefox presentation/session1-introduction-to-agentic-ai.html
```

## Error Recovery

Common issues and solutions with 16 GB RAM environment:

- **High memory usage:** Run `bash scripts/check-resources.sh` to check current usage. With 16 GB RAM, OOM is unlikely unless multiple large models are loaded simultaneously.
- **Disk space:** Check for large Ollama models: `du -sh ~/.ollama/models`. Remove unused models: `ollama rm <model-name>`. Clean temp files in `/tmp/`.
- **ChromaDB issues:** ChromaDB runs in-process (no server needed for small datasets). Check for file lock issues or permission errors.
- **Groq rate limit (429):** Free tier: ~1,000 requests/minute, ~250K tokens/minute. Wait 60 seconds and retry. If the entire class hits limits simultaneously, stagger lab start times by a few minutes.
- **Port conflicts:** If port 8000 or 11434 is in use, check running processes: `sudo lsof -i :8000` or `sudo lsof -i :11434`. Stop conflicting services or change port in configuration.
- **Python package conflicts:** Use virtual environment: `python3 -m venv .venv && source .venv/bin/activate`. Reinstall requirements: `pip install -r requirements.txt`.

## Commands

### Linux / macOS

```bash
# First-time setup (run once)
bash scripts/initial-setup.sh

# Check resource usage anytime
bash scripts/check-resources.sh

# Day-specific setup
bash scripts/day1-setup.sh      # Ollama + model
bash scripts/day2-setup.sh      # Verify Groq API + LangChain packages
bash scripts/day3-setup.sh      # Verify LangGraph packages
bash scripts/day4-setup.sh      # OTel + LangFuse + FastAPI + start server
bash scripts/day5-setup.sh      # MCP SDK + verify env

# Day-specific cleanup
bash scripts/day1-cleanup.sh    # Remove Ollama
bash scripts/day2-cleanup.sh    # Clean temp files
bash scripts/day3-cleanup.sh    # Stop servers
bash scripts/day4-cleanup.sh    # Stop LangFuse + clean temp files
bash scripts/day5-cleanup.sh    # Final cleanup

# Lab submission
bash scripts/submit-lab.sh 1 1 "notes"
```

### Windows (PowerShell)

```powershell
# First-time setup (run once)
.\scripts\initial-setup.ps1

# Check resource usage anytime
.\scripts\check-resources.ps1

# Day-specific setup
.\scripts\day1-setup.ps1        # Ollama + model
.\scripts\day2-setup.ps1        # Verify Groq API + LangChain packages
.\scripts\day3-setup.ps1        # Verify LangGraph packages
.\scripts\day4-setup.ps1        # OTel + LangFuse + FastAPI + start server
.\scripts\day5-setup.ps1        # MCP SDK + verify env

# Day-specific cleanup
.\scripts\day1-cleanup.ps1      # Remove Ollama
.\scripts\day2-cleanup.ps1      # Clean temp files
.\scripts\day3-cleanup.ps1      # Stop servers
.\scripts\day4-cleanup.ps1      # Stop LangFuse + clean temp files
.\scripts\day5-cleanup.ps1      # Final cleanup

# Lab submission
.\scripts\submit-lab.ps1 1 1 "notes"
```

## Git Remote

- **Repository:** https://github.com/brainupgrade-in/aiagentic-comp.git
- **Branch:** main
- **Auth:** `gh auth login -h github.com` (token may need refresh)
