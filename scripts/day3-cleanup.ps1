# day3-cleanup.ps1 — Day 3: Cleanup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 3: Cleanup"
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

# Stop any running app servers
Write-Host "[1/2] Stopping any running servers..."
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process -Name "fastapi" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

# Clean temp files and Python cache
Write-Host "[2/2] Cleaning temp files..."
Get-ChildItem -Path (Get-Location) -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-07-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-08-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-09-*" -Recurse -Force -ErrorAction SilentlyContinue

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
Write-Host "Day 3 cleanup complete. Ready for Day 4 (observability)."
Write-Host ""
