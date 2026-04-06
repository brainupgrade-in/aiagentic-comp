# day2-cleanup.ps1 — Day 2: Cleanup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day2-cleanup.ps1

$ErrorActionPreference = "SilentlyContinue"

$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 2: Cleanup"                            -ForegroundColor Cyan
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

# ── Step 1: Clean Python cache and lab temp files ─────────────────────────────
Write-Host "[1/1] Cleaning temp files..." -ForegroundColor Yellow

# Remove __pycache__ directories
Get-ChildItem -Path $REPO_DIR -Recurse -Force -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# Remove lab temp dirs (Windows %TEMP% equivalents)
$tempDirs = @(
    "$env:TEMP\k8s-lab-04-*",
    "$env:TEMP\k8s-lab-05-*",
    "$env:TEMP\k8s-lab-06-*"
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
Write-Host "Day 2 cleanup complete. Ready for Day 3." -ForegroundColor Green
Write-Host ""
