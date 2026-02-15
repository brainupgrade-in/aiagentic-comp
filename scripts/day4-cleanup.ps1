# day4-cleanup.ps1 — Day 4: Observability & Production Cleanup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 4: Observability & Production Cleanup"
Write-Host "============================================"
Write-Host ""

Write-Host "Before cleanup:"
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$usedGB = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 1)
$totalGB = [math]::Round($disk.Size / 1GB, 1)
Write-Host "  Storage: ${usedGB} GB used / ${totalGB} GB total"
$os = Get-CimInstance Win32_OperatingSystem
$usedMB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1024)
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
Write-Host "  Memory: ${usedMB} MB used / ${totalMB} MB total"
Write-Host ""

# Stop LangFuse server
Write-Host "[1/4] Stopping LangFuse server..."
$langfusePidFile = Join-Path $env:TEMP "langfuse-server.pid"
if (Test-Path $langfusePidFile) {
    $langfusePid = Get-Content $langfusePidFile -ErrorAction SilentlyContinue
    if ($langfusePid) {
        try {
            Stop-Process -Id $langfusePid -Force -ErrorAction SilentlyContinue
            Write-Host "  Stopped LangFuse server (PID: $langfusePid)"
        } catch {
            Write-Host "  LangFuse server not running (stale PID)"
        }
    }
    Remove-Item $langfusePidFile -Force -ErrorAction SilentlyContinue
} else {
    # Try to find by port
    $portProc = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($portProc) {
        Stop-Process -Id $portProc.OwningProcess -Force -ErrorAction SilentlyContinue
        Write-Host "  Stopped process on port 3000"
    } else {
        Write-Host "  No LangFuse server running"
    }
}

# Clean up LangFuse database and logs
Write-Host "[2/4] Cleaning up LangFuse data..."
Remove-Item "$env:TEMP\langfuse.db" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\langfuse-server.log" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\langfuse-server-err.log" -Force -ErrorAction SilentlyContinue
Write-Host "  Removed database and logs"

# Clean up lab temp files
Write-Host "[3/4] Removing lab temp files..."
Remove-Item "$env:TEMP\ailab-10-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-11-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\prod-lab-12-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-12-*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  Removed temp directories"

# Stop stale processes
Write-Host "[4/4] Stopping stale processes..."
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name "fastapi" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "After cleanup:"
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$usedGB = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 1)
$totalGB = [math]::Round($disk.Size / 1GB, 1)
Write-Host "  Storage: ${usedGB} GB used / ${totalGB} GB total"
$os = Get-CimInstance Win32_OperatingSystem
$usedMB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1024)
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
Write-Host "  Memory: ${usedMB} MB used / ${totalMB} MB total"
Write-Host ""
Write-Host "Day 4 cleanup complete. Ready for Day 5 (MCP + Capstone)."
Write-Host ""
