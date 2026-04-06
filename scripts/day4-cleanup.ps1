# day4-cleanup.ps1 — Day 4: Observability & Production Cleanup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day4-cleanup.ps1

$ErrorActionPreference = "SilentlyContinue"

$LANGFUSE_PID = "$env:TEMP\langfuse-server.pid"
$LANGFUSE_LOG = "$env:TEMP\langfuse-server.log"
$LANGFUSE_DB  = "$env:TEMP\langfuse.db"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 4: Observability & Production Cleanup" -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Before stats
Write-Host "Before cleanup:" -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$totalGB     = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$usedGB      = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
$disk        = Get-PSDrive C
$diskUsedGB  = [math]::Round($disk.Used / 1GB, 1)
$diskFreeGB  = [math]::Round($disk.Free / 1GB, 1)
$diskTotalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 1)
Write-Host "  Memory:   ${usedGB} GB used / ${totalGB} GB total"
Write-Host "  Storage C: ${diskUsedGB} GB used / ${diskTotalGB} GB total (${diskFreeGB} GB free)"
Write-Host ""

# ── Step 1: Stop LangFuse server ─────────────────────────────────────────────
Write-Host "[1/4] Stopping LangFuse server..." -ForegroundColor Yellow
if (Test-Path $LANGFUSE_PID) {
    $pid = Get-Content $LANGFUSE_PID -Raw
    $proc = Get-Process -Id $pid -ErrorAction SilentlyContinue
    if ($proc) {
        Stop-Process -Id $pid -Force
        Write-Host "  Stopped LangFuse server (PID: $pid)" -ForegroundColor Green
    } else {
        Write-Host "  LangFuse server not running (stale PID file)"
    }
    Remove-Item $LANGFUSE_PID -Force
} else {
    # Try by port
    $conn = Get-NetTCPConnection -LocalPort 3000 -State Listen -ErrorAction SilentlyContinue
    if ($conn) {
        Stop-Process -Id $conn.OwningProcess -Force
        Write-Host "  Stopped process on port 3000 (PID: $($conn.OwningProcess))" -ForegroundColor Green
    } else {
        Write-Host "  No LangFuse server running"
    }
}

# ── Step 2: Clean LangFuse data ───────────────────────────────────────────────
Write-Host "[2/4] Cleaning up LangFuse data..." -ForegroundColor Yellow
Remove-Item $LANGFUSE_DB  -Force -ErrorAction SilentlyContinue
Remove-Item $LANGFUSE_LOG -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\langfuse-server-err.log" -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "$env:TEMP\langfuse-traces*" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force
Write-Host "  Removed database and logs" -ForegroundColor Green

# ── Step 3: Clean lab temp files ─────────────────────────────────────────────
Write-Host "[3/4] Removing lab temp files..." -ForegroundColor Yellow
$tempDirs = @(
    "$env:TEMP\k8s-lab-10-*",
    "$env:TEMP\prod-lab-11-*",
    "$env:TEMP\k8s-lab-12-*",
    "$env:TEMP\prod-lab-12-*",
    "$env:TEMP\langfuse-traces"
)
foreach ($pattern in $tempDirs) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}
Write-Host "  Removed temp directories" -ForegroundColor Green

# ── Step 4: Stop stale processes ─────────────────────────────────────────────
Write-Host "[4/4] Stopping stale processes..." -ForegroundColor Yellow
Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match "uvicorn.*8000|fastapi" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Write-Host "  Stopped stale FastAPI processes" -ForegroundColor Green
Write-Host ""

# After stats
Write-Host "After cleanup:" -ForegroundColor Yellow
$os2 = Get-CimInstance Win32_OperatingSystem
$usedGB2 = [math]::Round(($os2.TotalVisibleMemorySize - $os2.FreePhysicalMemory) / 1MB, 1)
$disk2   = Get-PSDrive C
$diskUsedGB2 = [math]::Round($disk2.Used / 1GB, 1)
$diskFreeGB2 = [math]::Round($disk2.Free / 1GB, 1)
Write-Host "  Memory:   ${usedGB2} GB used / ${totalGB} GB total"
Write-Host "  Storage C: ${diskUsedGB2} GB used / ${diskTotalGB} GB total (${diskFreeGB2} GB free)"
Write-Host ""
Write-Host "Day 4 cleanup complete. Ready for Day 5 (MCP + Capstone)." -ForegroundColor Green
Write-Host ""
