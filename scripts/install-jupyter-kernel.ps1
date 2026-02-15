# install-jupyter-kernel.ps1 — Install Jupyter kernel spec (Windows)
$ErrorActionPreference = "Stop"

Write-Host "Installing Jupyter kernel spec for Gheware Agentic AI course..." -ForegroundColor Green

# Get the project root directory
$RepoDir = Split-Path -Parent $PSScriptRoot
$venvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"

# Check if virtual environment exists
if (-not (Test-Path $venvPython)) {
    Write-Host "Warning: Virtual environment not found at $RepoDir\.venv" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..."
    Set-Location $RepoDir
    python -m venv .venv
    & (Join-Path $RepoDir ".venv\Scripts\Activate.ps1")
    pip install --upgrade pip
    pip install ipykernel jupyter
} else {
    Write-Host "Found Python virtual environment at $venvPython"
    & (Join-Path $RepoDir ".venv\Scripts\Activate.ps1")
}

# Install ipykernel if not already installed
Write-Host "Ensuring ipykernel is installed..."
& $venvPython -m pip install ipykernel jupyter --quiet

# Install the kernel spec
Write-Host "Installing kernel spec..."
& $venvPython -m ipykernel install `
    --user `
    --name gheware-agentic-ai `
    --display-name "Python 3 (Gheware Agentic AI)"

Write-Host ""
Write-Host "Kernel spec installed successfully" -ForegroundColor Green

# Verify installation
Write-Host ""
Write-Host "Installed kernels:"
jupyter kernelspec list

Write-Host ""
Write-Host "Done! You can now select 'Python 3 (Gheware Agentic AI)' as the kernel in VS Code or Jupyter." -ForegroundColor Green
