# initial-setup.ps1 — One-time environment setup for Windows (PowerShell)
# Sets up Python venv, installs all packages, registers the Jupyter kernel,
# and configures every notebook to auto-select it.
#
# Usage (from repo root, in PowerShell):
#   .\scripts\initial-setup.ps1
#
# Run this ONCE before Day 1.

$ErrorActionPreference = "Stop"

$KERNEL_NAME    = "gheware-agentic-ai"
$KERNEL_DISPLAY = "Python 3 (Gheware Agentic AI)"

$REPO_DIR  = (Resolve-Path "$PSScriptRoot\..").Path
$VENV_DIR  = "$REPO_DIR\.venv"
$VENV_PY   = "$VENV_DIR\Scripts\python.exe"
$VENV_ACT  = "$VENV_DIR\Scripts\Activate.ps1"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Agentic AI Course - Initial Setup"        -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Python check ────────────────────────────────────────────────────
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
$pyCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pyCmd) { $pyCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $pyCmd) {
    Write-Host "  ERROR: Python not found!" -ForegroundColor Red
    Write-Host "  Install Python 3.12+ from https://www.python.org/downloads/" -ForegroundColor Red
    Write-Host "  Make sure to check 'Add Python to PATH' during installation." -ForegroundColor Red
    exit 1
}
$pyExe = $pyCmd.Source
$pyVer = & $pyExe --version 2>&1
$pyMinor = & $pyExe -c "import sys; print(sys.version_info.minor)"
if ([int]$pyMinor -lt 10) {
    Write-Host "  $pyVer (too old — need 3.10+)" -ForegroundColor Red
    Write-Host "  Install Python 3.12+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}
Write-Host "  $pyVer (OK)" -ForegroundColor Green
Write-Host ""

# ── Step 2: Virtual environment ─────────────────────────────────────────────
Write-Host "[2/6] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path $VENV_PY) {
    Write-Host "  Virtual environment already exists at $VENV_DIR"
} else {
    Write-Host "  Creating .venv in $REPO_DIR ..."
    & $pyExe -m venv "$VENV_DIR"
    Write-Host "  Virtual environment created" -ForegroundColor Green
}
& $VENV_ACT
Write-Host "  Activated: $(& $VENV_PY --version)" -ForegroundColor Green
Write-Host ""

# ── Step 3: Install packages ─────────────────────────────────────────────────
Write-Host "[3/6] Installing Python packages (this may take a few minutes)..." -ForegroundColor Yellow
$REQ_FILE = "$REPO_DIR\requirements.txt"
if (Test-Path $REQ_FILE) {
    & $VENV_PY -m pip install --upgrade pip --quiet
    # CPU-only PyTorch to avoid downloading multi-GB CUDA packages
    & $VENV_PY -m pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet
    & $VENV_PY -m pip install -r $REQ_FILE
    Write-Host ""
    Write-Host "  Packages installed successfully" -ForegroundColor Green
} else {
    Write-Host "  WARNING: requirements.txt not found at $REQ_FILE" -ForegroundColor Yellow
    Write-Host "  Install manually: pip install langchain langchain-groq langgraph chromadb fastapi uvicorn"
}
Write-Host ""

# ── Step 4: .env file ────────────────────────────────────────────────────────
Write-Host "[4/6] Setting up environment file..." -ForegroundColor Yellow
$ENV_FILE    = "$REPO_DIR\.env"
$ENV_EXAMPLE = "$REPO_DIR\.env.example"
if (Test-Path $ENV_FILE) {
    Write-Host "  .env file already exists"
} elseif (Test-Path $ENV_EXAMPLE) {
    Copy-Item $ENV_EXAMPLE $ENV_FILE
    Write-Host "  Created .env from .env.example" -ForegroundColor Green
    Write-Host "  IMPORTANT: Edit .env and add your GROQ_API_KEY!" -ForegroundColor Yellow
} else {
    Write-Host "  WARNING: .env.example not found" -ForegroundColor Yellow
}
Write-Host ""

# ── Step 5: Jupyter kernel ────────────────────────────────────────────────────
Write-Host "[5/6] Registering Jupyter kernel '$KERNEL_NAME'..." -ForegroundColor Yellow
$codeCmd = Get-Command code -ErrorAction SilentlyContinue
if ($codeCmd) {
    & code --install-extension ms-toolsai.jupyter --force 2>$null
    Write-Host "  VS Code Jupyter extension installed" -ForegroundColor Green
} else {
    Write-Host "  'code' CLI not found — install Jupyter extension manually in VS Code (ms-toolsai.jupyter)"
}
& $VENV_PY -m pip install --quiet ipykernel
& $VENV_PY -m ipykernel install --user --name $KERNEL_NAME --display-name $KERNEL_DISPLAY
Write-Host "  Kernel '$KERNEL_NAME' registered" -ForegroundColor Green
Write-Host ""

# ── Step 6: Configure all notebooks ──────────────────────────────────────────
Write-Host "[6/6] Configuring all notebooks to auto-select kernel..." -ForegroundColor Yellow
$pyScript = @"
import json, sys
from pathlib import Path

kernel_name    = "$KERNEL_NAME"
kernel_display = "$KERNEL_DISPLAY"
repo_root      = Path(r"$REPO_DIR")
hands_on_dir   = repo_root / "hands-on"

notebooks = [nb for nb in hands_on_dir.rglob("*.ipynb") if "README" not in nb.name]
if not notebooks:
    print("  No notebooks found!")
    sys.exit(1)

print(f"  Found {len(notebooks)} notebooks")
ok = fail = 0
for nb_path in sorted(notebooks):
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        nb.setdefault("metadata", {})
        nb["metadata"]["kernelspec"] = {
            "display_name": kernel_display,
            "language": "python",
            "name": kernel_name,
        }
        nb["metadata"].setdefault("language_info", {})["name"] = "python"
        nb_path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  OK {nb_path.relative_to(repo_root)}")
        ok += 1
    except Exception as e:
        print(f"  FAIL {nb_path.relative_to(repo_root)}: {e}")
        fail += 1

print(f"\n  Updated: {ok}  Failed: {fail}  Total: {len(notebooks)}")
if fail:
    sys.exit(1)
"@
& $VENV_PY -c $pyScript
Write-Host ""

# ── Summary ──────────────────────────────────────────────────────────────────
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Initial setup complete!"                   -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit .env and add your Groq API key:"
Write-Host "     GROQ_API_KEY=gsk_your_key_here"
Write-Host "     (Get one free at https://console.groq.com)"
Write-Host ""
Write-Host "  2. Run Day 1 setup:"
Write-Host "     .\scripts\day1-setup.ps1"
Write-Host ""
Write-Host "  3. Open the first lab - kernel auto-selects:"
Write-Host "     code hands-on/session-1/lab01_meet_your_llm.ipynb"
Write-Host ""
Write-Host "To activate the virtual environment in this terminal, run:"
Write-Host "  $VENV_ACT"
Write-Host ""
