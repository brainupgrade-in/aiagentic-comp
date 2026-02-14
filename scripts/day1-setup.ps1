# day1-setup.ps1 — Day 1: Ollama + Local LLM Setup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 1: Ollama + Local LLM Setup"
Write-Host "============================================"
Write-Host ""

# Check available resources
Write-Host "Current resource usage:"
$os = Get-CimInstance Win32_OperatingSystem
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
$freeMB  = [math]::Round($os.FreePhysicalMemory / 1024)
Write-Host "  Memory: Total ${totalMB} MB | Available ${freeMB} MB"
Write-Host ""

# Install Ollama
Write-Host "[1/2] Installing Ollama..."
Write-Host "  Downloading Ollama installer for Windows..."
$installerUrl = "https://ollama.com/download/OllamaSetup.exe"
$installerPath = "$env:TEMP\OllamaSetup.exe"
Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
Write-Host "  Running installer (follow the prompts)..."
Start-Process -FilePath $installerPath -Wait
Remove-Item $installerPath -ErrorAction SilentlyContinue

# Pull model
Write-Host "[2/2] Pulling llama3.2:1b model (~1.3 GB)..."
Start-Sleep -Seconds 5
ollama pull llama3.2:1b

Write-Host ""
Write-Host "============================================"
Write-Host "  Day 1 setup complete!"
Write-Host "============================================"
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
Write-Host "Labs (open in VS Code or JupyterLab):"
Write-Host "  hands-on\session-1\lab01_meet_your_llm.ipynb"
Write-Host "  hands-on\session-2\lab01_coding_agent_anatomy.ipynb"
Write-Host "  hands-on\session-3\lab01_chain_of_thought.ipynb"
Write-Host ""
Write-Host "IMPORTANT: Run '.\scripts\day1-cleanup.ps1' at end of day"
Write-Host "to free ~2 GB for remaining days."
Write-Host ""
