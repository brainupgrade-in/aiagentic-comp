#!/bin/bash
set -e

echo "============================================"
echo "  Agentic AI Course - Container Setup"
echo "============================================"
echo ""

# Delegate to the same setup script used by Linux/macOS participants
# This keeps container setup in sync with native setup automatically
bash scripts/initial-setup.sh

echo ""
echo "============================================"
echo "  Installing Jupyter Kernel"
echo "============================================"
bash scripts/install-jupyter-kernel.sh

echo ""
echo "============================================"
echo "  Day 3: LangGraph & Multi-Agent Verification"
echo "============================================"
bash scripts/day3-setup.sh

echo ""
echo "============================================"
echo "  Container ready!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Set GROQ_API_KEY in .env (or as a Codespaces secret)"
echo "     Get one free at https://console.groq.com"
echo "  2. Open a notebook in hands-on/session-7/"
echo "     Select kernel: gheware-agentic-ai"
echo ""
echo "Forwarded ports:"
echo "  8000 — FastAPI App"
echo "  3000 — LangFuse Server (Day 4)"
echo "  11434 — Ollama (Day 1)"
echo ""
