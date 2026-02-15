# day3-setup.ps1 — Day 3: LangGraph & Multi-Agent Setup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 3: LangGraph & Multi-Agent Setup"
Write-Host "============================================"
Write-Host ""

# Check available resources
Write-Host "Current resource usage:"
$os = Get-CimInstance Win32_OperatingSystem
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
$freeMB  = [math]::Round($os.FreePhysicalMemory / 1024)
Write-Host "  Memory: Total ${totalMB} MB | Available ${freeMB} MB"
Write-Host ""

# Check Python venv (relative to repo root)
$RepoDir = Split-Path -Parent $PSScriptRoot
Write-Host "[1/3] Verifying Python environment..."
$venvActivate = Join-Path $RepoDir ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
    $pyVer = python --version
    Write-Host "  Virtual environment active: $pyVer"
} else {
    try {
        $pyVer = python --version
        Write-Host "  Using system Python: $pyVer"
        Write-Host "  TIP: Create a venv with: python -m venv $RepoDir\.venv"
    } catch {
        Write-Host "  ERROR: Python not found. Install Python 3.10+ from https://python.org"
        exit 1
    }
}

# Verify LangGraph and production packages
Write-Host "[2/3] Verifying packages..."
$packages = @(
    @("langgraph",      "import langgraph; print(f'  langgraph {langgraph.__version__}')"),
    @("langchain-groq", "import langchain_groq; print(f'  langchain-groq {langchain_groq.__version__}')")
)
foreach ($pkg in $packages) {
    try {
        python -c $pkg[1] 2>$null
    } catch {
        Write-Host "  WARNING: $($pkg[0]) not installed"
    }
}

# Check Groq API key
Write-Host "[3/3] Checking Groq API key..."
if (-not $env:GROQ_API_KEY) {
    $envFile = Join-Path $RepoDir ".env"
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match '^\s*GROQ_API_KEY\s*=\s*(.+)$') {
                $env:GROQ_API_KEY = $Matches[1].Trim('"', "'", ' ')
            }
        }
    }
}

if ($env:GROQ_API_KEY -and $env:GROQ_API_KEY -ne "gsk_your_key_here") {
    Write-Host "  GROQ_API_KEY is set"
} else {
    Write-Host "  WARNING: GROQ_API_KEY not configured"
    Write-Host "  Add to .env: GROQ_API_KEY=gsk_your_key_here"
}

Write-Host ""
Write-Host "============================================"
Write-Host "  Day 3 ready!"
Write-Host "============================================"
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 7: LangGraph Stateful Workflows"
Write-Host "  Session 8: Advanced LangGraph Workflows"
Write-Host "  Session 9: Multi-Agent Systems"
Write-Host ""
Write-Host "Labs: hands-on\session-7\ through session-9\"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day3-cleanup.ps1' at end of day"
Write-Host "to free resources for Day 4 (observability stack)."
Write-Host ""
