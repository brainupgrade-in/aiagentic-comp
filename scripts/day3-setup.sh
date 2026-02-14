#!/bin/bash
set -e

echo "============================================"
echo "  Day 3: LangGraph & Multi-Agent Setup"
echo "============================================"
echo ""

# Check available resources
echo "Current resource usage:"
free -h | head -2
echo ""

# Check Python venv (relative to repo root)
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "[1/3] Verifying Python environment..."
if [ -f "$REPO_DIR/.venv/bin/python" ]; then
  source "$REPO_DIR/.venv/bin/activate"
  echo "  Virtual environment active: $(python --version)"
else
  echo "  ERROR: Virtual environment not found. Run: python -m venv $REPO_DIR/.venv"
  exit 1
fi

# Verify LangGraph and production packages
echo "[2/3] Verifying packages..."
python -c "import langgraph; print(f'  langgraph {langgraph.__version__}')" 2>/dev/null || echo "  WARNING: langgraph not installed"
python -c "import langchain_groq; print(f'  langchain-groq {langchain_groq.__version__}')" 2>/dev/null || echo "  WARNING: langchain-groq not installed"

# Check Groq API key
echo "[3/3] Checking Groq API key..."
if [ -f "$REPO_DIR/.env" ]; then
  source "$REPO_DIR/.env" 2>/dev/null || true
fi

if [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "gsk_your_key_here" ]; then
  echo "  GROQ_API_KEY is set"
else
  echo "  WARNING: GROQ_API_KEY not configured"
  echo "  Add to .env in the repo root: GROQ_API_KEY=gsk_your_key_here"
fi

echo ""
echo "============================================"
echo "  Day 3 ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 7: LangGraph Stateful Workflows"
echo "  Session 8: Advanced LangGraph Workflows"
echo "  Session 9: Multi-Agent Systems"
echo ""
echo "Labs: hands-on/session-7/ through session-9/"
echo ""
echo "IMPORTANT: Run 'bash scripts/day3-cleanup.sh' at end of day"
echo "to free resources for Day 4 (observability stack)."
echo ""
