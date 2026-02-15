# Scripts

Setup, cleanup, and utility scripts for the 5-day Agentic AI course. Both **Bash** (Linux/macOS) and **PowerShell** (Windows) versions are provided.

## Quick Start — First-Time Setup

Run the initial setup script to install Python, create a virtual environment, and install all packages:

```bash
# Linux / macOS
bash scripts/initial-setup.sh

# Windows (PowerShell)
.\scripts\initial-setup.ps1
```

This handles: Python version check, virtual environment creation, `pip install -r requirements.txt`, and `.env` file setup.

## Notebook Setup

Labs use Jupyter notebooks (`.ipynb`). Run the appropriate script to install everything needed:

```bash
# Linux / macOS
bash scripts/install-notebook.sh

# Windows (PowerShell)
.\scripts\install-notebook.ps1
```

This installs the VS Code Jupyter extension, `ipykernel`, and verifies the setup with Python's `antigravity` Easter egg.

## Running Notebooks

1. Open any `.ipynb` file in VS Code
2. Select the Python kernel when prompted (`.venv/bin/python` from your virtual environment)
3. Run cells with **Shift+Enter**
4. Fill in TODO sections, then compare with `solutions/`

## Day-by-Day Scripts

Each day has a **setup** script (run at start of day) and a **cleanup** script (run at end of day) to ensure a clean environment between sessions.

| Day | Setup | Cleanup | Purpose |
|-----|-------|---------|---------|
| 1 | `day1-setup` | `day1-cleanup` | Ollama + llama3.2:1b (~2 GB) |
| 2 | `day2-setup` | `day2-cleanup` | Verify Groq API + LangChain |
| 3 | `day3-setup` | `day3-cleanup` | Verify LangGraph, stop servers |
| 4 | `day4-setup` | `day4-cleanup` | Verify OTel + FastAPI + LangFuse + start LangFuse server |
| 5 | `day5-setup` | `day5-cleanup` | Install MCP SDK, final cleanup |

### Linux / macOS

```bash
bash scripts/day1-setup.sh        # Start of Day 1
bash scripts/day1-cleanup.sh      # End of Day 1
# ... same pattern for days 2-5
bash scripts/check-resources.sh   # Check memory/storage anytime
```

### Windows (PowerShell)

```powershell
.\scripts\day1-setup.ps1          # Start of Day 1
.\scripts\day1-cleanup.ps1        # End of Day 1
# ... same pattern for days 2-5
.\scripts\check-resources.ps1     # Check memory/storage anytime
```

> **Note:** If PowerShell blocks script execution, run this once:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

## Lab Submission

After completing a lab, submit your progress using the submit script:

```bash
# Linux / macOS
bash scripts/submit-lab.sh <session> <lab> ["optional notes"]
bash scripts/submit-lab.sh 1 1 "Great lab!"

# Windows (PowerShell)
.\scripts\submit-lab.ps1 <session> <lab> ["optional notes"]
.\scripts\submit-lab.ps1 1 1 "Great lab!"
```

Requires: GitHub CLI (`gh`) authenticated. See `SUBMIT-LAB-GUIDE.md` for details.

## Utility Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| `initial-setup` | .sh / .ps1 | One-time setup: Python, venv, packages, .env |
| `check-resources` | .sh / .ps1 | Show memory, storage, running Python processes |
| `install-notebook` | .sh / .ps1 | Install VS Code Jupyter extension + ipykernel |
| `install-jupyter-kernel` | .sh / .ps1 | Install named Jupyter kernel spec for the course |
| `submit-lab` | .sh / .ps1 | Submit lab completion to GitHub Issues |
| `test-langfuse-server` | .sh / .ps1 | Verify LangFuse server works (instructor use) |
| `langfuse-server.py` | Python | LangFuse-compatible server (FastAPI + SQLite) |
| `populate_langfuse_data.py` | Python | Generate demo data for LangFuse dashboard |

### populate_langfuse_data.py

**Purpose:** Instructor utility to populate LangFuse cloud dashboard with comprehensive observability data for Session 12 Lab 09 demonstrations.

**Usage:**
```bash
source .venv/bin/activate
python scripts/populate_langfuse_data.py
```

**Prerequisites:**
- `.env` file with: `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_HOST`, `GROQ_API_KEY`
- Packages: `langfuse`, `langchain-groq`, `langgraph`, `python-dotenv`

**Generated Data:**
- 35 traces with user_id and session_id
- 15+ unique users (Priya, Vikram, Amit, etc.)
- 15-20 sessions (including multi-turn conversations)
- 70 LLM generations (supervisor + worker)

**Populates:** Traces, Sessions, Users, and Generations views in LangFuse dashboard

**When to Use:** Before Session 12 to show students a fully populated observability dashboard

## File Listing

```
scripts/
├── README.md                        ← You are here
├── SUBMIT-LAB-GUIDE.md              ← Lab submission instructions
├── README-langfuse-server.md        ← LangFuse server documentation
│
├── initial-setup.sh / .ps1          ← One-time environment setup
├── install-notebook.sh / .ps1       ← Jupyter notebook setup
├── install-jupyter-kernel.sh / .ps1 ← Named kernel spec installation
├── check-resources.sh / .ps1        ← Resource monitor
├── submit-lab.sh / .ps1             ← Lab submission to GitHub
├── test-langfuse-server.sh / .ps1   ← LangFuse server verification
│
├── day1-setup.sh / .ps1             ← Ollama + local LLM
├── day1-cleanup.sh / .ps1           ← Remove Ollama (~2 GB freed)
├── day2-setup.sh / .ps1             ← Groq API + LangChain verification
├── day2-cleanup.sh / .ps1           ← Clean temp files
├── day3-setup.sh / .ps1             ← LangGraph verification
├── day3-cleanup.sh / .ps1           ← Stop servers + clean temp files
├── day4-setup.sh / .ps1             ← OTel + FastAPI + LangFuse + server startup
├── day4-cleanup.sh / .ps1           ← Stop LangFuse + FastAPI + clean temp files
├── day5-setup.sh / .ps1             ← MCP SDK install
├── day5-cleanup.sh / .ps1           ← Final cleanup
│
├── langfuse-server.py               ← LangFuse-compatible server (Python + SQLite)
├── populate_langfuse_data.py        ← LangFuse demo data generator
├── create-lab-issues.py             ← Create GitHub Issues for lab tracking
├── track-lab-comments.py            ← Track participant lab comments
├── configure-all-notebooks.py       ← Configure notebook metadata
├── configure-notebook-kernels.py    ← Set kernel specs in notebooks
└── setup-notebook-kernel.py         ← Kernel spec setup utility
```
