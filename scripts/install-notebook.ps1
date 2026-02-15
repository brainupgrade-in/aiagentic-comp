# install-notebook.ps1 — Jupyter Notebook Setup for VS Code (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  Jupyter Notebook Setup for VS Code"
Write-Host "============================================"
Write-Host ""

# Step 1: Install VS Code Jupyter extension
Write-Host "[1/3] Installing VS Code Jupyter extension..."
$codePath = Get-Command code -ErrorAction SilentlyContinue
if ($codePath) {
    try {
        code --install-extension ms-toolsai.jupyter --force 2>$null
        Write-Host "  Jupyter extension installed"
    } catch {
        Write-Host "  WARNING: Could not install extension (install manually: ms-toolsai.jupyter)"
    }
} else {
    Write-Host "  'code' CLI not found - install the extension manually in VS Code:"
    Write-Host "    Extensions sidebar -> search 'Jupyter' -> Install"
}
Write-Host ""

# Step 2: Install ipykernel
Write-Host "[2/3] Installing ipykernel..."
$RepoDir = Split-Path -Parent $PSScriptRoot
$venvActivate = Join-Path $RepoDir ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
}
pip install --quiet ipykernel 2>$null
if ($LASTEXITCODE -ne 0) {
    pip install ipykernel
}
python -m ipykernel install --user --name agentic-ai --display-name "Agentic AI (Python)" 2>$null
Write-Host "  ipykernel installed"
Write-Host ""

# Step 3: Verify with antigravity
Write-Host "[3/3] Verifying Python + notebook setup..."
python -c @"
import sys
print(f'  Python:    {sys.version.split()[0]}')

import ipykernel
print(f'  ipykernel: {ipykernel.__version__}')

# antigravity - Python Easter egg!
# (In a script it just confirms the module exists; in a notebook it opens xkcd.com/353)
import antigravity
print(f'  antigravity: loaded (try ""import antigravity"" in a notebook!)')

print()
print('  All checks passed!')
"@

Write-Host ""
Write-Host "============================================"
Write-Host "  Notebook setup complete!"
Write-Host "============================================"
Write-Host ""
Write-Host "How to use:"
Write-Host "  1. Open any .ipynb file in VS Code"
Write-Host "  2. Select kernel: 'Agentic AI (Python)' or your venv python"
Write-Host "  3. Run cells with Shift+Enter"
Write-Host ""
Write-Host "Try it:"
Write-Host "  Open hands-on\session-1\lab01_meet_your_llm.ipynb"
Write-Host ""
Write-Host "Fun first cell to try in a notebook:"
Write-Host "  import antigravity"
Write-Host ""
