# Session 12: LangFuse Setup Scripts

This directory contains setup scripts for Session 12 (LangFuse Observability) labs.

## Overview

Session 12 introduces LangFuse observability patterns using **mock mode** — all traces are logged to local JSON files instead of requiring a LangFuse server. This keeps resource usage low on the 2-core/8GB Codespace environment.

## Scripts

### Bash (Linux/macOS/Codespaces)

```bash
bash scripts/session12-langfuse-setup.sh
```

### PowerShell (Windows)

```powershell
powershell -ExecutionPolicy Bypass -File scripts/session12-langfuse-setup.ps1
```

## What the Scripts Do

1. **Verify Python environment** — Check for virtual environment or system Python 3.10+
2. **Verify LangFuse package** — Check if `langfuse>=2.50` is installed
3. **Create trace directory** — Set up `/tmp/langfuse-traces` (Linux/macOS) or `%TEMP%\langfuse-traces` (Windows)
4. **Check environment variables** — Verify `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` from `.env`
5. **Run verification test** — Create a mock trace and verify the setup works

## Mock Mode Architecture

```
LangChain App
    ↓
LangFuse SDK / CallbackHandler
    ↓
MockLangfuse (local JSON logging)
    ↓
JSON files (trace storage)
```

**Key benefits:**
- Same SDK patterns as production LangFuse
- No external server required (zero infrastructure overhead)
- All traces saved to local JSON files for inspection
- Easy to switch to production by changing `LANGFUSE_HOST`

## Environment Variables

Required in `.env` file (copy from `.env.example`):

```bash
# LangFuse (Day 4) — Mock mode for SDK pattern learning
LANGFUSE_SECRET_KEY=sk-lf-mock-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-mock-public-key
LANGFUSE_HOST=http://localhost:8000
```

**Note:** These are mock credentials. In production, you would use real LangFuse API keys.

## MockLangfuse Class

The setup script creates a reference implementation at `/tmp/langfuse-traces/test_mock_langfuse.py`:

```python
class MockLangfuse:
    def __init__(self, public_key, secret_key, host, output_dir="/tmp/langfuse-traces"):
        # Initialize mock client

    def trace(self, name, metadata=None):
        # Create a new trace

    def flush(self):
        # Write all traces to JSON file

    def get_traces(self):
        # Read traces from JSON file
```

## Viewing Traces

After running labs, view the captured traces:

### Linux/macOS/Codespaces
```bash
# Pretty print with jq
cat /tmp/langfuse-traces/traces.json | jq

# Or just view raw JSON
cat /tmp/langfuse-traces/traces.json
```

### Windows PowerShell
```powershell
# Pretty print
Get-Content $env:TEMP\langfuse-traces\traces.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Or view in default JSON viewer
Get-Content $env:TEMP\langfuse-traces\traces.json
```

## Trace Structure

Each trace contains:

```json
{
  "name": "trace-name",
  "timestamp": "2026-02-15T00:00:00.000000",
  "metadata": {
    "custom": "data"
  },
  "generations": [
    {
      "name": "generation-name",
      "model": "llama-3.3-70b-versatile",
      "input": "User prompt",
      "output": "LLM response"
    }
  ]
}
```

## Session 12 Labs

After running the setup script, proceed with these labs:

| Lab | Topic | Description |
|-----|-------|-------------|
| lab01 | LangFuse Fundamentals | Core concepts, architecture |
| lab02 | LangFuse Setup & Deployment | MockLangfuse implementation |
| lab03 | LangChain Integration | CallbackHandler usage |
| lab04 | Tracing Agents | Multi-step agent traces |
| lab05 | Feedback & Evaluation | User feedback capture |
| lab06 | Prompt Management | Prompt versioning |
| lab07 | Cost Analysis | Token usage tracking |
| lab08 | Challenge | Comprehensive integration |

## Troubleshooting

### langfuse not installed

```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install directly
pip install langfuse>=2.50
```

### Environment variables not set

```bash
# Copy example file
cp .env.example .env

# Edit .env and set the mock credentials
# LANGFUSE_SECRET_KEY=sk-lf-mock-secret-key
# LANGFUSE_PUBLIC_KEY=pk-lf-mock-public-key
# LANGFUSE_HOST=http://localhost:8000
```

### Spaces around `=` in .env

The scripts handle this automatically using Python-based parsing. If you manually source `.env`, remove spaces:

```bash
# ✗ Wrong
LANGFUSE_SECRET_KEY = "sk-lf-..."

# ✓ Correct
LANGFUSE_SECRET_KEY="sk-lf-..."
```

### Trace directory not writable

Linux/macOS:
```bash
sudo mkdir -p /tmp/langfuse-traces
sudo chmod 777 /tmp/langfuse-traces
```

Windows:
```powershell
New-Item -ItemType Directory -Path "$env:TEMP\langfuse-traces" -Force
```

## Re-running the Test

After setup, you can verify the mock LangFuse at any time:

```bash
# Linux/macOS/Codespaces
python /tmp/langfuse-traces/test_mock_langfuse.py

# Windows
python "$env:TEMP\langfuse-traces\test_mock_langfuse.py"
```

## Moving to Production

To use real LangFuse in production:

1. Sign up at https://langfuse.com or self-host
2. Get API keys (public + secret)
3. Update `.env`:
   ```bash
   LANGFUSE_SECRET_KEY=sk-lf-real-key-from-langfuse
   LANGFUSE_PUBLIC_KEY=pk-lf-real-key-from-langfuse
   LANGFUSE_HOST=https://cloud.langfuse.com  # or your self-hosted URL
   ```
4. No code changes needed — same SDK works with both mock and production!

## Resource Usage

- **Mock mode:** ~100 KB per 100 traces
- **Memory overhead:** Minimal (Python in-process only)
- **Storage:** Local JSON files in `/tmp` (auto-cleaned on system reboot)

This fits comfortably within the 2-core/8GB/32GB Codespace limits.

## Additional Resources

- [LangFuse Documentation](https://langfuse.com/docs)
- [LangFuse Python SDK](https://github.com/langfuse/langfuse-python)
- [LangChain Callbacks](https://python.langchain.com/docs/modules/callbacks/)
- [Course presentation](../presentation/session12-langfuse-observability.html)

---

**Course:** Agentic AI
**Instructor:** Rajesh Gheware
**Organization:** Gheware UniGPS Solutions LLP
