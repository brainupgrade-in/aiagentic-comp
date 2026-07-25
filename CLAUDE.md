# Agentic AI Course

5-day enterprise training by Rajesh Gheware. 15 sessions, 119 labs + solutions.
- Slides: `presentation/` (15 HTML decks) · Labs: `hands-on/session-{1..15}/`
- Outline: `course-outline-agentic-ai.pdf` · Repo: `brainupgrade-in/aiagentic-comp`

## Environment

**Platform:** Native Ubuntu Linux — NOT Codespaces (`.devcontainer/` unused here)
**Python:** 3.12 · **Venv:** `.venv/` · `python3 -m venv .venv && pip install -r requirements.txt`
**Instructor:** 12 CPU / 16 GB RAM · **Participants:** 8+ CPU / 16 GB RAM (Ubuntu/macOS/Win Git Bash)

## Tech Stack & Key Decisions

| Component | Choice | Note |
|-----------|--------|------|
| LLM Day 1 | Ollama + llama3.2:1b+ | Local inference; 3b/70b also viable |
| LLM Days 2-5 | Groq free API (primary) | Each participant gets own key at console.groq.com |
| LLM alt providers | OpenRouter, Big Pickle, Claude, OpenAI | Taught as provider-agnostic patterns — fallback chains, cost/latency tradeoffs |
| Vibe coding | OpenCode (opencode.ai), Claude CLI | Day 1 — agent-assisted dev, prompt-to-code |
| Observability | LangFuse | S12 Labs 01-08: MockLangFuse (JSON). Lab 09: real backend via `LANGFUSE_HOST` — cloud (default) or bundled local server on :3000 (`langfuse-server.sh`) |
| Vector DB | ChromaDB | In-process, no server |
| API | FastAPI | Async, AI-native |
| Agents | MCP Python SDK `mcp>=1.0` | Standard protocol |
| Deployment | Docker + Kubernetes | Day 4: containerize FastAPI agent, deploy to K8s (Deployments, Services, Ingress, HPA, Secrets, NetworkPolicies) |

## Resource Usage by Day

| Day | Services | RAM | Cleanup |
|-----|----------|-----|---------|
| 1 | Ollama + LangChain | 3-6 GB | optional |
| 2 | LangChain + Groq + ChromaDB | 2-3 GB | optional |
| 3 | LangGraph + Multi-Agent | 3-4 GB | optional |
| 4 | OTel + LangFuse + FastAPI | 2-3 GB | **stop LangFuse; rm DB/logs** |
| 5 | MCP + Safety + Capstone | 3-4 GB | recommended final cleanup |

## Key Ports

| Port | Service | Active |
|------|---------|--------|
| 3000 | LangFuse (Python+SQLite) | Day 4 Session 12 Lab 09 |
| 8000 | FastAPI app | Day 4 Session 11 |
| 11434 | Ollama | Day 1 only |

## Lab Pattern

Notebooks: `hands-on/session-NN/labXX_topic.ipynb` (student) · `solutions/labXX_topic.ipynb` (answer)

- Code cells have `"___"` placeholders; validation outputs `[PASS]/[FAIL]` with scoring
- Output dirs: `/tmp/k8s-lab-NN-XX/` · `/tmp/aidev-lab-NN-XX/` · `/tmp/prod-lab-11-XX/` · `/tmp/safety-lab-14-XX/` · `/tmp/capstone-lab-15-XX/`
- Labs build progressively; final lab per session = comprehensive challenge
- Timing: ~60-75 min/session; session 12 ~90-115 min; session 15 ~90-120 min

## File Structure

```
├── presentation/       15 HTML decks + shared.css/js, Reveal.js HUD, print support
├── hands-on/           session-{1..15}/ with .ipynb labs + solutions/
├── scripts/            setup.sh (all 5 days, idempotent), bootstrap.ps1 (Windows),
│                       cleanup.sh, configure-notebooks.py, langfuse-server.{sh,py},
│                       submit-lab.sh, check-resources.sh
├── reporting/          generate-dashboard.py, track-lab-comments.py, update-dashboard.sh
├── .github/            ISSUE_TEMPLATE/ (lab-help, bug-report, config)
├── .vscode/            settings.json, extensions.json
├── requirements.txt    All Python deps
└── .env.example        Template for all 5 days
```

## Commands

```bash
# Setup — one run covers all 5 days; no per-day setup scripts
source scripts/setup.sh                 # uv + Python 3.12 + venv + all packages + kernel + Ollama
bash scripts/setup.sh --verify          # check venv/packages/kernel/keys/Ollama
bash scripts/setup.sh --kernel-only     # re-register kernel + reconfigure notebooks
powershell -File scripts/bootstrap.ps1  # Windows: Git Bash + uv + Ollama, then setup.sh
bash scripts/check-resources.sh         # memory/storage/process status

# Per-day
bash scripts/langfuse-server.sh start   # Day 4 Session 12 Lab 09 (:3000)
bash scripts/cleanup.sh [1-5|all]       # end-of-day cleanup (day4 stops LangFuse)

# Lab submission
bash scripts/submit-lab.sh <session> <lab> "notes"

# Reporting
export GITHUB_TOKEN=$(cat ~/.rajesh/.github_bu)
python3 reporting/generate-dashboard.py --output reporting/dashboard.html --auto-refresh
python3 reporting/track-lab-comments.py          # text report

# Presentation
firefox presentation/index.html
firefox presentation/session1-introduction-to-agentic-ai.html
```

## Lab Tracking

Participants submit via `submit-lab.sh` → GitHub Issue comment (label: `lab-tracking`).
Issues: `https://github.com/brainupgrade-in/aiagentic-comp/issues?q=label%3Alab-tracking`

## Error Recovery

| Issue | Fix |
|-------|-----|
| High memory | `check-resources.sh`; OOM unlikely with 16 GB unless multiple large models |
| Disk space | `du -sh ~/.ollama/models`; `ollama rm <model>` |
| Groq 429 | Wait 60s; stagger class starts |
| Port conflict | `sudo lsof -i :8000` or `:11434`; stop conflicting service |
| Package conflicts | `rm -rf .venv && python3 -m venv .venv && pip install -r requirements.txt` |

## Groq API

Free tier: ~1,000 req/min, ~250K tokens/min. `GROQ_API_KEY` in `.env`. LangChain: `langchain-groq` / `ChatGroq`.

## OpenCode (Optional)

```bash
curl -fsSL https://opencode.ai/install | bash
opencode 'your prompt'   # or just `opencode` for TUI
```
Auth: `/connect` → GitHub Copilot, or set `GROQ_API_KEY`. Tab switches `build`/`plan` agents.

## Git Remote

`https://github.com/brainupgrade-in/aiagentic-comp.git` · branch: `main` · auth: `gh auth login -h github.com`
