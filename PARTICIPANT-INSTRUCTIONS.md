# Participant Instructions — Agentic AI Course

5-day course, 15 sessions, 119 labs. Fill in `___` placeholders in notebooks, get all `[PASS]`, submit each lab.

---

## One-Time Setup

Run **once** before Day 1. It installs everything all five days need — Python 3.12,
the `.venv`, every package, the Jupyter kernel, and the Day 1 local LLM. There are
no per-day setup scripts.

### Windows — one script

Download the repo as a ZIP (or clone it if you already have git), then in **PowerShell**
from the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
```

It installs Git for Windows (which gives you **Git Bash** and `curl`), `uv`, and Ollama,
then runs `scripts/setup.sh` under Git Bash. **Use Git Bash for every command after this.**

> If it says a tool "not found after install", close PowerShell, open a **new** window,
> and re-run — Windows only refreshes PATH for new processes.

### Linux / macOS

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
source scripts/setup.sh
```

### GitHub Codespaces / Dev Container (alternative to the above)

Nothing to install locally — open the repo in a Codespace, or in VS Code run
**Dev Containers: Reopen in Container**.

The container is configured to attach in **seconds**, which means setup is *not*
automatic. Run this **once** in the container terminal:

```bash
source scripts/setup.sh --skip-ollama
```

`--skip-ollama` is correct here: Codespaces has no GPU and limited disk, and Days
2-5 use Groq anyway. **Day 1 labs need Ollama**, so either run plain
`source scripts/setup.sh` (slow, large download) or do Day 1 on your own machine.

> If your `GROQ_API_KEY` / `GITHUB_TOKEN` are stored as Codespaces secrets, run
> `bash .devcontainer/post-create.sh` instead — same setup, plus it copies those
> secrets into `.env` for you.

The Codespace picks GitHub's default machine type. If a day feels short on memory,
use **Codespaces → Change machine type** to bump it — 4 CPU / 8 GB is comfortable.

### Then add your keys

```bash
code .env    # or: nano .env (Linux/Mac)  |  notepad .env (Windows)
```

> `.env` is gitignored.

You need **two free accounts of your own** — sign up before Day 2 and Day 4:

| Key | Where to get it | Needed for |
|-----|-----------------|------------|
| `GROQ_API_KEY` | https://console.groq.com | Days 2-5 (all LLM calls) |
| `LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` | https://cloud.langfuse.com → create a project → Settings → API Keys | Day 4, Session 12 Lab 09 |

Leave `LANGFUSE_HOST=https://cloud.langfuse.com` as-is. Session 12 Labs 01-08 run
in mock mode and need no LangFuse keys — only Lab 09 sends real traces.

Check the environment any time:

```bash
bash scripts/setup.sh --verify
```

---

## Identity & Token (Required for Lab Submission)

Do all four steps **once, before Day 1**, from inside the repo directory.

**1. Make sure you have a real clone, not a ZIP.** `submit-lab.sh` reads your name
from the repo's git config, so an unzipped folder can't submit. If you started from
a ZIP on Windows, clone the repo now and re-run `scripts/setup.sh` inside the clone:

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
```

**2. Set your identity** — nothing in setup does this for you, and submission fails
without it:

```bash
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

**3. Add the GitHub token** shared by the instructor to `.env`:

```bash
echo 'GITHUB_TOKEN=ghp_xxxx' >> .env
```

> Token needs `public_repo` scope. Replacing the `ghp_your_lab_submit_token_here`
> placeholder that setup wrote is fine — leaving it in place is treated as "no token".

**4. Dry-run the check.** Everything before the confirmation prompt is a pre-flight
check, so run this and answer `N`:

```bash
bash scripts/submit-lab.sh 1 1        # answer N at the "Submit this lab?" prompt
```

You should see your username and `✓ GitHub token found`. (Whether the token is
*valid* is only known on a real submission — do your first one early on Day 1.)

> **Windows (Git Bash):** activate the venv before submitting —
> `source .venv/Scripts/activate` — the script needs Python on `PATH` to build the
> request, and Git Bash has none of its own.

---

## Daily Workflow

```bash
git pull
source .venv/bin/activate            # Windows Git Bash: source .venv/Scripts/activate
```

That's it — the one-time setup already covered all five days.

Open labs in VS Code (`code .`), complete all `___` TODOs, run all cells.
Kernel: **Python 3 (Gheware Agentic AI)**. If missing: `bash scripts/setup.sh --kernel-only` then reload VS Code.

**First time you open the repo in VS Code**, accept the *"install recommended
extensions"* prompt (or run **Extensions: Show Recommended Extensions**). The repo
ships tuned workspace settings in `.vscode/` that work the same on Windows, macOS
and Linux — correct notebook output limits, LF line endings, `.venv` excluded from
file watching. You don't need to configure anything; your personal VS Code *User*
settings still win over these.

Day 4, before Session 12 Lab 09: make sure your own LangFuse Cloud keys are in
`.env` (see the table above), then confirm with `bash scripts/setup.sh --verify`.

Submit each lab when done:

```bash
bash scripts/submit-lab.sh <session> <lab> "optional notes"
# e.g. bash scripts/submit-lab.sh 1 2 "RAG pipeline working"
```

The script auto-detects your username, shows a preview, and confirms before posting.

End-of-day cleanup (optional): `bash scripts/cleanup.sh <day>` — e.g. `bash scripts/cleanup.sh 4`

### Session Checklist
- [ ] All validation cells show `[PASS]`
- [ ] All labs submitted via `submit-lab.sh`

---

## Lab Structure

| Path | Purpose |
|------|---------|
| `hands-on/session-N/labXX_topic.ipynb` | Student lab (`___` TODOs) |
| `hands-on/session-N/solutions/labXX_topic.ipynb` | Reference solution |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `source .venv/bin/activate` (or `Scripts/activate` on Windows), then `bash scripts/setup.sh --verify` |
| Wrong kernel | `bash scripts/setup.sh --kernel-only` → reload VS Code |
| Groq 429 | Wait 60s, retry; stagger class starts if widespread |
| `GITHUB_TOKEN not set` | Add to `.env` or `export GITHUB_TOKEN=ghp_xxxx` |
| `Could not detect username` | `git config user.name "your-github-username"` |
| Submission failed / token expired | Get new token from instructor, update `.env` |
| Port conflict | `sudo lsof -i :8000` or `:11434`; stop the conflicting process |
| Lab 09 traces not appearing | Check `LANGFUSE_HOST=https://cloud.langfuse.com` and your own keys are in `.env`; `bash scripts/setup.sh --verify` |
| Wrong Python version | `bash scripts/setup.sh` — recreates `.venv` on Python 3.12 |
| `uv: command not found` (Windows) | Run `scripts\bootstrap.ps1` in PowerShell first |
| `$'\r': command not found` (Windows) | CRLF got into a `.sh` file — only happens on clones made before `.gitattributes` was added. Fix in place: `git pull && git rm --cached -r . && git reset --hard` |
| No kernel in a Codespace | Setup isn't automatic there — run `source scripts/setup.sh --skip-ollama` once |
| VS Code nags to install Copilot | Ignore it — the course doesn't use Copilot and it errors without a subscription |

Debug GitHub token:
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/brainupgrade-in/aiagentic-comp/issues/1 \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('title', d.get('message')))"
```

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
