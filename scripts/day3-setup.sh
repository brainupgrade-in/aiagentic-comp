#!/bin/bash
set -e

echo "============================================"
echo "  Day 3: Production Development Setup"
echo "============================================"
echo ""

# Check available resources
echo "Current resource usage:"
free -h | head -2
echo ""

# Check Python venv
echo "[1/3] Verifying Python environment..."
if [ -f /home/vscode/.venv/bin/python ]; then
  source /home/vscode/.venv/bin/activate
  echo "  Virtual environment active: $(python --version)"
else
  echo "  ERROR: Virtual environment not found. Run: python -m venv /home/vscode/.venv"
  exit 1
fi

# Verify FastAPI and production packages
echo "[2/3] Verifying production packages..."
python -c "import fastapi; print(f'  fastapi {fastapi.__version__}')" 2>/dev/null || echo "  WARNING: fastapi not installed"
python -c "import uvicorn; print(f'  uvicorn {uvicorn.__version__}')" 2>/dev/null || echo "  WARNING: uvicorn not installed"
python -c "import pydantic; print(f'  pydantic {pydantic.__version__}')" 2>/dev/null || echo "  WARNING: pydantic not installed"
python -c "import httpx; print(f'  httpx {httpx.__version__}')" 2>/dev/null || echo "  WARNING: httpx not installed"

# Check Groq API key
echo "[3/3] Checking Groq API key..."
if [ -f ~/workspace/.env ]; then
  source ~/workspace/.env 2>/dev/null || true
fi

if [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "gsk_your_key_here" ]; then
  echo "  GROQ_API_KEY is set"
else
  echo "  WARNING: GROQ_API_KEY not configured"
  echo "  Add to ~/workspace/.env: GROQ_API_KEY=gsk_your_key_here"
fi

# Pre-pull ChromaDB image for RAG exercises
echo ""
echo "Pre-pulling ChromaDB Docker image..."
docker pull chromadb/chroma:latest 2>/dev/null &
wait

echo ""
echo "============================================"
echo "  Day 3 ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 8:  Multi-Agent Systems"
echo "  Session 9:  Production Application Development"
echo ""
echo "Quick test (FastAPI):"
echo "  cd ~/workspace/day3"
echo "  uvicorn app:app --reload --port 8000"
echo ""
echo "Labs: hands-on/session-8/ and session-9/"
echo ""
echo "IMPORTANT: Run 'bash scripts/day3-cleanup.sh' at end of day"
echo "to free resources for Day 4 (Docker + Kubernetes)."
echo ""
