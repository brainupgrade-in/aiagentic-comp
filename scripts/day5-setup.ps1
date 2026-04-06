# day5-setup.ps1 — Day 5: MCP, Safety & Capstone Setup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day5-setup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path
$VENV_PY  = "$REPO_DIR\.venv\Scripts\python.exe"
$VENV_PIP = "$REPO_DIR\.venv\Scripts\pip.exe"
$ENV_FILE = "$REPO_DIR\.env"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 5: MCP, Safety & Capstone Setup"      -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Resource check ─────────────────────────────────────────────────────────────
Write-Host "Current resource usage:" -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB  = [math]::Round($os.FreePhysicalMemory     / 1MB, 1)
$usedGB  = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
$disk    = Get-PSDrive C
$diskFreeGB = [math]::Round($disk.Free / 1GB, 1)
Write-Host "  Memory:  ${usedGB} GB used / ${totalGB} GB total (${freeGB} GB free)"
Write-Host "  Storage: ${diskFreeGB} GB free on C:"
Write-Host ""

# ── Step 1: Verify Python venv ────────────────────────────────────────────────
Write-Host "[1/3] Verifying Python environment..." -ForegroundColor Yellow
if (-not (Test-Path $VENV_PY)) {
    Write-Host "  ERROR: Virtual environment not found at $REPO_DIR\.venv" -ForegroundColor Red
    Write-Host "  Run: .\scripts\initial-setup.ps1" -ForegroundColor Red
    exit 1
}
$pyVer = & $VENV_PY --version 2>&1
Write-Host "  Virtual environment active: $pyVer" -ForegroundColor Green
Write-Host ""

# ── Step 2: Install MCP SDK ───────────────────────────────────────────────────
Write-Host "[2/3] Installing MCP Python SDK..." -ForegroundColor Yellow
& $VENV_PIP install --quiet "mcp>=1.0"
if ($LASTEXITCODE -eq 0) {
    $mcpVer = & $VENV_PY -c "import mcp; print(mcp.__version__)" 2>&1
    Write-Host "  mcp $mcpVer" -ForegroundColor Green
} else {
    Write-Host "  WARNING: MCP SDK install may have failed. Check pip output above." -ForegroundColor Yellow
}
Write-Host ""

# ── Step 3: Check Groq API key ────────────────────────────────────────────────
Write-Host "[3/3] Checking GROQ_API_KEY..." -ForegroundColor Yellow

$groqKey = $env:GROQ_API_KEY
if (-not $groqKey -and (Test-Path $ENV_FILE)) {
    foreach ($line in Get-Content $ENV_FILE) {
        if ($line -match "^GROQ_API_KEY=(.+)$") { $groqKey = $Matches[1]; break }
    }
}

if ($groqKey -and $groqKey -ne "gsk_your_key_here") {
    Write-Host "  GROQ_API_KEY found" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "  WARNING: GROQ_API_KEY not set." -ForegroundColor Yellow
    Write-Host "  Set it in .env or run: `$env:GROQ_API_KEY='gsk_...'"
    Write-Host "  Get your free key at: https://console.groq.com"
    Write-Host ""
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 5 Ready!"                              -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 13: Model Context Protocol (MCP)"
Write-Host "  Session 14: AI Safety & Guardrails"
Write-Host "  Session 15: Capstone Project (2 time slots)"
Write-Host ""
Write-Host "Labs (open in VS Code):"
Write-Host "  hands-on\session-13\lab01_mcp_fundamentals.ipynb"
Write-Host "  hands-on\session-14\lab01_prompt_injection_detection.ipynb"
Write-Host "  hands-on\session-15\lab01_capstone_architecture.ipynb"
Write-Host ""
Write-Host "Resource usage: ~3-4 GB RAM (Python + MCP SDK only)."
Write-Host "Day 5 is lightweight — no observability stack needed."
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day5-cleanup.ps1' at end of course." -ForegroundColor Yellow
Write-Host ""
