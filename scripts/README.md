# Scripts

Setup, cleanup, and utility scripts for the 5-day Agentic AI course.

There are **no per-day setup scripts**. `setup.sh` installs everything all five
days need in one pass, and is idempotent — re-run it any time.

## One-Time Setup

### Windows

One script. Run it in PowerShell from the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
```

It installs Git for Windows (Git Bash + curl), uv, and Ollama, then runs
`scripts/setup.sh` under Git Bash. Use Git Bash for everything afterwards.

Add `-SkipOllama` to skip the Day 1 local LLM (~2 GB).

### Linux / macOS

```bash
source scripts/setup.sh
```

(`source` leaves the venv active in your shell; `bash scripts/setup.sh` also works.)

Then add your Groq API key to `.env`:

```
GROQ_API_KEY=gsk_your_key_here      # free at https://console.groq.com
```

### What setup.sh does

| Step | Detail |
|------|--------|
| 1 | Installs `uv` if missing (Linux/macOS; Windows gets it from `bootstrap.ps1`) |
| 2 | `uv python install 3.12` — no sudo, no PPA, no Homebrew needed |
| 3 | Creates `.venv` with Python 3.12 (recreates it if the version is wrong) |
| 4 | Installs **all 5 days** of packages, CPU-only PyTorch first to avoid multi-GB CUDA wheels |
| 5 | Creates `.env` from `.env.example` (never overwrites an existing one) |
| 6 | Registers the `gheware-agentic-ai` Jupyter kernel and points every notebook at it |
| 7 | Installs Ollama + pulls `llama3.2:1b` (Day 1), plus OpenCode (optional) |

Flags:

```bash
bash scripts/setup.sh --verify        # check the environment, install nothing
bash scripts/setup.sh --skip-ollama   # skip the Day 1 local LLM
bash scripts/setup.sh --kernel-only   # re-register the kernel + reconfigure notebooks
```

`--verify` replaces the old per-day setup scripts: it reports the venv, every
package grouped by the day that needs it, the kernel, the API keys, and Ollama.

## Running Notebooks

1. Open any `.ipynb` in VS Code — the kernel **auto-selects** (`Python 3 (Gheware Agentic AI)`)
2. Run cells with **Shift+Enter**
3. Fill in `# TODO` / `"___"` sections, then compare with `solutions/`

In any new terminal:

```bash
source .venv/bin/activate          # Windows Git Bash: source .venv/Scripts/activate
```

## Daily Cleanup

Optional. Stops that day's servers and removes its `/tmp` lab dirs. The `.venv`
and all packages are never touched, so there is nothing to reinstall tomorrow.

```bash
bash scripts/cleanup.sh 1              # Day 1: stop Ollama, clear temp dirs
bash scripts/cleanup.sh 4              # Day 4: stop LangFuse, drop its DB + logs
bash scripts/cleanup.sh                # all days (end of course)
bash scripts/cleanup.sh 1 --purge-ollama   # also delete Ollama + the model (~2 GB)
```

Day 4 is the one worth running — it stops the LangFuse server and deletes
`/tmp/langfuse.db`.

## LangFuse Server (Day 4, Session 12 Lab 09)

```bash
bash scripts/langfuse-server.sh start    # http://localhost:3000
bash scripts/langfuse-server.sh status
bash scripts/langfuse-server.sh stop
```

Labs 01-08 of Session 12 use MockLangfuse (local JSON) and need no server.

## Lab Submission

```bash
bash scripts/submit-lab.sh <session> <lab> ["optional notes"]

# Examples
bash scripts/submit-lab.sh 1 1
bash scripts/submit-lab.sh 2 3 "LCEL makes chaining elegant"
```

Requires `GITHUB_TOKEN` in `.env` or exported. Auto-detects your username, shows
a preview, confirms before posting. See `PARTICIPANT-INSTRUCTIONS.md`.

## File Listing

```
scripts/
├── README.md                     ← You are here
├── README-langfuse-server.md     ← LangFuse server internals
│
│  Participant
├── bootstrap.ps1                 ← Windows: Git Bash + uv + Ollama, then setup.sh
├── setup.sh                      ← All platforms: Python 3.12, venv, all 5 days of
│                                   packages, .env, kernel, notebooks, Ollama, OpenCode
├── cleanup.sh                    ← End-of-day cleanup: cleanup.sh [1-5|all]
├── submit-lab.sh                 ← Submit a lab to GitHub Issues
├── check-resources.sh            ← Memory / storage / running processes
│
│  Shared
├── configure-notebooks.py        ← Point every notebook at the course kernel
├── langfuse-server.sh            ← start | stop | status for the LangFuse server
│
│  Instructor
├── langfuse-server.py            ← LangFuse-compatible server (FastAPI + SQLite)
├── populate_langfuse_data.py     ← Demo data for the LangFuse dashboard
├── test-langfuse-server.sh       ← Verify the LangFuse server works
└── create-lab-issues.py          ← Create the lab-tracking GitHub Issues (already run)
```

### populate_langfuse_data.py

Instructor utility to populate the LangFuse dashboard with sample observability
data before Session 12 Lab 09.

```bash
source .venv/bin/activate
python scripts/populate_langfuse_data.py
```

Requires `.env` with `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`,
`LANGFUSE_HOST`, `GROQ_API_KEY`. Generates 35 traces, 15+ users, 70 LLM
generations across the Traces/Sessions/Users/Generations views.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | `source .venv/bin/activate`, then `bash scripts/setup.sh --verify` |
| Wrong / missing kernel | `bash scripts/setup.sh --kernel-only` → reload VS Code |
| Wrong Python version | `bash scripts/setup.sh` — recreates `.venv` on 3.12 |
| `uv: command not found` (Windows) | Run `scripts\bootstrap.ps1` from PowerShell first |
| Port 3000 in use | `bash scripts/langfuse-server.sh stop` |
| Port 8000 or 11434 in use | `sudo lsof -i :8000`; stop the conflicting process |
| Groq 429 | Wait 60s; stagger class starts |
| Low memory / disk | `bash scripts/check-resources.sh`, then `bash scripts/cleanup.sh` |
