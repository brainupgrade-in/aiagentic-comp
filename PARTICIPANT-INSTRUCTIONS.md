# Participant Instructions — Agentic AI Course

## Overview

5-day hands-on course. Each session has Jupyter notebook labs with `TODO` placeholders to fill in.
Labs are submitted by commenting on GitHub Issues using the `submit-lab.sh` script.

**Before Day 1:** Complete the one-time setup below for your OS.

---

## One-Time Setup

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp

# Run setup (creates .venv, installs packages, registers Jupyter kernel)
source scripts/initial-setup.sh

# Edit .env and add your Groq API key
# Get one free at https://console.groq.com
nano .env   # or open in VS Code
```

### Windows (Git Bash)

1. Install **Git for Windows** from https://git-scm.com/download/win — this includes Git Bash
2. Open **Git Bash** (search "Git Bash" in the Start menu)
3. Run the same setup as Linux/macOS:

```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
source scripts/initial-setup.sh
nano .env   # or open in VS Code
```

> **Always use Git Bash** for all course scripts — not PowerShell or Command Prompt.

> **Activating the venv on Windows Git Bash:** Python on Windows creates the venv under `Scripts/` instead of `bin/`. Use:
> ```bash
> source .venv/Scripts/activate
> ```

---

## Setting Up Your Identity (Required for Lab Submission)

```bash
cd aiagentic-comp

git config user.name "your-github-username"
git config user.email "your-email@example.com"

# Verify
git config user.name
git config user.email
```

Use your **actual GitHub username** — this is how you appear in the instructor dashboard.

---

## GitHub Token Setup (Required for Lab Submission)

You will receive a shared access token during the Zoom session. Add it to `.env`:

```bash
echo 'GITHUB_TOKEN=ghp_xxxx' >> .env
```

Or export it for the session:

```bash
export GITHUB_TOKEN=ghp_xxxx
```

> The token needs **`public_repo`** scope. `.env` is gitignored — your token stays local.
>
> Token resolution order: environment variable first, then `.env` file.

---

## Opening Labs in VS Code

All labs are Jupyter notebooks (`.ipynb`). Open VS Code from the repo root:

```bash
code .
```

Navigate to `hands-on/session-1/lab01_meet_your_llm.ipynb` and open it.

**Kernel selection:** The setup script pre-configures every notebook to use the
`Python 3 (Gheware Agentic AI)` kernel (your `.venv`). If VS Code prompts you to
select a kernel, choose **Python 3 (Gheware Agentic AI)** from the list.

> If the kernel is missing after a fresh setup, run:
> ```bash
> bash scripts/set-notebook-kernels.sh
> ```
> Then reload VS Code: `Ctrl+Shift+P` → `Developer: Reload Window`.

---

## Daily Workflow

### 1. Pull Latest Updates

```bash
cd aiagentic-comp   # or wherever you cloned the repo
git pull
source .venv/bin/activate   # Linux/macOS
# Windows Git Bash: source .venv/Scripts/activate
```

### 2. Run Day Setup Script

```bash
bash scripts/day1-setup.sh   # Day 1 (Ollama + local LLM)
bash scripts/day2-setup.sh   # Day 2 (verify Groq + LangChain)
bash scripts/day3-setup.sh   # Day 3 (verify LangGraph)
bash scripts/day4-setup.sh   # Day 4 (OTel + LangFuse + FastAPI)
bash scripts/day5-setup.sh   # Day 5 (MCP SDK)
```

### 3. Complete Labs

Open the notebook in VS Code, fill in `___` placeholders, and run all cells.
Each lab ends with `[PASS]` / `[FAIL]` validation cells — aim for all `[PASS]`.

### 4. Submit Each Lab

```bash
bash scripts/submit-lab.sh <session> <lab> "optional notes"

# Examples
bash scripts/submit-lab.sh 1 1
bash scripts/submit-lab.sh 1 2 "Learned about reasoning patterns"
bash scripts/submit-lab.sh 2 5 "RAG pipeline working"
```

The script auto-detects your username from git config, shows a preview, and asks for confirmation before posting.

**Sample output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Lab Submission - Agentic AI Course
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 1  Lab: 1  Issue Number: #1

✓ Username: johndoe
✓ GitHub token found

Comment Preview:
✅ Completed
**Participant:** johndoe (johndoe@example.com)
**Validation:** All checks passed

Submit this lab? (y/N): y

✓ Submission Successful!
Comment: https://github.com/brainupgrade-in/aiagentic-comp/issues/1#issuecomment-...
```

### 5. End-of-Day Cleanup (Optional)

```bash
bash scripts/day1-cleanup.sh   # frees ~2 GB (removes Ollama model)
bash scripts/day2-cleanup.sh
# etc.
```

### End-of-Session Checklist

- [ ] All lab notebooks run without errors
- [ ] All validation cells show `[PASS]`
- [ ] Submitted all labs using `submit-lab.sh`
- [ ] Verified submissions on GitHub

---

## Lab Structure

| Path | Purpose |
|------|---------|
| `hands-on/session-N/labXX_topic.ipynb` | Lab to complete (has `___` TODOs) |
| `hands-on/session-N/solutions/labXX_topic.ipynb` | Reference solution |

Labs build progressively within each session. The last lab in each session is a challenge lab.

### Issue Number Reference

The script calculates the issue number automatically:

| Session | Lab Range | Issue Range |
|---------|-----------|-------------|
| 1 | 1–6 | #1 – #6 |
| 2 | 1–9 | #7 – #15 |
| 3 | 1–7 | #16 – #22 |
| 4 | 1–8 | #23 – #30 |
| 5 | 1–8 | #31 – #38 |
| 6 | 1–8 | #39 – #46 |
| 7 | 1–8 | #47 – #54 |
| 8 | 1–8 | #55 – #62 |
| 9 | 1–8 | #63 – #70 |
| 10 | 1–8 | #71 – #78 |
| 11 | 1–8 | #79 – #86 |
| 12 | 1–9 | #87 – #95 |
| 13 | 1–8 | #96 – #103 |
| 14 | 1–8 | #104 – #111 |
| 15 | 1–8 | #112 – #119 |

---

## Troubleshooting

### `ModuleNotFoundError` in notebooks

Virtual environment not active.

```bash
source .venv/bin/activate          # Linux/macOS
source .venv/Scripts/activate      # Windows Git Bash
```

### Kernel shows wrong Python / "Unable to handle ... Oracle/.venv"

Another workspace's kernel is cached. Run:

```bash
bash scripts/set-notebook-kernels.sh
```

Then reload VS Code (`Ctrl+Shift+P` → `Developer: Reload Window`).

### Groq rate limit (429 error)

Free tier limit hit. Wait 60 seconds and retry. If the whole class hits limits simultaneously, stagger lab start times by a few minutes.

### "GITHUB_TOKEN not set"

```bash
echo 'GITHUB_TOKEN=ghp_xxxx' >> .env
# or
export GITHUB_TOKEN=ghp_xxxx
```

### "Could not detect GitHub username"

```bash
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

### "Submission Failed" / token expired

Ask the instructor for a new token, update `.env`, then retry.

To debug the token manually:

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/brainupgrade-in/aiagentic-comp/issues/1 \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('title', d.get('message')))"
```

### Port conflict (8000 or 11434 already in use)

```bash
sudo lsof -i :8000
sudo lsof -i :11434
```

Stop the conflicting process, then re-run the day setup script.

---

## Advanced

### Batch Submission

```bash
for lab in {1..6}; do
  bash scripts/submit-lab.sh 1 $lab
  sleep 1
done
```

### Shell Alias

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias submit-lab='cd /path/to/aiagentic-comp && bash scripts/submit-lab.sh'
```

Then use from anywhere: `submit-lab 1 1`

---

## Session Summary

| Day | Sessions | Key Tech |
|-----|----------|----------|
| 1 | 1–3 | Ollama, ReAct, Chain-of-Thought |
| 2 | 4–6 | LangChain, LCEL, ChromaDB, RAG |
| 3 | 7–9 | LangGraph, Multi-Agent |
| 4 | 10–12 | OTel, LangFuse, FastAPI |
| 5 | 13–15 | MCP, AI Safety, Capstone |

---

## Quick Reference

```bash
# One-time setup
source scripts/initial-setup.sh

# Daily
git pull && source .venv/bin/activate
bash scripts/dayN-setup.sh

# Submit a lab
bash scripts/submit-lab.sh <session> <lab> "notes"

# Check resource usage
bash scripts/check-resources.sh
```

---

**Course Repository:** https://github.com/brainupgrade-in/aiagentic-comp  
**Lab Issues:** https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking  
**Groq API Keys:** https://console.groq.com  

**Questions?** Ask in Zoom chat during sessions or raise your hand.
