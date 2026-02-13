# day5-setup.ps1 — Day 5: MCP, Safety & Capstone Setup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 5: MCP, Safety & Capstone Setup"
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
Write-Host "[1/3] Verifying Python..."
try {
    $pyVer = python --version
    Write-Host "  $pyVer"
} catch {
    Write-Host "  ERROR: Python 3 not found"
    exit 1
}

# Install MCP SDK
Write-Host "[2/3] Installing MCP Python SDK..."
pip install --quiet "mcp>=1.0" 2>$null
if ($LASTEXITCODE -ne 0) {
    pip install "mcp>=1.0"
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
Write-Host "  Day 5 Ready!"
Write-Host "============================================"
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 13: Model Context Protocol (MCP)"
Write-Host "  Session 14: AI Safety & Guardrails"
Write-Host "  Session 15: Capstone Project (2 time slots)"
Write-Host ""
Write-Host "Labs:"
Write-Host "  python hands-on\session-13\lab01_mcp_fundamentals.py"
Write-Host "  python hands-on\session-14\lab01_prompt_injection_detection.py"
Write-Host "  python hands-on\session-15\lab01_capstone_architecture.py"
Write-Host ""
Write-Host "Resource usage: ~3-4 GB RAM (Python + MCP SDK only)"
Write-Host "Day 5 is lightweight - no observability stack needed."
Write-Host ""
