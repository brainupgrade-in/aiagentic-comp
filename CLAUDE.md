# Agentic AI Course (Oracle)

## Project Overview

5-day comprehensive Agentic AI training course delivered by Rajesh Gheware. Covers the full spectrum from LangChain fundamentals to production deployment with observability.

**Client:** Oracle
**Duration:** 5 days (15 sessions, ~3 sessions/day + hands-on labs)
**Course outline:** `course-outline-agentic-ai.pdf`
**Slides:** 15 HTML presentations in `presentation/`
**Hands-on:** 117 labs + 117 solutions in `hands-on/session-1/` through `session-15/`

## Lab Environment

**Platform:** GitHub Codespaces (free tier)
- Each participant uses their own GitHub account
- **Machine spec:** 2-core / 8 GB RAM / 32 GB storage
- **Free tier budget:** 120 core-hours/month → 60 hours on 2-core → 40 hours needed for 5-day course
- Default codespace image includes Python and common utilities

**Key constraint:** 8 GB RAM and 32 GB storage require careful resource management — never run all services simultaneously. Day-specific setup/cleanup scripts handle this.

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| LLM (Day 1) | Ollama + llama3.2:1b | Smallest model (~1.3 GB), sufficient for demos, removed after Day 1 |
| LLM (Days 2-5) | Groq free API | Offloads inference to cloud, saves ~2 GB RAM/storage. Each participant creates own Groq API key |
| MCP SDK | MCP Python SDK (`mcp>=1.0`) | Standard protocol for AI tool integration. Lightweight, no infrastructure overhead |
| Observability | Python in-process (no containers) | Lowest overhead on 2-core. Mock LangFuse logs to local JSON, OTel ConsoleSpanExporter |
| Vector DB | ChromaDB | Open-source, lightweight, sufficient for course exercises |
| API framework | FastAPI | Lightweight, async-native, good fit for AI application serving |
| Base image | python:3.13-bookworm devcontainer | Pre-built, includes common dev tools |

## Runtime

- **Python:** 3.13 (via `mcr.microsoft.com/devcontainers/python:3.13-bookworm`)
- Some LangChain packages may lag behind on 3.13 support — test `pip install -r requirements.txt` before the course and pin versions if needed

## Resource Management Strategy

Resources are tight on the free tier. The course uses a sequential approach:

```
Day 1: Ollama + LangChain + Vibe Coding (~5-6 GB RAM)
       → cleanup: remove Ollama completely

Day 2: LangChain + Groq API + ChromaDB (~3.5-4.5 GB RAM)
       → no cleanup needed

Day 3: LangGraph + Multi-Agent (~4-5 GB RAM)
       → cleanup: stop servers + clean temp files

Day 4: Python OTel + mock LangFuse + FastAPI (~3-4 GB RAM)
       → all Python in-process, no containers
       → cleanup: remove temp files

Day 5: MCP SDK + AI Safety + Capstone (~3-4 GB RAM)
       → lightweight, no containers needed
       → cleanup: remove temp files
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
│   └── post-create.sh                   Auto-setup: venv, pip install
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
│   ├── add-header-footer.sh             Batch update utility
│   ├── README.md                        Presentation documentation
│   ├── HEADER-FOOTER-GUIDE.md          Header/footer customization guide
│   └── FIXES-APPLIED.md                Recent fixes and improvements
├── hands-on/                            15 session directories with .ipynb labs + solutions
│   ├── session-1/                       6 labs + 6 solutions + README (.ipynb)
│   ├── session-2/                       8 labs + 8 solutions + README (.ipynb)
│   ├── session-3/                       7 labs + 7 solutions + README (.ipynb)
│   ├── session-4/ through session-15/   8 labs + 8 solutions + README each (.ipynb)
│   └── (session-1 has 6, session-3 has 7, all others have 8)
└── scripts/
    ├── day1-setup.sh                    Install Ollama + pull llama3.2:1b
    ├── day1-cleanup.sh                  Remove Ollama + model (~2 GB freed)
    ├── day2-setup.sh                    Verify Groq API key + LangChain packages
    ├── day2-cleanup.sh                  Clean temp files
    ├── day3-setup.sh                    Verify LangGraph packages
    ├── day3-cleanup.sh                  Stop servers + clean up for Day 4
    ├── day4-setup.sh                    Verify OTel + LangFuse + FastAPI packages
    ├── day4-cleanup.sh                  Clean temp files
    ├── day5-setup.sh                    Install MCP SDK, verify env
    ├── day5-cleanup.sh                  Final cleanup
    └── check-resources.sh              Memory/storage/process status monitor
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
| 2 | AI Coding Assistants & Vibe Coding | 8 | Agent loop, context management, vibe coding, prompts |
| 3 | Reasoning, Planning & Tool Use | 7 | ReAct, chain-of-thought, tool calling |
| 4 | LangChain Fundamentals | 8 | LCEL, chains, prompts, output parsers |
| 5 | Building RAG Applications | 8 | Document loaders, embeddings, vector stores, retrieval |
| 6 | LangChain Agents & Memory | 8 | Agent types, memory patterns, conversation management |
| 7 | LangGraph Stateful Workflows | 8 | StateGraph, nodes, edges, conditional routing |
| 8 | Advanced LangGraph Workflows | 8 | Human-in-the-loop, subgraphs, parallel execution |
| 9 | Multi-Agent Systems | 8 | Supervisor pattern, agent collaboration, orchestration |
| 10 | Observability Fundamentals | 8 | Three pillars, metric types, structured logging, OTel |
| 11 | LangFuse Observability | 8 | Trace hierarchy, CallbackHandler, feedback, cost tracking |
| 12 | Production Development & Deployment | 8 | FastAPI, health probes, secrets, structured logging, production checklist |
| 13 | Model Context Protocol (MCP) | 8 | MCP architecture, enterprise use cases, ecosystem discovery, client config, LangChain bridge, security & governance |
| 14 | AI Safety & Guardrails | 8 | Prompt injection, output validation, jailbreak defense, guardrails, red teaming |
| 15 | Capstone Project | 8 | Architecture design, integration, deployment, testing (2 time slots) |

## Key Ports

| Port | Service | Days Active |
|------|---------|-------------|
| 8000 | FastAPI application | 4 |
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

- Free tier: 30 requests/minute, 14,400 requests/day per API key
- Each participant must create their own key at https://console.groq.com
- Env var: `GROQ_API_KEY` in `.env` (copy from `.env.example` at project root)
- LangChain integration: `langchain-groq` package, `ChatGroq` class

## Course Outline Review Notes

Strengths identified:
- Strong logical 5-day progression (foundations → LangChain → LangGraph → observability+production → MCP+capstone)
- 117 labs + 15 challenge labs across 15 sessions
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
  - `/tmp/k8s-lab-NN-XX/` (sessions 1, 3-11)
  - `/tmp/aidev-lab-NN-XX/` (sessions 2, 13)
  - `/tmp/prod-lab-12-XX/` (session 12)
  - `/tmp/safety-lab-14-XX/` (session 14)
  - `/tmp/capstone-lab-15-XX/` (session 15)
- Labs build progressively within each session; the final lab is always a comprehensive challenge

**Totals:** 117 labs + 117 solutions across 15 sessions (~60-75 min per session, ~90-120 min for session 15)

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

**Documentation:**
- `presentation/README.md` — Complete system documentation
- `presentation/HEADER-FOOTER-GUIDE.md` — Customization guide
- `presentation/FIXES-APPLIED.md` — Recent bug fixes

**View Presentations:**
```bash
# Open course index
firefox presentation/index.html

# Open specific session
firefox presentation/session1-introduction-to-agentic-ai.html

# Apply code block enhancements (if needed)
cd presentation/
./apply-code-enhancements.sh
```

## Error Recovery (Constrained Environment)

Common failure modes on the 8 GB Codespace and how to fix them:

- **OOM (process killed):** Run `bash scripts/check-resources.sh` to see what's consuming memory. Stop unused Python processes. If Ollama is still running on Day 2+, run `bash scripts/day1-cleanup.sh`.
- **Disk full (32 GB limit):** Check for leftover models: `rm -rf ~/.ollama/models` if Day 1 cleanup was incomplete. Remove temp files in `/tmp/`.
- **ChromaDB issues:** ChromaDB runs in-process (no server needed for small datasets). Check for file lock issues.
- **Groq rate limit (429):** Wait 60 seconds and retry. If the entire class hits limits simultaneously, stagger lab start times by a few minutes.

## Commands

```bash
# Check resource usage anytime
bash scripts/check-resources.sh

# Day-specific setup
bash scripts/day1-setup.sh      # Ollama + model
bash scripts/day2-setup.sh      # Verify Groq API + LangChain packages
bash scripts/day3-setup.sh      # Verify LangGraph packages
bash scripts/day4-setup.sh      # OTel + LangFuse + FastAPI packages
bash scripts/day5-setup.sh      # MCP SDK + verify env

# Day-specific cleanup
bash scripts/day1-cleanup.sh    # Remove Ollama
bash scripts/day2-cleanup.sh    # Clean temp files
bash scripts/day3-cleanup.sh    # Stop servers
bash scripts/day4-cleanup.sh    # Clean temp files
bash scripts/day5-cleanup.sh    # Final cleanup
```

## Git Remote

- **Repository:** https://github.com/brainupgrade-in/aiagentic-comp.git
- **Branch:** main
- **Auth:** `gh auth login -h github.com` (token may need refresh)
