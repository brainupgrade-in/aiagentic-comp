# day1-cleanup.ps1 — Day 1: Cleanup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 1: Cleanup (freeing ~2 GB)"
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

# Stop Ollama
Write-Host "[1/4] Stopping Ollama..."
Stop-Process -Name "ollama*" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Remove model
Write-Host "[2/4] Removing llama3.2:1b model..."
try { ollama rm llama3.2:1b 2>$null } catch {}

# Uninstall Ollama
Write-Host "[3/4] Uninstalling Ollama..."
$uninstaller = Get-ChildItem "C:\Users\$env:USERNAME\AppData\Local\Programs\Ollama\unins*.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
if ($uninstaller) {
    Start-Process -FilePath $uninstaller.FullName -ArgumentList "/SILENT" -Wait
} else {
    Write-Host "  Ollama uninstaller not found — remove manually from Add/Remove Programs if needed"
}
Remove-Item "$env:USERPROFILE\.ollama" -Recurse -Force -ErrorAction SilentlyContinue

# Clean temp files from Day 1 labs
Write-Host "[4/4] Cleaning lab temp files..."
Remove-Item "$env:TEMP\ailab-01-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\aidev-lab-02-*" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "$env:TEMP\ailab-03-*" -Recurse -Force -ErrorAction SilentlyContinue

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
Write-Host "Done! From Day 2 onwards, use Groq API (free, cloud-hosted)."
Write-Host ""
