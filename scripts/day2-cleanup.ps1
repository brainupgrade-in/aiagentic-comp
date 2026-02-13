# day2-cleanup.ps1 — Day 2: Cleanup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 2: Cleanup"
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

# Clean Python cache and temp files
Write-Host "[1/1] Cleaning temp files..."
Get-ChildItem -Path (Get-Location) -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\k8s-lab-04-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\k8s-lab-05-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\k8s-lab-06-*" -Recurse -Force -ErrorAction SilentlyContinue

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
Write-Host "Day 2 cleanup complete. Ready for Day 3."
Write-Host ""
