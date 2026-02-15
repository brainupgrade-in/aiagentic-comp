# day4-setup.ps1 — Day 4: Observability & Production Setup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 4: Observability & Production Setup"
Write-Host "============================================"
Write-Host ""

Write-Host "Current resource usage:"
$os = Get-CimInstance Win32_OperatingSystem
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
$freeMB  = [math]::Round($os.FreePhysicalMemory / 1024)
Write-Host "  Memory: Total ${totalMB} MB | Available ${freeMB} MB"
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$usedGB = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 1)
$totalGB = [math]::Round($disk.Size / 1GB, 1)
Write-Host "  Storage: ${usedGB} GB used / ${totalGB} GB total"
Write-Host ""

# Verify Python (relative to repo root)
$RepoDir = Split-Path -Parent $PSScriptRoot
Write-Host "[1/4] Verifying Python environment..."
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
        Write-Host "  ERROR: Python 3 not found"
        exit 1
    }
}

# Verify FastAPI and production packages
Write-Host "[2/4] Verifying production packages..."
$packages = @(
    @("fastapi",        "import fastapi; print(f'  fastapi {fastapi.__version__}')"),
    @("uvicorn",        "import uvicorn; print(f'  uvicorn {uvicorn.__version__}')"),
    @("pydantic",       "import pydantic; print(f'  pydantic {pydantic.__version__}')"),
    @("psutil",         "import psutil; print(f'  psutil {psutil.__version__}')"),
    @("langfuse",       "import langfuse; print(f'  langfuse {langfuse.__version__}')"),
    @("opentelemetry",  "import opentelemetry; print(f'  opentelemetry-api installed')")
)
foreach ($pkg in $packages) {
    try {
        python -c $pkg[1] 2>$null
    } catch {
        Write-Host "  WARNING: $($pkg[0]) not installed"
    }
}

# Verify GROQ_API_KEY
Write-Host "[3/4] Checking GROQ_API_KEY..."
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
    Write-Host ""
    Write-Host "  WARNING: GROQ_API_KEY not set."
    Write-Host "  Set it in .env or run: `$env:GROQ_API_KEY='gsk_...'"
    Write-Host "  Get your free key at: https://console.groq.com"
    Write-Host ""
}

# Start LangFuse server for Session 12 Lab 09
Write-Host ""
Write-Host "[4/4] Starting LangFuse server for Session 12 Lab 09..."
$langfuseScript = Join-Path $RepoDir "scripts\langfuse-server.py"
$langfusePidFile = Join-Path $env:TEMP "langfuse-server.pid"
$langfuseLog = Join-Path $env:TEMP "langfuse-server.log"

# Check if port 3000 is already in use
$portInUse = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "  WARNING: Port 3000 already in use. LangFuse server may already be running."
    Write-Host "  To stop it: .\scripts\day4-cleanup.ps1"
} else {
    $venvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"
    if (Test-Path $venvPython) {
        $proc = Start-Process -FilePath $venvPython -ArgumentList $langfuseScript `
            -WindowStyle Hidden -PassThru -RedirectStandardOutput $langfuseLog -RedirectStandardError (Join-Path $env:TEMP "langfuse-server-err.log")
        $proc.Id | Out-File -FilePath $langfusePidFile -Encoding ASCII
        Start-Sleep -Seconds 3

        try {
            $health = Invoke-WebRequest -Uri "http://localhost:3000/api/public/health" -UseBasicParsing -TimeoutSec 5
            Write-Host "  LangFuse server started on http://localhost:3000"
            Write-Host "  PID: $($proc.Id) (saved to $langfusePidFile)"
            Write-Host "  Logs: $langfuseLog"
        } catch {
            Write-Host "  ERROR: LangFuse server failed to start. Check $langfuseLog"
        }
    } else {
        Write-Host "  Skipping LangFuse server (virtual environment not found)"
        Write-Host "  You can start it manually later: python scripts\langfuse-server.py"
    }
}

Write-Host ""
Write-Host "============================================"
Write-Host "  Day 4 Ready!"
Write-Host "============================================"
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
Write-Host "  Database: $env:TEMP\langfuse.db (SQLite)"
Write-Host "  Logs: $langfuseLog"
Write-Host ""
Write-Host "Labs (open in VS Code or JupyterLab):"
Write-Host "  Session 10: hands-on\session-10\lab01_three_pillars.ipynb (8 labs)"
Write-Host "  Session 11: hands-on\session-11\lab01_fastapi_basics.ipynb (8 labs)"
Write-Host "  Session 12: hands-on\session-12\lab01_langfuse_fundamentals.ipynb (9 labs)"
Write-Host ""
Write-Host "Lab pattern:"
Write-Host "  - Labs 01-08: Use MockLangfuse (local JSON files)"
Write-Host "  - Lab 09: Use real LangFuse server (http://localhost:3000)"
Write-Host ""
Write-Host "Resource usage: ~2-4 GB RAM (Python + SQLite)"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day4-cleanup.ps1' at end of day"
Write-Host ""
