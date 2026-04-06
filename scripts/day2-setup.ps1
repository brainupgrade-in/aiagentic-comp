# day2-setup.ps1 — Day 2: LangChain + Groq API Setup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day2-setup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path
$VENV_PY  = "$REPO_DIR\.venv\Scripts\python.exe"
$ENV_FILE = "$REPO_DIR\.env"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 2: LangChain + Groq API Setup"        -ForegroundColor Cyan
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

# ── Warn if Ollama is still running ────────────────────────────────────────────
$ollamaProc = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if ($ollamaProc) {
    Write-Host "WARNING: Ollama is still running." -ForegroundColor Yellow
    Write-Host "  Run '.\scripts\day1-cleanup.ps1' first to free ~2 GB of resources." -ForegroundColor Yellow
    Write-Host ""
}

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

# ── Step 2: Verify LangChain packages ────────────────────────────────────────
Write-Host "[2/3] Verifying LangChain packages..." -ForegroundColor Yellow

$checks = @(
    @{ Module = "langchain";        Label = "langchain" },
    @{ Module = "langchain_groq";   Label = "langchain-groq" },
    @{ Module = "langchain_chroma"; Label = "langchain-chroma" },
    @{ Module = "langgraph";        Label = "langgraph" }
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
    Write-Host "  1. Sign up at https://console.groq.com (free)"
    Write-Host "  2. Create an API key"
    Write-Host "  3. Add to .env in the repo root:"
    Write-Host "     GROQ_API_KEY=gsk_your_key_here"
}
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 2 ready!"                              -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 4: LangChain Fundamentals"
Write-Host "  Session 5: Building RAG Applications"
Write-Host "  Session 6: LangChain Agents & Memory"
Write-Host ""
Write-Host "Quick test (Python):"
Write-Host "  from langchain_groq import ChatGroq"
Write-Host "  llm = ChatGroq(model='llama-3.1-8b-instant')"
Write-Host "  print(llm.invoke('Hello from Day 2!'))"
Write-Host ""
Write-Host "Labs: hands-on\session-4\ through session-6\"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day2-cleanup.ps1' at end of day." -ForegroundColor Yellow
Write-Host ""
