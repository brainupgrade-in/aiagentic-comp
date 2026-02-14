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

# Verify Python
Write-Host "[1/3] Verifying Python environment..."
$venvPython = Join-Path $env:USERPROFILE ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & (Join-Path $env:USERPROFILE ".venv\Scripts\Activate.ps1")
    $pyVer = python --version
    Write-Host "  Virtual environment active: $pyVer"
} else {
    try {
        $pyVer = python --version
        Write-Host "  Using system Python: $pyVer"
    } catch {
        Write-Host "  ERROR: Python 3 not found"
        exit 1
    }
}

# Verify FastAPI and production packages
Write-Host "[2/3] Verifying production packages..."
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
Write-Host "[3/3] Checking GROQ_API_KEY..."
if (-not $env:GROQ_API_KEY) {
    $envFile = Join-Path (Get-Location) ".env"
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

Write-Host ""
Write-Host "============================================"
Write-Host "  Day 4 Ready!"
Write-Host "============================================"
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 10: Observability Fundamentals"
Write-Host "  Session 11: LangFuse Observability"
Write-Host "  Session 12: Production Development & Deployment"
Write-Host ""
Write-Host "All labs run as pure Python - no external services needed."
Write-Host "LangFuse SDK patterns are taught using mock mode (logs to local JSON)."
Write-Host ""
Write-Host "Labs (open in VS Code or JupyterLab):"
Write-Host "  hands-on\session-10\lab01_three_pillars.ipynb"
Write-Host "  hands-on\session-11\lab01_langfuse_fundamentals.ipynb"
Write-Host "  hands-on\session-12\lab01_fastapi_basics.ipynb"
Write-Host ""
Write-Host "Resource usage: ~2-3 GB RAM (Python only)"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day4-cleanup.ps1' at end of day"
Write-Host ""
