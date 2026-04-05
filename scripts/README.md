# Scripts

Setup, cleanup, and utility scripts for the 5-day Agentic AI course.

## Quick Start — First-Time Setup

Run once before Day 1. Creates `.venv`, installs all packages, registers the Jupyter kernel, and configures every notebook to auto-select it. Also activates the venv in your current shell:

```bash
source scripts/initial-setup.sh
```

After setup, edit `.env` and add your Groq API key:
```
GROQ_API_KEY=gsk_your_key_here
```

## Running Notebooks

1. Open any `.ipynb` file in VS Code — the kernel **auto-selects** (`Python 3 (Gheware Agentic AI)`)
2. Run cells with **Shift+Enter**
3. Fill in `# TODO` / `"___"` sections, then compare with `solutions/`

In any new terminal, activate the venv with:
```bash
source .venv/bin/activate
```

## Day-by-Day Scripts

Each day has a **setup** script (run at start) and a **cleanup** script (run at end).

| Day | Setup | Cleanup | Purpose |
|-----|-------|---------|---------|
| 1 | `day1-setup.sh` | `day1-cleanup.sh` | Ollama + llama3.2:1b (~2 GB) |
| 2 | `day2-setup.sh` | `day2-cleanup.sh` | Verify Groq API + LangChain |
| 3 | `day3-setup.sh` | `day3-cleanup.sh` | Verify LangGraph, stop servers |
| 4 | `day4-setup.sh` | `day4-cleanup.sh` | Verify OTel + FastAPI + LangFuse |
| 5 | `day5-setup.sh` | `day5-cleanup.sh` | MCP SDK, final cleanup |

```bash
bash scripts/day1-setup.sh        # Start of Day 1
bash scripts/day1-cleanup.sh      # End of Day 1
# ... same pattern for days 2-5
bash scripts/check-resources.sh   # Check memory/storage anytime
```

## Lab Submission

After completing a lab, submit your progress:

```bash
bash scripts/submit-lab.sh <session> <lab> ["optional notes"]

# Examples
bash scripts/submit-lab.sh 1 1
bash scripts/submit-lab.sh 2 3 "LCEL makes chaining elegant"
```

Requires: GitHub CLI (`gh`) authenticated with the token shared during Zoom. See `SUBMIT-LAB-GUIDE.md` for details.

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `initial-setup.sh` | One-time setup: venv, packages, Jupyter kernel, notebook config |
| `install-notebook.sh` | Re-run kernel registration + notebook config only (if needed) |
| `check-resources.sh` | Show memory, storage, running Python/uvicorn processes |
| `submit-lab.sh` | Submit lab completion to GitHub Issues |
| `test-langfuse-server.sh` | Verify LangFuse server works (instructor use) |
| `langfuse-server.py` | LangFuse-compatible server (FastAPI + SQLite) |
| `populate_langfuse_data.py` | Generate demo data for LangFuse dashboard (instructor use) |
| `create-lab-issues.py` | Create GitHub Issues for lab tracking (already run) |
| `reporting/track-lab-comments.py` | Track participant lab completion via issue comments |

### populate_langfuse_data.py

Instructor utility to populate the LangFuse dashboard with sample observability data before Session 12 Lab 09.

```bash
source .venv/bin/activate
python scripts/populate_langfuse_data.py
```

Requires `.env` with: `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_HOST`, `GROQ_API_KEY`

Generates: 35 traces, 15+ unique users, 70 LLM generations across Traces/Sessions/Users/Generations views.

## File Listing

```
scripts/
├── README.md                        ← You are here
├── SUBMIT-LAB-GUIDE.md              ← Lab submission instructions
├── README-langfuse-server.md        ← LangFuse server documentation
│
├── initial-setup.sh                 ← One-time setup (venv + packages + kernel + notebooks)
├── install-notebook.sh              ← Re-register kernel + reconfigure notebooks
├── install-jupyter-kernel.sh        ← Register Jupyter kernel only (no notebook reconfiguration)
├── set-notebook-kernels.sh          ← Force all notebooks to use gheware-agentic-ai kernel
├── check-resources.sh               ← Resource monitor
├── submit-lab.sh                    ← Lab submission to GitHub Issues
├── test-langfuse-server.sh          ← LangFuse server verification (instructor)
├── day1-setup.sh / day1-cleanup.sh  ← Ollama + local LLM
├── day2-setup.sh / day2-cleanup.sh  ← Groq API + LangChain
├── day3-setup.sh / day3-cleanup.sh  ← LangGraph
├── day4-setup.sh / day4-cleanup.sh  ← OTel + FastAPI + LangFuse
├── day5-setup.sh / day5-cleanup.sh  ← MCP SDK + final cleanup
│
├── langfuse-server.py               ← LangFuse-compatible server (Python + SQLite)
├── populate_langfuse_data.py        ← LangFuse demo data generator
├── configure-all-notebooks.py       ← Configure kernel in all notebooks (student + solutions)
├── configure-notebook-kernels.py    ← Configure kernel in solution notebooks only
├── setup-notebook-kernel.py         ← Register kernel + configure all notebooks (legacy helper)
├── create-lab-issues.py             ← Create GitHub Issues (already run once)
└── (track-lab-comments.py moved to reporting/)
```
