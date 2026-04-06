# day3-setup.ps1 — Day 3: LangGraph & Multi-Agent Setup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day3-setup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path
$VENV_PY  = "$REPO_DIR\.venv\Scripts\python.exe"
$ENV_FILE = "$REPO_DIR\.env"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 3: LangGraph & Multi-Agent Setup"     -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Resource check ─────────────────────────────────────────────────────────────
Write-Host "Current resource usage:" -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB  = [math]::Round($os.FreePhysicalMemory     / 1MB, 1)
$usedGB  = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
Write-Host "  Memory: ${usedGB} GB used / ${totalGB} GB total (${freeGB} GB free)"
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

# ── Step 2: Verify LangGraph packages ─────────────────────────────────────────
Write-Host "[2/3] Verifying packages..." -ForegroundColor Yellow

$checks = @(
    @{ Module = "langgraph";      Label = "langgraph" },
    @{ Module = "langchain_groq"; Label = "langchain-groq" }
)
foreach ($c in $checks) {
    $ver = & $VENV_PY -c "import $($c.Module); print($($c.Module).__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $($c.Label) $ver" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: $($c.Label) not installed" -ForegroundColor Yellow
    }
}
Write-Host ""

# ── Step 3: Check Groq API key ────────────────────────────────────────────────
Write-Host "[3/3] Checking Groq API key..." -ForegroundColor Yellow

$groqKey = $env:GROQ_API_KEY
if (-not $groqKey -and (Test-Path $ENV_FILE)) {
    foreach ($line in Get-Content $ENV_FILE) {
        if ($line -match "^GROQ_API_KEY=(.+)$") { $groqKey = $Matches[1]; break }
    }
}

if ($groqKey -and $groqKey -ne "gsk_your_key_here") {
    Write-Host "  GROQ_API_KEY is set" -ForegroundColor Green
} else {
    Write-Host "  WARNING: GROQ_API_KEY not configured" -ForegroundColor Yellow
    Write-Host "  Add to .env in the repo root: GROQ_API_KEY=gsk_your_key_here"
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 3 ready!"                              -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 7: LangGraph Stateful Workflows"
Write-Host "  Session 8: Advanced LangGraph Workflows"
Write-Host "  Session 9: Multi-Agent Systems"
Write-Host ""
Write-Host "Labs: hands-on\session-7\ through session-9\"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day3-cleanup.ps1' at end of day" -ForegroundColor Yellow
Write-Host "to free resources for Day 4 (observability stack)." -ForegroundColor Yellow
Write-Host ""
