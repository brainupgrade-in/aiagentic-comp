# install-opencode.ps1 — Install opencode AI coding assistant (Windows PowerShell)
#
# Usage (from repo root, in PowerShell):
#   .\scripts\install-opencode.ps1
#
# What it does:
#   1. Installs opencode via official installer
#   2. Verifies the installation
#   3. Prints auth and usage instructions

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  OpenCode: AI Coding Assistant Setup"      -ForegroundColor Cyan
Write-Host "  (Windows PowerShell)"                     -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ── Step 1: Install opencode ──────────────────────────────────────────────────
Write-Host "[1/2] Installing opencode..." -ForegroundColor Yellow

$opencodeCmd = Get-Command opencode -ErrorAction SilentlyContinue
if ($opencodeCmd) {
    $ver = & opencode --version 2>&1
    Write-Host "  opencode already installed: $ver" -ForegroundColor Green
} else {
    Write-Host "  Running official installer..."
    $installScript = "$env:TEMP\opencode-install.ps1"
    Invoke-WebRequest -Uri "https://opencode.ai/install" -OutFile $installScript -UseBasicParsing
    & powershell -ExecutionPolicy Bypass -File $installScript
    Remove-Item $installScript -Force -ErrorAction SilentlyContinue

    # Refresh PATH in this session
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH", "User")

    $opencodeCmd = Get-Command opencode -ErrorAction SilentlyContinue
    if (-not $opencodeCmd) {
        Write-Host ""
        Write-Host "  opencode installed but not yet on PATH." -ForegroundColor Yellow
        Write-Host "  Open a new PowerShell window and run: opencode --version" -ForegroundColor Yellow
        Write-Host "  Then re-run this script to verify."
        exit 0
    }
    $ver = & opencode --version 2>&1
    Write-Host "  opencode installed: $ver" -ForegroundColor Green
}
Write-Host ""

# ── Step 2: Verify ────────────────────────────────────────────────────────────
Write-Host "[2/2] Verifying installation..." -ForegroundColor Yellow
$opencodeExe = (Get-Command opencode).Source
Write-Host "  Binary: $opencodeExe" -ForegroundColor Green
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  OpenCode ready!"                           -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Authentication (choose one):"
Write-Host ""
Write-Host "  Option A - GitHub Copilot (free tier available):"
Write-Host "    opencode        # launch TUI, then type /connect"
Write-Host ""
Write-Host "  Option B - Groq API (free, no login needed):"
Write-Host "    `$env:GROQ_API_KEY = 'gsk_your_key_here'"
Write-Host "    # or add GROQ_API_KEY to .env in the repo root"
Write-Host ""
Write-Host "Usage:"
Write-Host "  opencode                       # interactive TUI"
Write-Host "  opencode 'explain this code'   # single prompt"
Write-Host ""
Write-Host "TUI tips:"
Write-Host "  Tab          - switch between build / plan agents"
Write-Host "  /connect     - authenticate with a provider"
Write-Host "  /help        - show all commands"
Write-Host ""
