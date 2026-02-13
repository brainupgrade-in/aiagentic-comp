# day2-setup.ps1 — Day 2: LangChain + Groq API Setup (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Day 2: LangChain + Groq API Setup"
Write-Host "============================================"
Write-Host ""

# Check available resources
Write-Host "Current resource usage:"
$os = Get-CimInstance Win32_OperatingSystem
$totalMB = [math]::Round($os.TotalVisibleMemorySize / 1024)
$freeMB  = [math]::Round($os.FreePhysicalMemory / 1024)
Write-Host "  Memory: Total ${totalMB} MB | Available ${freeMB} MB"
Write-Host ""

# Verify Day 1 cleanup was done
if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "WARNING: Ollama is still installed. Run '.\scripts\day1-cleanup.ps1' first"
    Write-Host "to free ~2 GB of resources."
    Write-Host ""
}

# Check Python venv
Write-Host "[1/3] Verifying Python environment..."
$venvPython = Join-Path $env:USERPROFILE ".venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    & (Join-Path $env:USERPROFILE ".venv\Scripts\Activate.ps1")
    $pyVer = python --version
    Write-Host "  Virtual environment active: $pyVer"
} else {
    try {
        $pyVer = python --version
        Write-Host "  Using system Python: $pyVer"
    } catch {
        Write-Host "  ERROR: Python not found. Install Python 3.10+ from https://python.org"
        exit 1
    }
}

# Verify key packages
Write-Host "[2/3] Verifying LangChain packages..."
$packages = @(
    @("langchain",       "import langchain; print(f'  langchain {langchain.__version__}')"),
    @("langchain-groq",  "import langchain_groq; print(f'  langchain-groq {langchain_groq.__version__}')"),
    @("langchain-chroma","import langchain_chroma; print(f'  langchain-chroma {langchain_chroma.__version__}')"),
    @("langgraph",       "import langgraph; print(f'  langgraph {langgraph.__version__}')")
)
foreach ($pkg in $packages) {
    try {
        python -c $pkg[1] 2>$null
    } catch {
        Write-Host "  WARNING: $($pkg[0]) not installed"
    }
}

# Check Groq API key
Write-Host "[3/3] Checking Groq API key..."
if (-not $env:GROQ_API_KEY) {
    $envFile = Join-Path (Get-Location) ".env"
    if (Test-Path $envFile) {
        Get-Content $envFile | ForEach-Object {
            if ($_ -match '^\s*GROQ_API_KEY\s*=\s*(.+)$') {
                $env:GROQ_API_KEY = $Matches[1].Trim('"', "'", ' ')
            }
        }
    }
}

if ($env:GROQ_API_KEY -and $env:GROQ_API_KEY -ne "gsk_your_key_here") {
    Write-Host "  GROQ_API_KEY is set"
} else {
    Write-Host "  WARNING: GROQ_API_KEY not configured"
    Write-Host "  1. Sign up at https://console.groq.com (free)"
    Write-Host "  2. Create an API key"
    Write-Host "  3. Add to .env file:"
    Write-Host "     GROQ_API_KEY=gsk_your_key_here"
}

Write-Host ""
Write-Host "============================================"
Write-Host "  Day 2 ready!"
Write-Host "============================================"
Write-Host ""
Write-Host "Today's sessions:"
Write-Host "  Session 4: LangChain Fundamentals"
Write-Host "  Session 5: Building RAG Applications"
Write-Host "  Session 6: LangChain Agents & Memory"
Write-Host ""
Write-Host "Quick test (Python):"
Write-Host "  from langchain_groq import ChatGroq"
Write-Host "  llm = ChatGroq(model='llama-3.1-8b-instant')"
Write-Host "  print(llm.invoke('Hello from Day 2!'))"
Write-Host ""
Write-Host "Labs: hands-on\session-4\ through session-6\"
Write-Host ""
