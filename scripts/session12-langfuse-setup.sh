#!/bin/bash
set -e

echo "============================================"
echo "  Session 11: LangFuse Setup (Mock Mode)"
echo "============================================"
echo ""

# Get repo root directory
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Verify Python environment
echo "[1/5] Verifying Python environment..."
if [ -f "$REPO_DIR/.venv/bin/python" ]; then
  source "$REPO_DIR/.venv/bin/activate"
  echo "  ✓ Virtual environment active: $(python --version)"
else
  python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }
  echo "  ✓ System Python: $(python3 --version)"
fi

# Verify LangFuse package
echo ""
echo "[2/5] Verifying LangFuse package..."
if python -c "import langfuse; print(f'  ✓ langfuse {langfuse.__version__}')" 2>/dev/null; then
  :
else
  echo "  ✗ WARNING: langfuse not installed"
  echo ""
  echo "  To install: pip install langfuse>=2.50"
  echo "  Or run: pip install -r requirements.txt"
  echo ""
  echo "  Continuing setup (install langfuse before running labs)..."
fi

# Create mock LangFuse trace directory
echo ""
echo "[3/5] Creating mock LangFuse trace directory..."
TRACE_DIR="/tmp/langfuse-traces"
if [ -d "$TRACE_DIR" ]; then
  echo "  ℹ Directory already exists: $TRACE_DIR"
  TRACE_COUNT=$(find "$TRACE_DIR" -name "*.json" 2>/dev/null | wc -l)
  if [ "$TRACE_COUNT" -gt 0 ]; then
    echo "  ℹ Found $TRACE_COUNT existing trace file(s)"
  fi
else
  mkdir -p "$TRACE_DIR"
  echo "  ✓ Created: $TRACE_DIR"
fi

# Verify environment variables
echo ""
echo "[4/5] Checking LangFuse environment variables..."
MISSING_VARS=()

# Try to load from .env using Python (more robust than bash parsing)
if [ -f "$REPO_DIR/.env" ]; then
  eval "$(python -c "
import os
import re

env_file = '$REPO_DIR/.env'
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # Match KEY = VALUE or KEY=VALUE, handle quotes
            match = re.match(r'^([A-Z_]+)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                # Remove quotes if present
                value = value.strip('\"').strip(\"'\")
                # Export as bash variable
                print(f'export {key}=\"{value}\"')
")"
fi

# Check LANGFUSE_PUBLIC_KEY
if [ -z "$LANGFUSE_PUBLIC_KEY" ]; then
  MISSING_VARS+=("LANGFUSE_PUBLIC_KEY")
  echo "  ✗ LANGFUSE_PUBLIC_KEY not set"
else
  echo "  ✓ LANGFUSE_PUBLIC_KEY is set"
fi

# Check LANGFUSE_SECRET_KEY
if [ -z "$LANGFUSE_SECRET_KEY" ]; then
  MISSING_VARS+=("LANGFUSE_SECRET_KEY")
  echo "  ✗ LANGFUSE_SECRET_KEY not set"
else
  echo "  ✓ LANGFUSE_SECRET_KEY is set"
fi

# Check LANGFUSE_HOST
if [ -z "$LANGFUSE_HOST" ]; then
  MISSING_VARS+=("LANGFUSE_HOST")
  echo "  ✗ LANGFUSE_HOST not set"
else
  echo "  ✓ LANGFUSE_HOST is set: $LANGFUSE_HOST"
fi

# Warn if variables missing
if [ ${#MISSING_VARS[@]} -gt 0 ]; then
  echo ""
  echo "  WARNING: Missing environment variables:"
  for var in "${MISSING_VARS[@]}"; do
    echo "    - $var"
  done
  echo ""
  echo "  For mock mode, add these to .env:"
  echo "    LANGFUSE_PUBLIC_KEY=pk-lf-mock-public-key"
  echo "    LANGFUSE_SECRET_KEY=sk-lf-mock-secret-key"
  echo "    LANGFUSE_HOST=http://localhost:8000"
  echo ""
  echo "  Copy from .env.example:"
  echo "    cp .env.example .env"
  echo ""
fi

# Create test script to verify mock setup
echo ""
echo "[5/5] Creating mock LangFuse test..."
TEST_SCRIPT="$TRACE_DIR/test_mock_langfuse.py"
cat > "$TEST_SCRIPT" << 'EOF'
#!/usr/bin/env python3
"""Test script for MockLangfuse setup."""
import json
import os
from datetime import datetime

class MockLangfuse:
    """Mock LangFuse client that logs traces to local JSON files."""

    def __init__(self, public_key, secret_key, host, output_dir="/tmp/langfuse-traces"):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host
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
EOF

# Run the test
python "$TEST_SCRIPT"

echo ""
echo "============================================"
echo "  Session 11 LangFuse Setup Complete!"
echo "============================================"
echo ""
echo "Configuration:"
echo "  • Mock mode enabled (local JSON logging)"
echo "  • Trace directory: $TRACE_DIR"
echo "  • Test script: $TEST_SCRIPT"
echo ""
echo "Next steps:"
echo "  1. Open hands-on/session-11/ labs in VS Code or JupyterLab"
echo "  2. Labs use MockLangfuse class for local trace logging"
echo "  3. View traces: cat $TRACE_DIR/traces.json | jq"
echo ""
echo "Key labs:"
echo "  • lab01: LangFuse fundamentals"
echo "  • lab02: LangFuse setup & deployment"
echo "  • lab03: LangChain integration"
echo "  • lab04: Tracing agents"
echo "  • lab05: Feedback & evaluation"
echo ""
echo "To re-run test: python $TEST_SCRIPT"
echo ""
