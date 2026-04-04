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
echo "  Container ready!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add your Groq API key to .env"
echo "     Get one free at https://console.groq.com"
echo "  2. Run Day 1 setup:"
echo "     bash scripts/day1-setup.sh"
echo ""
echo "Forwarded ports:"
echo "  8000 — FastAPI App"
echo "  3000 — LangFuse Server (Day 4)"
echo "  11434 — Ollama (Day 1)"
echo ""
