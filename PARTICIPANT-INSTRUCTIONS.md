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

### Windows

Open **PowerShell** (not Command Prompt) in the repo folder and run:

```powershell
# Allow script execution (one-time)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force

# Clone the repository
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp

# Bootstrap: installs Git Bash if needed, configures VS Code, runs initial-setup.sh
.\scripts\windows-bootstrap.ps1
```

This script:
- Installs **Git for Windows** (Git Bash) automatically via `winget` if not present
- Configures **VS Code** to use Git Bash as the default integrated terminal
- Runs `initial-setup.sh` through Git Bash — same setup as Linux/Mac

After bootstrap, **always use the Git Bash terminal in VS Code** to run course scripts.

> **No Git / winget?** Install Git for Windows manually from https://git-scm.com/download/win, then re-run the bootstrap script.

---

## Setting Up Your Identity (Required for Lab Submission)

```bash
cd ~/aiagentic-comp   # or cd aiagentic-comp on Windows Git Bash

git config user.name "your-github-username"
git config user.email "your-email@example.com"

# Verify
git config user.name
git config user.email
```

Use your **actual GitHub username** — this is how you appear in the instructor dashboard.

---

## GitHub CLI Authentication (Required for Lab Submission)

You will receive a shared access token during the Zoom session.

```bash
gh auth login
# Select: GitHub.com → HTTPS → Paste an authentication token
# Paste the token shared by the instructor

# Verify
gh auth status
```

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
cd ~/aiagentic-comp
git pull
source .venv/bin/activate   # Linux/macOS
# Windows Git Bash: source .venv/Scripts/activate
```

### 2. Run Day Setup Script

```bash
bash scripts/day1-setup.sh   # Day 1 (Ollama + local LLM)
bash scripts/day2-setup.sh   # Day 2 (verify Groq + LangChain)
bash scripts/day3-setup.sh   # Day 3 (verify LangGraph)
bash scripts/day4-setup.sh   # Day 4 (start LangFuse server)
bash scripts/day5-setup.sh   # Day 5 (MCP SDK)
```

### 3. Complete Labs

Open the notebook in VS Code, fill in `___` placeholders, and run all cells.
Each lab ends with `[PASS]` / `[FAIL]` validation cells — aim for all `[PASS]`.

### 4. Submit Each Lab

```bash
# Linux / macOS / Windows Git Bash
bash scripts/submit-lab.sh <session> <lab> "optional notes"

# Examples
bash scripts/submit-lab.sh 1 1
bash scripts/submit-lab.sh 1 2 "Learned about reasoning patterns"
bash scripts/submit-lab.sh 2 5 "RAG pipeline working"
```

The script auto-detects your GitHub username, shows a preview, and asks for confirmation before posting.

### 5. End-of-Day Cleanup (Optional)

```bash
bash scripts/day1-cleanup.sh   # frees ~2 GB (removes Ollama model)
bash scripts/day2-cleanup.sh
# etc.
```

---

## Lab Structure

| Path | Purpose |
|------|---------|
| `hands-on/session-N/labXX_topic.ipynb` | Lab to complete (has `___` TODOs) |
| `hands-on/session-N/solutions/labXX_topic.ipynb` | Reference solution |

Labs build progressively within each session. The last lab in each session is a challenge lab.

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

### `gh: command not found`

```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Windows — already included in Git for Windows (Git Bash)
```

### "Resource not accessible by personal access token"

Token expired. Ask the instructor for a new token, then re-authenticate:

```bash
gh auth login
```

### "Could not detect GitHub username"

Git config not set. Re-run the identity setup:

```bash
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

### Port conflict (8000 or 11434 already in use)

```bash
sudo lsof -i :8000    # find what's using port 8000
sudo lsof -i :11434   # find what's using Ollama port
```

Stop the conflicting process, then re-run the day setup script.

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
source scripts/initial-setup.sh          # Linux/macOS
.\scripts\windows-bootstrap.ps1          # Windows PowerShell

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
