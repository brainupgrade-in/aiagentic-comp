# Scripts

Setup, cleanup, and utility scripts for the 5-day Agentic AI course. Both **Bash** (Linux/macOS/Codespaces) and **PowerShell** (Windows) versions are provided.

## Quick Start — Notebook Setup

Labs use Jupyter notebooks (`.ipynb`). Run the appropriate script to install everything needed:

```bash
# Linux / macOS / Codespaces
bash scripts/install-notebook.sh

# Windows (PowerShell)
.\scripts\install-notebook.ps1
```

This installs the VS Code Jupyter extension, `ipykernel`, and verifies the setup with Python's `antigravity` Easter egg.

## Running Notebooks

1. Open any `.ipynb` file in VS Code
2. Select the Python kernel when prompted (`~/.venv/bin/python` on Codespaces, or your local venv)
3. Run cells with **Shift+Enter**
4. Fill in TODO sections, then compare with `solutions/`

## Day-by-Day Scripts

Each day has a **setup** script (run at start of day) and a **cleanup** script (run at end of day) to manage the 8 GB RAM / 32 GB storage Codespace constraints.

| Day | Setup | Cleanup | Purpose |
|-----|-------|---------|---------|
| 1 | `day1-setup` | `day1-cleanup` | Ollama + llama3.2:1b (~2 GB) |
| 2 | `day2-setup` | `day2-cleanup` | Verify Groq API + LangChain |
| 3 | `day3-setup` | `day3-cleanup` | Verify LangGraph, stop servers |
| 4 | `day4-setup` | `day4-cleanup` | Verify OTel + FastAPI + LangFuse |
| 5 | `day5-setup` | `day5-cleanup` | Install MCP SDK, final cleanup |

### Linux / macOS / Codespaces

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

## Utility Scripts

| Script | Purpose |
|--------|---------|
| `check-resources` | Show memory, storage, running Python processes, top consumers |
| `install-notebook` | Install VS Code Jupyter extension + ipykernel + verify setup |

## File Listing

```
scripts/
├── README.md                  ← You are here
├── install-notebook.sh        ← Notebook setup (Linux/macOS/Codespaces)
├── install-notebook.ps1       ← Notebook setup (Windows)
├── check-resources.sh         ← Resource monitor (Linux/macOS/Codespaces)
├── check-resources.ps1        ← Resource monitor (Windows)
├── day1-setup.sh / .ps1       ← Ollama + local LLM
├── day1-cleanup.sh / .ps1     ← Remove Ollama (~2 GB freed)
├── day2-setup.sh / .ps1       ← Groq API + LangChain verification
├── day2-cleanup.sh / .ps1     ← Clean temp files
├── day3-setup.sh / .ps1       ← LangGraph verification
├── day3-cleanup.sh / .ps1     ← Stop servers + clean temp files
├── day4-setup.sh / .ps1       ← OTel + FastAPI + LangFuse verification
├── day4-cleanup.sh / .ps1     ← Stop FastAPI + clean temp files
├── day5-setup.sh / .ps1       ← MCP SDK install
└── day5-cleanup.sh / .ps1     ← Final cleanup
```
