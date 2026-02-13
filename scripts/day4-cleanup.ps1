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

# Clean up lab temp files
Write-Host "[1/2] Removing lab temp files..."
Remove-Item "$env:TEMP\k8s-lab-10-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\k8s-lab-11-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\prod-lab-12-*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  Removed temp directories"

# Stop stale processes
Write-Host "[2/2] Stopping stale processes..."
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
