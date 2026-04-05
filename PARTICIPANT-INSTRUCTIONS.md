# Participant Instructions — Agentic AI Course

5-day course, 15 sessions, 119 labs. Fill in `___` placeholders in notebooks, get all `[PASS]`, submit each lab.

---

## One-Time Setup

**Windows:** Install [Git for Windows](https://git-scm.com/download/win) and use Git Bash for all commands.

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
source scripts/initial-setup.sh      # creates .venv, installs packages, registers kernel
nano .env                             # add GROQ_API_KEY (get free at https://console.groq.com)
```

> Windows Git Bash: activate venv with `source .venv/Scripts/activate` (not `bin/`).

---

## Identity & Token (Required for Lab Submission)

```bash
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

Add the GitHub token shared by the instructor to `.env`:

```bash
echo 'GITHUB_TOKEN=ghp_xxxx' >> .env
```

Or export it: `export GITHUB_TOKEN=ghp_xxxx`

> Token needs `public_repo` scope. `.env` is gitignored.

---

## Daily Workflow

```bash
git pull
source .venv/bin/activate            # Windows: source .venv/Scripts/activate
bash scripts/dayN-setup.sh           # N = 1..5
```

Open labs in VS Code (`code .`), complete all `___` TODOs, run all cells.
Kernel: **Python 3 (Gheware Agentic AI)**. If missing: `bash scripts/set-notebook-kernels.sh` then reload VS Code.

Submit each lab when done:

```bash
bash scripts/submit-lab.sh <session> <lab> "optional notes"
# e.g. bash scripts/submit-lab.sh 1 2 "RAG pipeline working"
```

The script auto-detects your username, shows a preview, and confirms before posting.

End-of-day cleanup (optional): `bash scripts/dayN-cleanup.sh`

### Session Checklist
- [ ] All validation cells show `[PASS]`
- [ ] All labs submitted via `submit-lab.sh`

---

## Lab Structure

| Path | Purpose |
|------|---------|
| `hands-on/session-N/labXX_topic.ipynb` | Student lab (`___` TODOs) |
| `hands-on/session-N/solutions/labXX_topic.ipynb` | Reference solution |

### Session → Issue Mapping

| Session | Labs | Issues |
|---------|------|--------|
| 1 | 1–6 | #1–6 |
| 2 | 1–9 | #7–15 |
| 3 | 1–7 | #16–22 |
| 4–11 | 1–8 each | #23–86 |
| 12 | 1–9 | #87–95 |
| 13–15 | 1–8 each | #96–119 |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `source .venv/bin/activate` (or `Scripts/activate` on Windows) |
| Wrong kernel | `bash scripts/set-notebook-kernels.sh` → reload VS Code |
| Groq 429 | Wait 60s, retry; stagger class starts if widespread |
| `GITHUB_TOKEN not set` | Add to `.env` or `export GITHUB_TOKEN=ghp_xxxx` |
| `Could not detect username` | `git config user.name "your-github-username"` |
| Submission failed / token expired | Get new token from instructor, update `.env` |
| Port conflict | `sudo lsof -i :8000` or `:11434`; stop the conflicting process |

Debug token: `curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/brainupgrade-in/aiagentic-comp/issues/1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('title', d.get('message')))"`

---

## Course Map

| Day | Sessions | Tech |
|-----|----------|------|
| 1 | 1–3 | Ollama, ReAct, Chain-of-Thought |
| 2 | 4–6 | LangChain, LCEL, ChromaDB, RAG |
| 3 | 7–9 | LangGraph, Multi-Agent |
| 4 | 10–12 | OTel, LangFuse, FastAPI |
| 5 | 13–15 | MCP, AI Safety, Capstone |

---

**Repo:** https://github.com/brainupgrade-in/aiagentic-comp  
**Lab Issues:** https://github.com/brainupgrade-in/aiagentic-comp/issues?q=label:lab-tracking  
**Groq Keys:** https://console.groq.com · **Questions?** Ask in Zoom chat.
