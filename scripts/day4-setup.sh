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

# Verify Python
echo "[1/4] Verifying Python environment..."
if [ -f /home/vscode/.venv/bin/python ]; then
  source /home/vscode/.venv/bin/activate
  echo "  Virtual environment active: $(python --version)"
else
  python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }
fi

# Verify FastAPI and production packages
echo "[2/4] Verifying production packages..."
python -c "import fastapi; print(f'  fastapi {fastapi.__version__}')" 2>/dev/null || echo "  WARNING: fastapi not installed"
python -c "import uvicorn; print(f'  uvicorn {uvicorn.__version__}')" 2>/dev/null || echo "  WARNING: uvicorn not installed"
python -c "import pydantic; print(f'  pydantic {pydantic.__version__}')" 2>/dev/null || echo "  WARNING: pydantic not installed"

# Verify GROQ_API_KEY
echo "[3/4] Checking GROQ_API_KEY..."
if [ -z "$GROQ_API_KEY" ]; then
    if [ -f .env ]; then
        source .env
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

# Start observability stack
COMPOSE_DIR=~/workspace/day4/observability

echo "[4/4] Starting observability stack..."
mkdir -p "$COMPOSE_DIR"

if [ ! -f "$COMPOSE_DIR/docker-compose.yml" ]; then
  cp scripts/day5-docker-compose.yml "$COMPOSE_DIR/docker-compose.yml"
  cp scripts/prometheus.yml "$COMPOSE_DIR/prometheus.yml"
fi

cd "$COMPOSE_DIR"
docker compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

echo ""
echo "============================================"
echo "  Day 4 Ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 10: Observability Fundamentals"
echo "  Session 11: LangFuse Observability"
echo "  Session 12: Production Development & Deployment"
echo ""
echo "Services:"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3000  (admin/admin)"
echo "  LangFuse:    http://localhost:8080"
echo ""
echo "Labs:"
echo "  python hands-on/session-10/lab01_three_pillars.py"
echo "  python hands-on/session-11/lab01_langfuse_fundamentals.py"
echo "  python hands-on/session-12/lab01_fastapi_basics.py"
echo ""
echo "Resource usage: ~5-7 GB RAM (Docker Compose + Python)"
echo ""
echo "IMPORTANT: Run 'bash scripts/day4-cleanup.sh' at end of day"
echo ""
