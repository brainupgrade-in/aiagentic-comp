# day5-cleanup.ps1 — Day 5: Final Cleanup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day5-cleanup.ps1

$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 5: Final Cleanup"                      -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Remove lab temp files ─────────────────────────────────────────────
Write-Host "[1/2] Removing lab temp files..." -ForegroundColor Yellow
$tempDirs = @(
    "$env:TEMP\aidev-lab-13-*",
    "$env:TEMP\safety-lab-14-*",
    "$env:TEMP\capstone-lab-15-*",
    "$env:TEMP\chroma-data",
    "$env:TEMP\langfuse-data"
)
foreach ($pattern in $tempDirs) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}
Write-Host "  Removed MCP, safety, and capstone temp directories" -ForegroundColor Green

# ── Step 2: Stop stale processes ─────────────────────────────────────────────
Write-Host "[2/2] Stopping stale processes..." -ForegroundColor Yellow
Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -match "uvicorn|mcp.*server" } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
Write-Host "  Done" -ForegroundColor Green
Write-Host ""

# Final stats
$disk = Get-PSDrive C
$diskUsedGB  = [math]::Round($disk.Used / 1GB, 1)
$diskFreeGB  = [math]::Round($disk.Free / 1GB, 1)
$diskTotalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 1)
$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$usedGB  = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
Write-Host "  Memory:   ${usedGB} GB used / ${totalGB} GB total"
Write-Host "  Storage C: ${diskUsedGB} GB used / ${diskTotalGB} GB total (${diskFreeGB} GB free)"
Write-Host ""
Write-Host "Cleanup complete." -ForegroundColor Green
Write-Host "Course complete! Thank you for participating." -ForegroundColor Cyan
Write-Host ""
