# initial-setup.ps1 — One-time environment setup for Windows participants
# Run this ONCE at the start of the course to set up Python, venv, and all packages.
#
# Usage (from repo root in PowerShell):
#   .\scripts\initial-setup.ps1
#
$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Agentic AI Course — Initial Setup" -ForegroundColor Cyan
Write-Host "  (Windows)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$RepoDir = Split-Path -Parent $PSScriptRoot

# Step 1: Check PowerShell execution policy
Write-Host "[1/6] Checking PowerShell execution policy..."
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted" -or $policy -eq "AllSigned") {
    Write-Host "  Current policy: $policy (too restrictive)"
    Write-Host "  Setting to RemoteSigned for current user..."
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    Write-Host "  Execution policy updated to RemoteSigned"
} else {
    Write-Host "  Execution policy: $policy (OK)"
}
Write-Host ""

# Step 2: Check Python installation
Write-Host "[2/6] Checking Python installation..."
try {
    $pyVer = python --version 2>&1
    if ($pyVer -match "Python (\d+)\.(\d+)") {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        if ($major -ge 3 -and $minor -ge 10) {
            Write-Host "  $pyVer (OK)"
        } else {
            Write-Host "  $pyVer (too old — need 3.10+)" -ForegroundColor Yellow
            Write-Host ""
            Write-Host "  Install Python 3.12+ from: https://python.org/downloads"
            Write-Host "  IMPORTANT: Check 'Add Python to PATH' during installation!"
            Write-Host ""
            exit 1
        }
    }
} catch {
    Write-Host "  Python not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Install Python 3.12+ from: https://python.org/downloads"
    Write-Host "  IMPORTANT: Check 'Add Python to PATH' during installation!"
    Write-Host ""
    Write-Host "  After installing, close and reopen PowerShell, then run this script again."
    exit 1
}
Write-Host ""

# Step 3: Check pip
Write-Host "[3/6] Checking pip..."
try {
    $pipVer = pip --version 2>&1
    Write-Host "  $pipVer"
} catch {
    Write-Host "  pip not found. Installing..."
    python -m ensurepip --upgrade
}
Write-Host ""

# Step 4: Create virtual environment
Write-Host "[4/6] Creating virtual environment..."
$venvDir = Join-Path $RepoDir ".venv"
$venvPython = Join-Path $venvDir "Scripts\python.exe"

if (Test-Path $venvPython) {
    Write-Host "  Virtual environment already exists at $venvDir"
} else {
    Write-Host "  Creating .venv in $RepoDir ..."
    python -m venv $venvDir
    Write-Host "  Virtual environment created"
}

# Activate
& (Join-Path $venvDir "Scripts\Activate.ps1")
Write-Host "  Activated: $(python --version)"
Write-Host ""

# Step 5: Install requirements
Write-Host "[5/6] Installing Python packages (this may take a few minutes)..."
$reqFile = Join-Path $RepoDir "requirements.txt"
if (Test-Path $reqFile) {
    pip install --upgrade pip --quiet 2>$null
    # Install CPU-only PyTorch first to avoid downloading multi-GB NVIDIA/CUDA packages
    pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet 2>$null
    pip install -r $reqFile
    Write-Host ""
    Write-Host "  Packages installed successfully"
} else {
    Write-Host "  WARNING: requirements.txt not found at $reqFile" -ForegroundColor Yellow
    Write-Host "  Install packages manually: pip install langchain langchain-groq langgraph chromadb fastapi uvicorn"
}
Write-Host ""

# Step 6: Set up .env file
Write-Host "[6/6] Setting up environment file..."
$envFile = Join-Path $RepoDir ".env"
$envExample = Join-Path $RepoDir ".env.example"

if (Test-Path $envFile) {
    Write-Host "  .env file already exists"
} elseif (Test-Path $envExample) {
    Copy-Item $envExample $envFile
    Write-Host "  Created .env from .env.example"
    Write-Host "  IMPORTANT: Edit .env and add your GROQ_API_KEY!" -ForegroundColor Yellow
} else {
    Write-Host "  WARNING: .env.example not found" -ForegroundColor Yellow
}
Write-Host ""

# Check GitHub CLI (optional)
Write-Host "--- Optional: GitHub CLI ---"
try {
    $ghVer = gh --version 2>&1 | Select-Object -First 1
    Write-Host "  $ghVer (OK)"
} catch {
    Write-Host "  GitHub CLI (gh) not installed — needed for lab submission" -ForegroundColor Yellow
    Write-Host "  Install: winget install GitHub.cli"
    Write-Host "  Or download: https://cli.github.com/"
}
Write-Host ""

# Check VS Code (optional)
Write-Host "--- Optional: VS Code ---"
try {
    $codeVer = code --version 2>&1 | Select-Object -First 1
    Write-Host "  VS Code $codeVer (OK)"
} catch {
    Write-Host "  VS Code CLI not found" -ForegroundColor Yellow
    Write-Host "  Download: https://code.visualstudio.com/"
}
Write-Host ""

# Summary
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Initial setup complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Edit .env and add your Groq API key:" -ForegroundColor Cyan
Write-Host "     GROQ_API_KEY=gsk_your_key_here"
Write-Host "     (Get one free at https://console.groq.com)"
Write-Host ""
Write-Host "  2. Set up Jupyter notebooks:" -ForegroundColor Cyan
Write-Host "     .\scripts\install-notebook.ps1"
Write-Host ""
Write-Host "  3. Run Day 1 setup:" -ForegroundColor Cyan
Write-Host "     .\scripts\day1-setup.ps1"
Write-Host ""
Write-Host "  4. Open the first lab in VS Code:" -ForegroundColor Cyan
Write-Host "     code hands-on\session-1\lab01_meet_your_llm.ipynb"
Write-Host ""
Write-Host "Activate the virtual environment in any new terminal with:"
Write-Host "  $venvDir\Scripts\Activate.ps1"
Write-Host ""
