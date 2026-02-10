#!/bin/bash
set -e

echo "============================================"
echo "  Agentic AI Course - Environment Setup"
echo "============================================"

# Create and activate virtual environment
echo "[1/5] Creating Python virtual environment..."
python -m venv /home/vscode/.venv
source /home/vscode/.venv/bin/activate

# Install Python dependencies
echo "[2/5] Installing Python packages..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Install OpenCode — AI coding agent for the terminal
echo "[3/5] Installing OpenCode (AI coding assistant)..."
curl -fsSL https://opencode.ai/install | bash

# Pre-pull Docker images (lightweight ones only, others pulled on-demand)
echo "[4/5] Pre-pulling Docker images..."
docker pull chromadb/chroma:latest &
docker pull prom/prometheus:latest &
docker pull grafana/grafana:latest &
wait

# Create working directories
echo "[5/5] Setting up workspace..."
mkdir -p ~/workspace/{day1,day2,day3,day4,day5}
mkdir -p ~/workspace/day5/observability

# Create .env template
cat > ~/workspace/.env.template << 'EOF'
# Groq API (https://console.groq.com - create free account)
GROQ_API_KEY=gsk_your_key_here

# LangFuse (populated by Day 5 setup script)
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
LANGFUSE_HOST=http://localhost:8080
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
