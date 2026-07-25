#!/bin/bash
set -e

echo "============================================"
echo "  Agentic AI Course - Container Setup"
echo "============================================"
echo ""

# Delegate to the same setup script used by Linux/macOS participants
# This keeps container setup in sync with native setup automatically.
# --skip-ollama: Codespaces has no GPU and limited disk; Days 2-5 use Groq instead.
bash scripts/setup.sh --skip-ollama

# Inject Codespaces secrets into .env so scripts/notebooks can load them via dotenv.
# LAB_SUBMIT_TOKEN: fine-grained PAT with Issues read/write (set as repo Codespaces secret)
# GROQ_API_KEY: Groq free-tier key (set as user or repo Codespaces secret)
ENV_FILE="$(pwd)/.env"
if [ -f "$ENV_FILE" ]; then
  if [ -n "$LAB_SUBMIT_TOKEN" ]; then
    sed -i "s|^GITHUB_TOKEN=.*|GITHUB_TOKEN=$LAB_SUBMIT_TOKEN|" "$ENV_FILE"
    echo "  ✓ LAB_SUBMIT_TOKEN injected into .env as GITHUB_TOKEN"
  fi
  if [ -n "$GROQ_API_KEY" ] && [ "$GROQ_API_KEY" != "gsk_your_key_here" ]; then
    sed -i "s|^GROQ_API_KEY=.*|GROQ_API_KEY=$GROQ_API_KEY|" "$ENV_FILE"
    echo "  ✓ GROQ_API_KEY injected into .env"
  fi
fi

echo ""
echo "============================================"
echo "  Verifying the environment (all 5 days)"
echo "============================================"
bash scripts/setup.sh --verify

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
