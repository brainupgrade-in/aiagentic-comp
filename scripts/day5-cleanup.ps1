# day5-cleanup.ps1 — Day 5: Final Cleanup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 5: Final Cleanup"
Write-Host "============================================"
Write-Host ""

# Clean up lab temp files
Write-Host "[1/2] Removing lab temp files..."
Remove-Item "$env:TEMP\aidev-lab-13-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\safety-lab-14-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\capstone-lab-15-*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  Removed MCP, safety, and capstone temp directories"

# Kill any stale processes
Write-Host "[2/2] Stopping stale processes..."
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process | Where-Object { $_.ProcessName -match "python" -and $_.MainWindowTitle -eq "" } | ForEach-Object {
    # Only stop background python processes that look like MCP servers
    try {
        $cmdLine = (Get-CimInstance Win32_Process -Filter "ProcessId=$($_.Id)").CommandLine
        if ($cmdLine -match "mcp.*server") {
            Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
        }
    } catch {}
}

Write-Host ""
Write-Host "Cleanup complete."
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$usedGB = [math]::Round(($disk.Size - $disk.FreeSpace) / 1GB, 1)
$totalGB = [math]::Round($disk.Size / 1GB, 1)
Write-Host "  Storage: ${usedGB} GB used / ${totalGB} GB total"
$os = Get-CimInstance Win32_OperatingSystem
$usedMB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1024)
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
Write-Host "  Memory: ${usedMB} MB used / ${totalMB} MB total"
Write-Host ""
Write-Host "Course complete! Thank you for participating."
Write-Host ""
