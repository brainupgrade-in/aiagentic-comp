# test-langfuse-server.ps1 — LangFuse Server Test (Windows)
$ErrorActionPreference = "Stop"

Write-Host "============================================"
Write-Host "  LangFuse Server Test"
Write-Host "============================================"
Write-Host ""

$RepoDir = Split-Path -Parent $PSScriptRoot
$env:LANGFUSE_SECRET_KEY = "sk-lf-course-secret"
$env:LANGFUSE_PUBLIC_KEY = "pk-lf-course-key"
$env:LANGFUSE_HOST = "http://localhost:3000"

# Check if virtual environment exists
$venvPython = Join-Path $RepoDir ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "ERROR: Virtual environment not found at $RepoDir\.venv"
    Write-Host "Run: python -m venv $RepoDir\.venv; $RepoDir\.venv\Scripts\Activate.ps1; pip install -r requirements.txt"
    exit 1
}

& (Join-Path $RepoDir ".venv\Scripts\Activate.ps1")

# Check if required packages are installed
Write-Host "[1/6] Checking dependencies..."
try {
    python -c "import fastapi, uvicorn, pydantic" 2>$null
    Write-Host "  All dependencies installed"
} catch {
    Write-Host "ERROR: Missing dependencies. Install with: pip install -r requirements.txt"
    exit 1
}

# Start the server in background
Write-Host ""
Write-Host "[2/6] Starting LangFuse server..."
$langfuseScript = Join-Path $RepoDir "scripts\langfuse-server.py"
$logFile = Join-Path $env:TEMP "langfuse-server-test.log"
$errFile = Join-Path $env:TEMP "langfuse-server-test-err.log"
$proc = Start-Process -FilePath $venvPython -ArgumentList $langfuseScript `
    -WindowStyle Hidden -PassThru -RedirectStandardOutput $logFile -RedirectStandardError $errFile
Write-Host "  Server started (PID: $($proc.Id))"

# Wait for server to start
Write-Host ""
Write-Host "[3/6] Waiting for server to be ready..."
Start-Sleep -Seconds 3

# Check if server is running
if ($proc.HasExited) {
    Write-Host "  ERROR: Server failed to start. Log output:"
    if (Test-Path $logFile) { Get-Content $logFile }
    if (Test-Path $errFile) { Get-Content $errFile }
    exit 1
}

# Test health endpoint
Write-Host ""
Write-Host "[4/6] Testing health endpoint..."
try {
    $healthResponse = (Invoke-WebRequest -Uri "http://localhost:3000/api/public/health" -UseBasicParsing -TimeoutSec 5).Content
    if ($healthResponse -match '"status"\s*:\s*"ok"') {
        Write-Host "  Health check passed"
        Write-Host "  Response: $healthResponse"
    } else {
        Write-Host "  ERROR: Health check failed"
        Write-Host "  Response: $healthResponse"
        Stop-Process -Id $proc.Id -Force
        exit 1
    }
} catch {
    Write-Host "  ERROR: Could not connect to health endpoint"
    Write-Host "  $_"
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# Test API endpoints
Write-Host ""
Write-Host "[5/6] Testing API endpoints..."

# Create a trace
$traceBody = '{"name":"test_trace","userId":"test-user","sessionId":"test-session","tags":["test"]}'
$traceResponse = (Invoke-WebRequest -Uri "http://localhost:3000/api/public/traces" `
    -Method POST -Headers @{"Authorization"="Bearer $env:LANGFUSE_SECRET_KEY"; "Content-Type"="application/json"} `
    -Body $traceBody -UseBasicParsing -TimeoutSec 5).Content

if ($traceResponse -match '"id"\s*:\s*"([^"]+)"') {
    $traceId = $Matches[1]
    Write-Host "  Created trace: $traceId"
} else {
    Write-Host "  ERROR: Failed to create trace"
    Write-Host "  Response: $traceResponse"
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# Create a generation
$genBody = @"
{"traceId":"$traceId","name":"test_generation","model":"llama-3.3-70b-versatile","input":"test input","output":"test output","usage":{"input_tokens":10,"output_tokens":20}}
"@
$genResponse = (Invoke-WebRequest -Uri "http://localhost:3000/api/public/generations" `
    -Method POST -Headers @{"Authorization"="Bearer $env:LANGFUSE_SECRET_KEY"; "Content-Type"="application/json"} `
    -Body $genBody -UseBasicParsing -TimeoutSec 5).Content

if ($genResponse -match '"cost"') {
    Write-Host "  Created generation with cost calculation"
} else {
    Write-Host "  ERROR: Failed to create generation"
    Write-Host "  Response: $genResponse"
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# Create a score
$scoreBody = @"
{"traceId":"$traceId","name":"user_rating","value":5,"comment":"Excellent!"}
"@
$scoreResponse = (Invoke-WebRequest -Uri "http://localhost:3000/api/public/scores" `
    -Method POST -Headers @{"Authorization"="Bearer $env:LANGFUSE_SECRET_KEY"; "Content-Type"="application/json"} `
    -Body $scoreBody -UseBasicParsing -TimeoutSec 5).Content

if ($scoreResponse -match '"value"\s*:\s*5') {
    Write-Host "  Created score"
} else {
    Write-Host "  ERROR: Failed to create score"
    Write-Host "  Response: $scoreResponse"
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# Get traces
$tracesResponse = (Invoke-WebRequest -Uri "http://localhost:3000/api/public/traces?userId=test-user" `
    -Headers @{"Authorization"="Bearer $env:LANGFUSE_SECRET_KEY"} `
    -UseBasicParsing -TimeoutSec 5).Content

if ($tracesResponse -match '"totalItems"\s*:\s*1') {
    Write-Host "  Retrieved traces successfully"
} else {
    Write-Host "  ERROR: Failed to retrieve traces"
    Write-Host "  Response: $tracesResponse"
    Stop-Process -Id $proc.Id -Force
    exit 1
}

# Cleanup
Write-Host ""
Write-Host "[6/6] Cleaning up..."
Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
Remove-Item "$env:TEMP\langfuse.db" -Force -ErrorAction SilentlyContinue
Remove-Item $logFile -Force -ErrorAction SilentlyContinue
Remove-Item $errFile -Force -ErrorAction SilentlyContinue
Write-Host "  Server stopped and temp files removed"

Write-Host ""
Write-Host "============================================"
Write-Host "  All tests passed!"
Write-Host "============================================"
Write-Host ""
Write-Host "The LangFuse server is ready for Session 12 Lab 09."
Write-Host ""
