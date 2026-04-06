# day1-cleanup.ps1 — Day 1: Cleanup (freeing ~2 GB) — Windows PowerShell
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day1-cleanup.ps1

$ErrorActionPreference = "SilentlyContinue"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 1: Cleanup (freeing ~2 GB)"           -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Before stats
Write-Host "Before cleanup:" -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$usedGB  = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$disk = Get-PSDrive C
$diskUsedGB  = [math]::Round(($disk.Used)  / 1GB, 1)
$diskFreeGB  = [math]::Round(($disk.Free)  / 1GB, 1)
$diskTotalGB = [math]::Round(($disk.Used + $disk.Free) / 1GB, 1)
Write-Host "  Memory: ${usedGB} GB used / ${totalGB} GB total"
Write-Host "  Storage C: ${diskUsedGB} GB used / ${diskTotalGB} GB total (${diskFreeGB} GB free)"
Write-Host ""

# ── Step 1: Stop Ollama ───────────────────────────────────────────────────────
Write-Host "[1/4] Stopping Ollama..." -ForegroundColor Yellow
Stop-Process -Name "ollama" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Write-Host "  Done"

# ── Step 2: Remove model ──────────────────────────────────────────────────────
Write-Host "[2/4] Removing llama3.2:1b model..." -ForegroundColor Yellow
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    ollama rm llama3.2:1b 2>$null
    Write-Host "  Done"
} else {
    Write-Host "  Ollama not found, skipping model removal"
}

# ── Step 3: Uninstall Ollama ──────────────────────────────────────────────────
Write-Host "[3/4] Removing Ollama data and binaries..." -ForegroundColor Yellow

# Remove Ollama model cache
$ollamaData = "$env:USERPROFILE\.ollama"
if (Test-Path $ollamaData) {
    Remove-Item -Recurse -Force $ollamaData
    Write-Host "  Removed $ollamaData"
}

# Remove Ollama from LocalAppData (Windows installer location)
$ollamaApp = "$env:LOCALAPPDATA\Programs\Ollama"
if (Test-Path $ollamaApp) {
    Remove-Item -Recurse -Force $ollamaApp
    Write-Host "  Removed $ollamaApp"
}

# Run uninstaller if present
$uninstaller = "$env:LOCALAPPDATA\Programs\Ollama\uninstall.exe"
if (Test-Path $uninstaller) {
    Write-Host "  Running Ollama uninstaller..."
    Start-Process -FilePath $uninstaller -ArgumentList "/S" -Wait
}

Write-Host "  Done"

# ── Step 4: Clean temp lab files ─────────────────────────────────────────────
Write-Host "[4/4] Cleaning lab temp files..." -ForegroundColor Yellow
$tmpDirs = @(
    "$env:TEMP\aidev-lab-02-*",
    "$env:TEMP\k8s-lab-03-*"
)
foreach ($pattern in $tmpDirs) {
    Get-ChildItem -Path $pattern -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
}
Write-Host "  Done"

Write-Host ""

# After stats
Write-Host "After cleanup:" -ForegroundColor Yellow
$os2 = Get-CimInstance Win32_OperatingSystem
$usedGB2  = [math]::Round(($os2.TotalVisibleMemorySize - $os2.FreePhysicalMemory) / 1MB, 1)
$disk2 = Get-PSDrive C
$diskUsedGB2  = [math]::Round(($disk2.Used) / 1GB, 1)
$diskFreeGB2  = [math]::Round(($disk2.Free) / 1GB, 1)
Write-Host "  Memory: ${usedGB2} GB used / ${totalGB} GB total"
Write-Host "  Storage C: ${diskUsedGB2} GB used / ${diskTotalGB} GB total (${diskFreeGB2} GB free)"

Write-Host ""
Write-Host "Done! From Day 2 onwards, use Groq API (free, cloud-hosted)." -ForegroundColor Green
Write-Host ""
