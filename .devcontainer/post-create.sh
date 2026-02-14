#!/bin/bash
set -e

echo "============================================"
echo "  Agentic AI Course - Environment Setup"
echo "============================================"

# Create and activate virtual environment in repo root
echo "[1/4] Creating Python virtual environment..."
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "[2/4] Installing Python packages..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Install OpenCode — AI coding agent for the terminal
echo "[3/4] Installing OpenCode (AI coding assistant)..."
curl -fsSL https://opencode.ai/install | bash

# Set up environment
echo "[4/4] Setting up environment..."

# Copy .env from template if it doesn't exist
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
  echo "  Copied .env.example → .env (add your API keys)"
fi

echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Add your Groq API key to .env: https://console.groq.com"
echo "  2. Run: source .venv/bin/activate"
echo "  3. Connect OpenCode to GitHub Copilot:"
echo "     opencode"
echo "     Then type /connect and select GitHub Copilot"
echo ""
echo "Day-specific scripts are in ./scripts/"
echo "  Day 1: bash scripts/day1-setup.sh"
echo "  Day 4: bash scripts/day4-setup.sh"
echo "  Day 5: bash scripts/day5-setup.sh"
echo ""
echo "AI Coding Assistant:"
echo "  opencode              # Launch OpenCode TUI"
echo "  opencode 'fix this'   # Non-interactive mode"
echo ""
