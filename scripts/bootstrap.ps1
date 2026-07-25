# bootstrap.ps1 — The ONLY script Windows participants need to run.
#
# Installs the three host tools the course needs, then hands off to the shared
# bash setup (which does Python 3.12, the venv, every package for all 5 days,
# the Jupyter kernel, and notebook wiring):
#
#   1. Git for Windows  — provides Git Bash + curl
#   2. uv               — Python version + package manager
#   3. Ollama           — Day 1 local LLM
#   4. scripts/setup.sh — run under Git Bash
#
# Usage (PowerShell, from the repo root):
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
#
# Options:
#   -SkipOllama   Skip the Ollama install and the llama3.2:1b pull (~2 GB)

param(
    [switch]$SkipOllama
)

$ErrorActionPreference = "Stop"
$REPO_DIR = (Resolve-Path "$PSScriptRoot\..").Path

function Write-Step($msg) { Write-Host ""; Write-Host $msg -ForegroundColor Yellow }
function Write-Ok($msg)   { Write-Host "  [OK]   $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "  [WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "  [FAIL] $msg" -ForegroundColor Red }

function Refresh-Path {
    $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" +
                [Environment]::GetEnvironmentVariable("PATH", "User")
}

function Have($cmd) { [bool](Get-Command $cmd -ErrorAction SilentlyContinue) }

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Agentic AI Course - Windows Bootstrap"      -ForegroundColor Cyan
Write-Host "  Git Bash + uv + Ollama, then setup.sh"      -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$hasWinget = Have "winget"
if (-not $hasWinget) {
    Write-Warn "winget not found - falling back to direct downloads."
    Write-Warn "Installers may prompt for administrator approval (UAC)."
}

# ── 1. Git for Windows (gives us Git Bash and curl) ──────────────────────────
Write-Step "[1/4] Git for Windows (Git Bash + curl)..."
$bashCandidates = @(
    "$env:ProgramFiles\Git\bin\bash.exe",
    "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
)
$bashExe = $bashCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($bashExe) {
    Write-Ok "already installed: $bashExe"
} else {
    if ($hasWinget) {
        Write-Host "  Installing via winget..."
        winget install --id Git.Git --source winget --silent `
            --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "  Downloading the latest Git for Windows installer..."
        $release = Invoke-RestMethod "https://api.github.com/repos/git-for-windows/git/releases/latest"
        $asset = $release.assets | Where-Object { $_.name -like "Git-*-64-bit.exe" } | Select-Object -First 1
        if (-not $asset) { Write-Err "Could not find a Git installer. Install manually: https://git-scm.com/download/win"; exit 1 }
        $installer = "$env:TEMP\$($asset.name)"
        Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $installer
        Write-Host "  Running the installer (silent)..."
        Start-Process -FilePath $installer -ArgumentList "/VERYSILENT","/NORESTART","/NOCANCEL","/SP-" -Wait
        Remove-Item $installer -Force
    }
    Refresh-Path
    $bashExe = $bashCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $bashExe) {
        Write-Err "Git Bash not found after install."
        Write-Host "  Open a NEW PowerShell window and re-run this script." -ForegroundColor Red
        exit 1
    }
    Write-Ok "installed: $bashExe"
}

# ── 2. uv (Python toolchain + package manager) ────────────────────────────────
Write-Step "[2/4] uv (Python 3.12 + package manager)..."
Refresh-Path
if (Have "uv") {
    Write-Ok "already installed: $(uv --version)"
} else {
    if ($hasWinget) {
        Write-Host "  Installing via winget..."
        winget install --id astral-sh.uv --source winget --silent `
            --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "  Installing via the official script..."
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    }
    Refresh-Path
    # The uv installer drops the binary here; make sure this session and Git Bash see it
    $uvBin = "$env:USERPROFILE\.local\bin"
    if (Test-Path "$uvBin\uv.exe") { $env:PATH = "$uvBin;$env:PATH" }
    if (-not (Have "uv")) {
        Write-Err "uv not found after install."
        Write-Host "  Open a NEW PowerShell window and re-run this script." -ForegroundColor Red
        exit 1
    }
    Write-Ok "installed: $(uv --version)"
}

# ── 3. Ollama (Day 1 local LLM) ───────────────────────────────────────────────
Write-Step "[3/4] Ollama (Day 1 local LLM)..."
if ($SkipOllama) {
    Write-Warn "skipped (-SkipOllama). Day 1 labs need it - re-run without the flag."
} elseif (Have "ollama") {
    Write-Ok "already installed"
} else {
    if ($hasWinget) {
        Write-Host "  Installing via winget..."
        winget install --id Ollama.Ollama --source winget --silent `
            --accept-package-agreements --accept-source-agreements
    } else {
        Write-Host "  Downloading the Ollama installer..."
        $installer = "$env:TEMP\OllamaSetup.exe"
        Invoke-WebRequest -Uri "https://ollama.com/download/OllamaSetup.exe" -OutFile $installer
        Start-Process -FilePath $installer -ArgumentList "/silent" -Wait
        Remove-Item $installer -Force
    }
    Refresh-Path
    if (Have "ollama") { Write-Ok "installed" }
    else { Write-Warn "Ollama not on PATH yet - setup.sh will warn; re-run this script from a new window to finish it." }
}

# Ollama on Windows runs as a tray app; make sure the API is up before setup.sh pulls a model
if (-not $SkipOllama -and (Have "ollama")) {
    if (-not (Get-Process -Name "ollama*" -ErrorAction SilentlyContinue)) {
        Write-Host "  Starting the Ollama server..."
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 4
    }
}

# ── 4. Hand off to the shared bash setup ──────────────────────────────────────
Write-Step "[4/4] Running scripts/setup.sh under Git Bash..."
Write-Host "  This installs Python 3.12, the venv, all 5 days of packages," -ForegroundColor Gray
Write-Host "  the Jupyter kernel, and points every notebook at it." -ForegroundColor Gray
Write-Host ""

# Git Bash needs an MSYS path: C:\path\to\repo -> /c/path/to/repo
$repoPosix = $REPO_DIR -replace '\\', '/'
if ($repoPosix -match '^([A-Za-z]):(.*)$') {
    $repoPosix = "/" + $Matches[1].ToLower() + $Matches[2]
}
$setupArgs = if ($SkipOllama) { "--skip-ollama" } else { "" }

& $bashExe -lc "export PATH=`"`$HOME/.local/bin:`$PATH`"; cd '$repoPosix' && bash scripts/setup.sh $setupArgs"
$setupExit = $LASTEXITCODE

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
if ($setupExit -eq 0) {
    Write-Host "  Bootstrap complete"                     -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "From here on, use Git Bash for everything:"
    Write-Host "  cd $REPO_DIR"
    Write-Host "  source .venv/Scripts/activate"
    Write-Host "  code hands-on/session-1/lab01_meet_your_llm.ipynb"
    Write-Host ""
    Write-Host "Add your Groq API key to .env (free at https://console.groq.com):"
    Write-Host "  notepad .env"
} else {
    Write-Host "  Bootstrap FAILED (setup.sh exit $setupExit)" -ForegroundColor Red
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Open Git Bash in the repo and re-run to see the full output:" -ForegroundColor Yellow
    Write-Host "  bash scripts/setup.sh"
    exit $setupExit
}
Write-Host ""
