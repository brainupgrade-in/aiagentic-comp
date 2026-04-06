# day4-setup.ps1 — Day 4: Observability & Production Setup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day4-setup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR        = (Resolve-Path "$PSScriptRoot\..").Path
$VENV_PY         = "$REPO_DIR\.venv\Scripts\python.exe"
$ENV_FILE        = "$REPO_DIR\.env"
$LANGFUSE_SCRIPT = "$REPO_DIR\scripts\langfuse-server.py"
$LANGFUSE_PID    = "$env:TEMP\langfuse-server.pid"
$LANGFUSE_LOG    = "$env:TEMP\langfuse-server.log"
$LANGFUSE_DB     = "$env:TEMP\langfuse.db"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 4: Observability & Production Setup"  -ForegroundColor Cyan
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
Write-Host "[1/4] Verifying Python environment..." -ForegroundColor Yellow
if (-not (Test-Path $VENV_PY)) {
    Write-Host "  ERROR: Virtual environment not found at $REPO_DIR\.venv" -ForegroundColor Red
    Write-Host "  Run: .\scripts\initial-setup.ps1" -ForegroundColor Red
    exit 1
}
$pyVer = & $VENV_PY --version 2>&1
Write-Host "  Virtual environment active: $pyVer" -ForegroundColor Green
Write-Host ""

# ── Step 2: Verify production packages ───────────────────────────────────────
Write-Host "[2/4] Verifying production packages..." -ForegroundColor Yellow

$checks = @(
    @{ Module = "fastapi";        Label = "fastapi" },
    @{ Module = "uvicorn";        Label = "uvicorn" },
    @{ Module = "pydantic";       Label = "pydantic" },
    @{ Module = "psutil";         Label = "psutil" },
    @{ Module = "langfuse";       Label = "langfuse" },
    @{ Module = "opentelemetry";  Label = "opentelemetry-api" }
)
foreach ($c in $checks) {
    if ($c.Module -eq "opentelemetry") {
        $result = & $VENV_PY -c "import opentelemetry; print('installed')" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  opentelemetry-api installed" -ForegroundColor Green
        } else {
            Write-Host "  WARNING: opentelemetry not installed" -ForegroundColor Yellow
        }
    } else {
        $ver = & $VENV_PY -c "import $($c.Module); print($($c.Module).__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  $($c.Label) $ver" -ForegroundColor Green
        } else {
            Write-Host "  WARNING: $($c.Label) not installed" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

# ── Step 3: Check Groq API key ────────────────────────────────────────────────
Write-Host "[3/4] Checking GROQ_API_KEY..." -ForegroundColor Yellow

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

# ── Step 4: Start LangFuse server ────────────────────────────────────────────
Write-Host "[4/4] Starting LangFuse server for Session 12 Lab 09..." -ForegroundColor Yellow

# Check if port 3000 is already in use
$port3000 = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
if ($port3000) {
    Write-Host "  WARNING: Port 3000 already in use. LangFuse may already be running." -ForegroundColor Yellow
    Write-Host "  To stop it: .\scripts\day4-cleanup.ps1"
} elseif (-not (Test-Path $LANGFUSE_SCRIPT)) {
    Write-Host "  ERROR: langfuse-server.py not found at $LANGFUSE_SCRIPT" -ForegroundColor Red
} else {
    # Start LangFuse in background
    $proc = Start-Process -FilePath $VENV_PY `
        -ArgumentList $LANGFUSE_SCRIPT `
        -RedirectStandardOutput $LANGFUSE_LOG `
        -RedirectStandardError  "$env:TEMP\langfuse-server-err.log" `
        -WindowStyle Hidden `
        -PassThru
    $proc.Id | Out-File -FilePath $LANGFUSE_PID -Encoding ascii

    # Wait for server to come up
    Start-Sleep -Seconds 4

    try {
        $resp = Invoke-WebRequest -Uri "http://localhost:3000/api/public/health" -UseBasicParsing -TimeoutSec 5
        if ($resp.StatusCode -eq 200) {
            Write-Host "  LangFuse server started on http://localhost:3000" -ForegroundColor Green
            Write-Host "  PID: $($proc.Id) (saved to $LANGFUSE_PID)"
            Write-Host "  Logs: $LANGFUSE_LOG"
            Write-Host "  Database: $LANGFUSE_DB"
        }
    } catch {
        Write-Host "  ERROR: LangFuse server failed to start." -ForegroundColor Red
        Write-Host "  Check logs at: $LANGFUSE_LOG" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 4 Ready!"                              -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 10: Observability Fundamentals"
Write-Host "  Session 11: Production Development & Deployment"
Write-Host "  Session 12: LangFuse Observability"
Write-Host ""
Write-Host "Session flow: Learn observability theory -> Build production app -> Instrument it"
Write-Host ""
Write-Host "Infrastructure:"
Write-Host "  LangFuse server running on http://localhost:3000 (for Lab 09)"
Write-Host "  Database: $LANGFUSE_DB"
Write-Host "  Logs:     $LANGFUSE_LOG"
Write-Host ""
Write-Host "Labs (open in VS Code):"
Write-Host "  Session 10: hands-on\session-10\lab01_three_pillars.ipynb  (8 labs)"
Write-Host "  Session 11: hands-on\session-11\lab01_fastapi_basics.ipynb (8 labs)"
Write-Host "  Session 12: hands-on\session-12\lab01_langfuse_fundamentals.ipynb (9 labs)"
Write-Host ""
Write-Host "Lab pattern:"
Write-Host "  Labs 01-08: Use MockLangfuse (local JSON files)"
Write-Host "  Lab 09:     Use real LangFuse server (http://localhost:3000)"
Write-Host ""
Write-Host "Resource usage: ~2-4 GB RAM (Python + SQLite)"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day4-cleanup.ps1' at end of day." -ForegroundColor Yellow
Write-Host ""
