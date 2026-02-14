# Session 11: LangFuse Setup (Mock Mode) - PowerShell Version
# Run with: powershell -ExecutionPolicy Bypass -File session11-langfuse-setup.ps1

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Session 11: LangFuse Setup (Mock Mode)" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Get repo root directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoDir = Split-Path -Parent $ScriptDir

# Verify Python environment
Write-Host "[1/5] Verifying Python environment..." -ForegroundColor Yellow

# Check for venv
$VenvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (Test-Path $VenvPython) {
    $PythonCmd = $VenvPython
    $PythonVersion = & $PythonCmd --version 2>&1
    Write-Host "  ✓ Virtual environment active: $PythonVersion" -ForegroundColor Green
} else {
    try {
        $PythonVersion = python --version 2>&1
        $PythonCmd = "python"
        Write-Host "  ✓ System Python: $PythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ ERROR: Python 3 not found" -ForegroundColor Red
        Write-Host "  Install Python 3.10+ from https://www.python.org/downloads/" -ForegroundColor Red
        exit 1
    }
}

# Verify LangFuse package
Write-Host ""
Write-Host "[2/5] Verifying LangFuse package..." -ForegroundColor Yellow

$LangfuseCheck = & $PythonCmd -c "import langfuse; print(f'langfuse {langfuse.__version__}')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ $LangfuseCheck" -ForegroundColor Green
} else {
    Write-Host "  ✗ WARNING: langfuse not installed" -ForegroundColor Red
    Write-Host ""
    $Install = Read-Host "Install langfuse now? (y/n)"
    if ($Install -eq 'y' -or $Install -eq 'Y') {
        & $PythonCmd -m pip install "langfuse>=2.50"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ langfuse installed" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Installation failed" -ForegroundColor Red
        }
    } else {
        Write-Host "  Skipping installation. Labs may fail." -ForegroundColor Yellow
    }
}

# Create mock LangFuse trace directory
Write-Host ""
Write-Host "[3/5] Creating mock LangFuse trace directory..." -ForegroundColor Yellow

$TraceDir = "$env:TEMP\langfuse-traces"
if (-not $TraceDir) {
    $TraceDir = "C:\tmp\langfuse-traces"
}

if (Test-Path $TraceDir) {
    Write-Host "  ℹ Directory already exists: $TraceDir" -ForegroundColor Cyan
    $Clear = Read-Host "Clear existing traces? (y/n)"
    if ($Clear -eq 'y' -or $Clear -eq 'Y') {
        Remove-Item "$TraceDir\*" -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "  ✓ Cleared existing traces" -ForegroundColor Green
    }
} else {
    New-Item -ItemType Directory -Path $TraceDir -Force | Out-Null
    Write-Host "  ✓ Created: $TraceDir" -ForegroundColor Green
}

# Verify environment variables
Write-Host ""
Write-Host "[4/5] Checking LangFuse environment variables..." -ForegroundColor Yellow

$MissingVars = @()

# Try to load from .env file
$EnvFile = Join-Path $RepoDir ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.*)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [System.Environment]::SetEnvironmentVariable($name, $value, 'Process')
        }
    }
}

# Check LANGFUSE_PUBLIC_KEY
if (-not $env:LANGFUSE_PUBLIC_KEY) {
    $MissingVars += "LANGFUSE_PUBLIC_KEY"
    Write-Host "  ✗ LANGFUSE_PUBLIC_KEY not set" -ForegroundColor Red
} else {
    Write-Host "  ✓ LANGFUSE_PUBLIC_KEY is set" -ForegroundColor Green
}

# Check LANGFUSE_SECRET_KEY
if (-not $env:LANGFUSE_SECRET_KEY) {
    $MissingVars += "LANGFUSE_SECRET_KEY"
    Write-Host "  ✗ LANGFUSE_SECRET_KEY not set" -ForegroundColor Red
} else {
    Write-Host "  ✓ LANGFUSE_SECRET_KEY is set" -ForegroundColor Green
}

# Check LANGFUSE_HOST
if (-not $env:LANGFUSE_HOST) {
    $MissingVars += "LANGFUSE_HOST"
    Write-Host "  ✗ LANGFUSE_HOST not set" -ForegroundColor Red
} else {
    Write-Host "  ✓ LANGFUSE_HOST is set: $env:LANGFUSE_HOST" -ForegroundColor Green
}

# Warn if variables missing
if ($MissingVars.Count -gt 0) {
    Write-Host ""
    Write-Host "  WARNING: Missing environment variables:" -ForegroundColor Yellow
    foreach ($var in $MissingVars) {
        Write-Host "    - $var" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "  For mock mode, add these to .env:" -ForegroundColor Cyan
    Write-Host "    LANGFUSE_PUBLIC_KEY=pk-lf-mock-public-key"
    Write-Host "    LANGFUSE_SECRET_KEY=sk-lf-mock-secret-key"
    Write-Host "    LANGFUSE_HOST=http://localhost:8000"
    Write-Host ""
    Write-Host "  Copy from .env.example:" -ForegroundColor Cyan
    Write-Host "    Copy-Item .env.example .env"
    Write-Host ""
}

# Create test script to verify mock setup
Write-Host ""
Write-Host "[5/5] Creating mock LangFuse test..." -ForegroundColor Yellow

$TestScript = Join-Path $TraceDir "test_mock_langfuse.py"

$TestScriptContent = @'
#!/usr/bin/env python3
"""Test script for MockLangfuse setup."""
import json
import os
from datetime import datetime

class MockLangfuse:
    """Mock LangFuse client that logs traces to local JSON files."""

    def __init__(self, public_key, secret_key, host, output_dir=None):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host
        if output_dir is None:
            import tempfile
            output_dir = os.path.join(tempfile.gettempdir(), "langfuse-traces")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._traces = []

    def trace(self, name, metadata=None):
        trace_data = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "generations": [],
        }
        self._traces.append(trace_data)
        return MockTrace(trace_data)

    def flush(self):
        output_file = os.path.join(self.output_dir, "traces.json")
        with open(output_file, "w") as f:
            json.dump(self._traces, f, indent=2)
        print(f"✓ Flushed {len(self._traces)} traces to {output_file}")
        return len(self._traces)

    def get_traces(self):
        output_file = os.path.join(self.output_dir, "traces.json")
        if os.path.exists(output_file):
            with open(output_file) as f:
                return json.load(f)
        return []

class MockTrace:
    def __init__(self, trace_data):
        self._data = trace_data

    def generation(self, name, model=None, input=None, output=None):
        gen = {"name": name, "model": model, "input": input, "output": output}
        self._data["generations"].append(gen)
        return gen

if __name__ == "__main__":
    print("Testing MockLangfuse setup...")
    print()

    # Initialize mock client
    client = MockLangfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY", "pk-test"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY", "sk-test"),
        host=os.getenv("LANGFUSE_HOST", "http://localhost:8000"),
    )

    # Create a test trace
    trace = client.trace(name="test-session-11", metadata={"test": True})
    trace.generation(
        name="test-generation",
        model="llama-3.3-70b-versatile",
        input="What is LangFuse?",
        output="LangFuse is an open-source observability platform for LLM applications.",
    )

    # Flush traces
    count = client.flush()

    # Verify traces
    traces = client.get_traces()
    print(f"✓ Retrieved {len(traces)} trace(s)")
    print()
    print("Sample trace structure:")
    print(json.dumps(traces[0], indent=2))
    print()
    print("✓ MockLangfuse setup verified successfully!")
'@

Set-Content -Path $TestScript -Value $TestScriptContent -Encoding UTF8

# Run the test
Write-Host ""
& $PythonCmd $TestScript

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Session 11 LangFuse Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Configuration:" -ForegroundColor Green
Write-Host "  • Mock mode enabled (local JSON logging)"
Write-Host "  • Trace directory: $TraceDir"
Write-Host "  • Test script: $TestScript"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open hands-on/session-11/ labs in VS Code or JupyterLab"
Write-Host "  2. Labs use MockLangfuse class for local trace logging"
Write-Host "  3. View traces: Get-Content $TraceDir\traces.json | ConvertFrom-Json"
Write-Host ""
Write-Host "Key labs:" -ForegroundColor Cyan
Write-Host "  • lab01: LangFuse fundamentals"
Write-Host "  • lab02: LangFuse setup & deployment"
Write-Host "  • lab03: LangChain integration"
Write-Host "  • lab04: Tracing agents"
Write-Host "  • lab05: Feedback & evaluation"
Write-Host ""
Write-Host "To re-run test: python $TestScript" -ForegroundColor Cyan
Write-Host ""
