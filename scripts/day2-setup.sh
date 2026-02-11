#!/bin/bash
set -e

echo "============================================"
echo "  Day 2: LangChain + Groq API Setup"
echo "============================================"
echo ""

# Check available resources
echo "Current resource usage:"
free -h | head -2
echo ""

# Verify Day 1 cleanup was done
if command -v ollama &>/dev/null; then
  echo "WARNING: Ollama is still installed. Run 'bash scripts/day1-cleanup.sh' first"
  echo "to free ~2 GB of resources."
  echo ""
fi

# Check Python venv
echo "[1/3] Verifying Python environment..."
if [ -f /home/vscode/.venv/bin/python ]; then
  source /home/vscode/.venv/bin/activate
  echo "  Virtual environment active: $(python --version)"
else
  echo "  ERROR: Virtual environment not found. Run: python -m venv /home/vscode/.venv"
  exit 1
fi

# Verify key packages
echo "[2/3] Verifying LangChain packages..."
python -c "import langchain; print(f'  langchain {langchain.__version__}')" 2>/dev/null || echo "  WARNING: langchain not installed"
python -c "import langchain_groq; print(f'  langchain-groq {langchain_groq.__version__}')" 2>/dev/null || echo "  WARNING: langchain-groq not installed"
python -c "import langchain_chroma; print(f'  langchain-chroma {langchain_chroma.__version__}')" 2>/dev/null || echo "  WARNING: langchain-chroma not installed"
python -c "import langgraph; print(f'  langgraph {langgraph.__version__}')" 2>/dev/null || echo "  WARNING: langgraph not installed"

# Check Groq API key
echo "[3/3] Checking Groq API key..."
if [ -f ~/workspace/.env ]; then
  source ~/workspace/.env 2>/dev/null || true
fi

if [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "gsk_your_key_here" ]; then
  echo "  GROQ_API_KEY is set"
else
  echo "  WARNING: GROQ_API_KEY not configured"
  echo "  1. Sign up at https://console.groq.com (free)"
  echo "  2. Create an API key"
  echo "  3. Add to ~/workspace/.env:"
  echo "     GROQ_API_KEY=gsk_your_key_here"
fi

echo ""
echo "============================================"
echo "  Day 2 ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 5: LangChain Agents & Memory"
echo "  Session 6: LangGraph Stateful Workflows"
echo "  Session 7: Advanced LangGraph Workflows"
echo ""
echo "Quick test (Python):"
echo "  from langchain_groq import ChatGroq"
echo "  llm = ChatGroq(model='llama-3.1-8b-instant')"
echo "  print(llm.invoke('Hello from Day 2!'))"
echo ""
echo "Labs: hands-on/session-5/ through session-7/"
echo ""
