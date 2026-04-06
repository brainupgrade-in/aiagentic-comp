# day1-setup.ps1 — Day 1: Ollama + Local LLM Setup (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\day1-setup.ps1

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 1: Ollama + Local LLM Setup"          -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Resource check ────────────────────────────────────────────────────────────
Write-Host "Current resource usage:" -ForegroundColor Yellow
$os = Get-CimInstance Win32_OperatingSystem
$totalGB  = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB   = [math]::Round($os.FreePhysicalMemory     / 1MB, 1)
$usedGB   = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1MB, 1)
Write-Host "  Memory: ${usedGB} GB used / ${totalGB} GB total (${freeGB} GB free)"
Write-Host ""

# ── Step 1: Install Ollama ────────────────────────────────────────────────────
Write-Host "[1/2] Installing Ollama..." -ForegroundColor Yellow

$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollamaCmd) {
    Write-Host "  Ollama already installed: $(ollama --version 2>&1)" -ForegroundColor Green
} else {
    $installer = "$env:TEMP\OllamaSetup.exe"
    Write-Host "  Downloading Ollama installer..."
    Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer
    Write-Host "  Running installer (follow prompts if any)..."
    Start-Process -FilePath $installer -Wait
    Remove-Item $installer -Force

    # Refresh PATH so 'ollama' is found in this session
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH", "User")

    $ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
    if (-not $ollamaCmd) {
        Write-Host "  ERROR: Ollama not found after install." -ForegroundColor Red
        Write-Host "  Open a NEW PowerShell window and re-run this script." -ForegroundColor Red
        exit 1
    }
    Write-Host "  Ollama installed successfully" -ForegroundColor Green
}
Write-Host ""

# ── Step 2: Start Ollama service & pull model ─────────────────────────────────
Write-Host "[2/2] Pulling llama3.2:1b model (~1.3 GB)..." -ForegroundColor Yellow

# Ollama on Windows auto-starts as a tray app; ensure server is running
$ollamaProc = Get-Process -Name "ollama" -ErrorAction SilentlyContinue
if (-not $ollamaProc) {
    Write-Host "  Starting Ollama server..."
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 4
}

ollama pull llama3.2:1b
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Day 1 setup complete!"                    -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 1: Introduction to Agentic AI"
Write-Host "  Session 2: AI Coding Assistants & Vibe Coding"
Write-Host "  Session 3: Reasoning, Planning & Tool Use"
Write-Host ""
Write-Host "Test it:"
Write-Host "  ollama run llama3.2:1b 'Hello, world!'"
Write-Host ""
Write-Host "In Python:"
Write-Host "  from langchain_ollama import ChatOllama"
Write-Host "  llm = ChatOllama(model='llama3.2:1b')"
Write-Host "  print(llm.invoke('Hello'))"
Write-Host ""
Write-Host "Labs (open in VS Code):"
Write-Host "  hands-on\session-1\lab01_meet_your_llm.ipynb"
Write-Host "  hands-on\session-2\lab01_coding_agent_anatomy.ipynb"
Write-Host "  hands-on\session-3\lab01_chain_of_thought.ipynb"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day1-cleanup.ps1' at end of day" -ForegroundColor Yellow
Write-Host "to free ~2 GB for remaining days." -ForegroundColor Yellow
Write-Host ""
