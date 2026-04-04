#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: Observability & Production Setup"
echo "============================================"
echo ""

echo "Current resource usage:"
free -h | head -2
df -h / | tail -1 | awk '{print "Storage: "$3" used / "$2" total ("$5" used)"}'
echo ""

# Verify Python (relative to repo root)
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "[1/4] Verifying Python environment..."
if [ -f "$REPO_DIR/.venv/bin/python" ]; then
  source "$REPO_DIR/.venv/bin/activate"
  echo "  Virtual environment active: $(python --version)"
else
  python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }
fi

# Verify FastAPI and production packages
echo "[2/4] Verifying production packages..."
python -c "import fastapi; print(f'  fastapi {fastapi.__version__}')" 2>/dev/null || echo "  WARNING: fastapi not installed"
python -c "import uvicorn; print(f'  uvicorn {uvicorn.__version__}')" 2>/dev/null || echo "  WARNING: uvicorn not installed"
python -c "import pydantic; print(f'  pydantic {pydantic.__version__}')" 2>/dev/null || echo "  WARNING: pydantic not installed"
python -c "import psutil; print(f'  psutil {psutil.__version__}')" 2>/dev/null || echo "  WARNING: psutil not installed"
python -c "import langfuse; print(f'  langfuse {langfuse.__version__}')" 2>/dev/null || echo "  WARNING: langfuse not installed"
python -c "import opentelemetry; print(f'  opentelemetry-api installed')" 2>/dev/null || echo "  WARNING: opentelemetry not installed"

# Verify GROQ_API_KEY
echo "[3/4] Checking GROQ_API_KEY..."
if [ -z "$GROQ_API_KEY" ]; then
    if [ -f "$REPO_DIR/.env" ]; then
        source "$REPO_DIR/.env"
    fi
    if [ -z "$GROQ_API_KEY" ]; then
        echo ""
        echo "WARNING: GROQ_API_KEY not set."
        echo "  Set it in .env or export GROQ_API_KEY=gsk_..."
        echo "  Get your free key at: https://console.groq.com"
        echo ""
    else
        echo "  GROQ_API_KEY found in .env"
    fi
else
    echo "  GROQ_API_KEY is set"
fi

# Start LangFuse server for Session 12 Lab 09
echo ""
echo "[4/4] Starting LangFuse server for Session 12 Lab 09..."

# Check if LangFuse server is already running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  WARNING: Port 3000 already in use. LangFuse server may already be running."
    echo "  To stop it: bash scripts/day4-cleanup.sh"
else
    # Start LangFuse server in background
    if [ -f "$REPO_DIR/.venv/bin/python" ]; then
        nohup "$REPO_DIR/.venv/bin/python" "$REPO_DIR/scripts/langfuse-server.py" > /tmp/langfuse-server.log 2>&1 &
        LANGFUSE_PID=$!
        echo $LANGFUSE_PID > /tmp/langfuse-server.pid

        # Wait for server to start
        sleep 3

        # Check if server started successfully
        if curl -s http://localhost:3000/api/public/health > /dev/null 2>&1; then
            echo "  ✓ LangFuse server started on http://localhost:3000"
            echo "  ✓ PID: $LANGFUSE_PID (saved to /tmp/langfuse-server.pid)"
            echo "  ✓ Logs: /tmp/langfuse-server.log"
            echo "  ✓ Database: /tmp/langfuse.db"
        else
            echo "  ERROR: LangFuse server failed to start. Check /tmp/langfuse-server.log"
        fi
    else
        echo "  ERROR: Virtual environment not found. Cannot start LangFuse server."
        exit 1
    fi
fi

echo ""
echo "============================================"
echo "  Day 4 Ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 10: Observability Fundamentals"
echo "  Session 11: Production Development & Deployment"
echo "  Session 12: LangFuse Observability"
echo ""
echo "Session flow: Learn observability theory → Build production app → Instrument it"
echo ""
echo "Infrastructure:"
echo "  ✓ LangFuse server running on http://localhost:3000 (for Lab 09)"
echo "  ✓ Database: /tmp/langfuse.db (SQLite)"
echo "  ✓ Logs: /tmp/langfuse-server.log"
echo ""
echo "Labs (open in VS Code or JupyterLab):"
echo "  Session 10: hands-on/session-10/lab01_three_pillars.ipynb (8 labs)"
echo "  Session 11: hands-on/session-11/lab01_fastapi_basics.ipynb (8 labs)"
echo "  Session 12: hands-on/session-12/lab01_langfuse_fundamentals.ipynb (9 labs)"
echo ""
echo "Lab pattern:"
echo "  - Labs 01-08: Use MockLangfuse (local JSON files)"
echo "  - Lab 09: Use real LangFuse server (http://localhost:3000)"
echo ""
echo "Capstone:"
echo "  Session 12 Lab 09: Production-grade FastAPI + LangGraph + LangFuse"
echo "  - Full trace collection with SQLite backend"
echo "  - Cost tracking per request"
echo "  - User feedback via scores API"
echo "  - Health probes with observability metrics"
echo ""
echo "Resource usage: ~2-4 GB RAM (Python + SQLite)"
echo ""
echo "IMPORTANT: Run 'bash scripts/day4-cleanup.sh' at end of day"
echo ""
