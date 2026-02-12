#!/bin/bash
set -e

echo "============================================"
echo "  Agentic AI Course - Environment Setup"
echo "============================================"

# Create and activate virtual environment
echo "[1/4] Creating Python virtual environment..."
python -m venv /home/vscode/.venv
source /home/vscode/.venv/bin/activate

# Install Python dependencies
echo "[2/4] Installing Python packages..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Install OpenCode — AI coding agent for the terminal
echo "[3/4] Installing OpenCode (AI coding assistant)..."
curl -fsSL https://opencode.ai/install | bash

# Create working directories
echo "[4/4] Setting up workspace..."
mkdir -p ~/workspace/{day1,day2,day3,day4,day5}

# Create .env template
cat > ~/workspace/.env.template << 'EOF'
# Groq API (https://console.groq.com - create free account)
GROQ_API_KEY=gsk_your_key_here

# LangFuse (mock mode — SDK patterns logged to local JSON files)
LANGFUSE_SECRET_KEY=sk-lf-mock-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-mock-public-key
LANGFUSE_HOST=http://localhost:8000
EOF

echo ""
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Copy .env template:  cp ~/workspace/.env.template ~/workspace/.env"
echo "  2. Add your Groq API key: https://console.groq.com"
echo "  3. Run: source /home/vscode/.venv/bin/activate"
echo "  4. Connect OpenCode to GitHub Copilot:"
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
