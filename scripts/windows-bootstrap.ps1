# windows-bootstrap.ps1
# Run this ONCE on Windows to:
#   1. Install Git for Windows (Git Bash) if missing
#   2. Configure VS Code to use Git Bash as default terminal
#   3. Run initial-setup.sh through Git Bash
#
# Usage (from repo root in PowerShell as normal user):
#   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
#   .\scripts\windows-bootstrap.ps1

$ErrorActionPreference = "Stop"

$GIT_BASH_PATHS = @(
    "C:\Program Files\Git\bin\bash.exe",
    "C:\Program Files (x86)\Git\bin\bash.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Agentic AI Course — Windows Bootstrap" -ForegroundColor Cyan
Write-Host "============================================"
Write-Host ""

# ---------------------------------------------------------------------------
# Step 1: Locate or install Git Bash
# ---------------------------------------------------------------------------
Write-Host "[1/3] Checking for Git Bash..." -ForegroundColor Yellow

$BASH = $null
foreach ($p in $GIT_BASH_PATHS) {
    if (Test-Path $p) { $BASH = $p; break }
}

if (-not $BASH) {
    Write-Host "  Git Bash not found. Attempting install via winget..." -ForegroundColor Yellow

    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        winget install --id Git.Git -e --source winget --silent --accept-package-agreements --accept-source-agreements
        # Re-check after install
        foreach ($p in $GIT_BASH_PATHS) {
            if (Test-Path $p) { $BASH = $p; break }
        }
    }

    if (-not $BASH) {
        Write-Host ""
        Write-Host "  ERROR: Git Bash not found and automatic install failed." -ForegroundColor Red
        Write-Host "  Please install Git for Windows manually from https://git-scm.com/download/win" -ForegroundColor Red
        Write-Host "  Then re-run this script."
        exit 1
    }

    Write-Host "  Git installed successfully." -ForegroundColor Green
} else {
    Write-Host "  Found Git Bash at: $BASH" -ForegroundColor Green
}
Write-Host ""

# ---------------------------------------------------------------------------
# Step 2: Configure VS Code to use Git Bash as default terminal
# ---------------------------------------------------------------------------
Write-Host "[2/3] Configuring VS Code to use Git Bash..." -ForegroundColor Yellow

$VS_CODE_SETTINGS = "$env:APPDATA\Code\User\settings.json"
$BASH_ESCAPED = $BASH -replace '\\', '\\\\'

if (Test-Path $VS_CODE_SETTINGS) {
    $settings = Get-Content $VS_CODE_SETTINGS -Raw | ConvertFrom-Json
} else {
    New-Item -ItemType File -Path $VS_CODE_SETTINGS -Force | Out-Null
    $settings = [PSCustomObject]@{}
}

# Set Git Bash as the default terminal profile
$settings | Add-Member -Force -NotePropertyName "terminal.integrated.defaultProfile.windows" -NotePropertyValue "Git Bash"
$settings | Add-Member -Force -NotePropertyName "terminal.integrated.profiles.windows" -NotePropertyValue ([PSCustomObject]@{
    "Git Bash" = [PSCustomObject]@{
        source = "Git Bash"
        icon   = "terminal-bash"
    }
})

# Point VS Code Python interpreter to the venv (repo-relative, works cross-platform)
$settings | Add-Member -Force -NotePropertyName "python.defaultInterpreterPath" -NotePropertyValue '${workspaceFolder}/.venv/bin/python'
$settings | Add-Member -Force -NotePropertyName "jupyter.kernelPicker.type" -NotePropertyValue "default"

$settings | ConvertTo-Json -Depth 10 | Set-Content $VS_CODE_SETTINGS -Encoding UTF8
Write-Host "  VS Code settings updated: $VS_CODE_SETTINGS" -ForegroundColor Green
Write-Host "  Reload VS Code after setup completes (Ctrl+Shift+P -> Developer: Reload Window)" -ForegroundColor Cyan
Write-Host ""

# ---------------------------------------------------------------------------
# Step 3: Run initial-setup.sh through Git Bash
# ---------------------------------------------------------------------------
Write-Host "[3/3] Running initial-setup.sh via Git Bash..." -ForegroundColor Yellow
Write-Host ""

# Convert Windows path to Unix path for Git Bash (e.g. C:\Users\foo -> /c/Users/foo)
$WIN_PATH  = (Get-Location).Path
$DRIVE     = $WIN_PATH.Substring(0,1).ToLower()
$REST      = $WIN_PATH.Substring(2) -replace '\\', '/'
$REPO_UNIX = "/$DRIVE$REST"

# Verify script exists
if (-not (Test-Path "scripts\initial-setup.sh")) {
    Write-Host "  ERROR: scripts\initial-setup.sh not found." -ForegroundColor Red
    Write-Host "  Make sure you are running this from the repo root directory."
    exit 1
}

& $BASH --login -c "cd '$REPO_UNIX' && bash scripts/initial-setup.sh"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "  ERROR: initial-setup.sh failed (exit code $LASTEXITCODE)." -ForegroundColor Red
    Write-Host "  Check the output above for details."
    exit $LASTEXITCODE
}

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Windows bootstrap complete!" -ForegroundColor Green
Write-Host "============================================"
Write-Host ""
Write-Host "You can now run any course script from a Git Bash terminal:"
Write-Host "  bash scripts/day1-setup.sh"
Write-Host "  bash scripts/day2-setup.sh"
Write-Host "  ... etc"
Write-Host ""
Write-Host "Or open a Git Bash terminal in VS Code:" -ForegroundColor Cyan
Write-Host "  Ctrl+Shift+P -> Terminal: Create New Terminal"
Write-Host "  (Git Bash is now the default terminal in VS Code)"
Write-Host ""
Write-Host "Next step: Edit .env and add your Groq API key:"
Write-Host "  GROQ_API_KEY=gsk_your_key_here"
Write-Host "  (Get one free at https://console.groq.com)"
Write-Host ""
