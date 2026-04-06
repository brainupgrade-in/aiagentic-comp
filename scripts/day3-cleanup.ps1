# day3-cleanup.ps1 — Day 3: Cleanup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day3-cleanup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 3: Cleanup"                            -ForegroundColor Cyan
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

# ── Step 1: Stop any running servers ─────────────────────────────────────────
Write-Host "[1/2] Stopping any running servers..." -ForegroundColor Yellow
Get-Process -Name "uvicorn" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match "uvicorn|fastapi" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Write-Host "  Done" -ForegroundColor Green

# ── Step 2: Clean Python cache and lab temp files ─────────────────────────────
Write-Host "[2/2] Cleaning temp files..." -ForegroundColor Yellow

Get-ChildItem -Path $REPO_DIR -Recurse -Force -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

$tempDirs = @(
    "$env:TEMP\k8s-lab-07-*",
    "$env:TEMP\k8s-lab-08-*",
    "$env:TEMP\k8s-lab-09-*"
)
foreach ($pattern in $tempDirs) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}
Write-Host "  Done" -ForegroundColor Green
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
Write-Host "Day 3 cleanup complete. Ready for Day 4 (observability)." -ForegroundColor Green
Write-Host ""
