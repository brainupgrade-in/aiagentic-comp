# check-resources.ps1 — Resource Monitor (Windows)
$ErrorActionPreference = "Continue"

Write-Host "============================================"
Write-Host "  Resource Monitor"
Write-Host "============================================"
Write-Host ""

# Memory
Write-Host "--- Memory ---"
$os = Get-CimInstance Win32_OperatingSystem
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
$freeMB  = [math]::Round($os.FreePhysicalMemory / 1024)
$usedMB  = $totalMB - $freeMB
Write-Host "  Total: ${totalMB} MB | Used: ${usedMB} MB | Available: ${freeMB} MB"
Write-Host ""

# Storage
Write-Host "--- Storage ---"
$disk = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$totalGB = [math]::Round($disk.Size / 1GB, 1)
$freeGB  = [math]::Round($disk.FreeSpace / 1GB, 1)
$usedGB  = [math]::Round($totalGB - $freeGB, 1)
$pct     = [math]::Round(($usedGB / $totalGB) * 100)
Write-Host "  Total: ${totalGB} GB | Used: ${usedGB} GB (${pct}%) | Available: ${freeGB} GB"
Write-Host ""

# Python processes
Write-Host "--- Python Processes ---"
$procs = Get-Process -Name python*, uvicorn -ErrorAction SilentlyContinue
if ($procs) {
    Write-Host "  Running processes:"
    foreach ($p in $procs) {
        $mem = [math]::Round($p.WorkingSet64 / 1MB, 1)
        Write-Host "    - PID $($p.Id): $($p.ProcessName) (${mem} MB)"
    }
} else {
    Write-Host "  No running Python/uvicorn processes"
}
Write-Host ""

# Ollama
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "--- Ollama ---"
    Write-Host "  Installed models:"
    ollama list 2>$null | ForEach-Object { Write-Host "    $_" }
    Write-Host ""
}

# Top processes by memory
Write-Host "--- Top 5 Processes (by memory) ---"
Write-Host ("  {0,-10} {1}" -f "MEM(MB)", "PROCESS")
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 5 | ForEach-Object {
    $mem = [math]::Round($_.WorkingSet64 / 1MB, 1)
    Write-Host ("  {0,-10} {1}" -f $mem, $_.ProcessName)
}
Write-Host ""
