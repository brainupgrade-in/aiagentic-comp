#!/bin/bash
# initial-setup.sh — One-time environment setup for Linux/macOS participants
# Run this ONCE at the start of the course to set up Python, venv, and all packages.
#
# Usage (from repo root):
#   bash scripts/initial-setup.sh
#
set -e

echo "============================================"
echo "  Agentic AI Course — Initial Setup"
echo "  (Linux/macOS)"
echo "============================================"
echo ""

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Step 1: Check Python installation
echo "[1/4] Checking Python installation..."
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version)
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MINOR" -ge 10 ]; then
        echo "  $PY_VER (OK)"
    else
        echo "  $PY_VER (too old — need 3.10+)"
        echo "  Install Python 3.12+: sudo apt install python3.12 python3.12-venv"
        exit 1
    fi
else
    echo "  Python 3 not found!"
    echo "  Install: sudo apt install python3 python3-venv python3-pip"
    exit 1
fi
echo ""

# Step 2: Create virtual environment
echo "[2/4] Creating virtual environment..."
if [ -f "$REPO_DIR/.venv/bin/python" ]; then
    echo "  Virtual environment already exists at $REPO_DIR/.venv"
else
    echo "  Creating .venv in $REPO_DIR ..."
    python3 -m venv "$REPO_DIR/.venv"
    echo "  Virtual environment created"
fi

source "$REPO_DIR/.venv/bin/activate"
echo "  Activated: $(python --version)"
echo ""

# Step 3: Install requirements
echo "[3/4] Installing Python packages (this may take a few minutes)..."
if [ -f "$REPO_DIR/requirements.txt" ]; then
    pip install --upgrade pip --quiet
    pip install -r "$REPO_DIR/requirements.txt"
    echo ""
    echo "  Packages installed successfully"
else
    echo "  WARNING: requirements.txt not found at $REPO_DIR/requirements.txt"
    echo "  Install packages manually: pip install langchain langchain-groq langgraph chromadb fastapi uvicorn"
fi
echo ""

# Step 4: Set up .env file
echo "[4/4] Setting up environment file..."
if [ -f "$REPO_DIR/.env" ]; then
    echo "  .env file already exists"
elif [ -f "$REPO_DIR/.env.example" ]; then
    cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"
    echo "  Created .env from .env.example"
    echo "  IMPORTANT: Edit .env and add your GROQ_API_KEY!"
else
    echo "  WARNING: .env.example not found"
fi
echo ""

# Check optional tools
echo "--- Optional: GitHub CLI ---"
if command -v gh &>/dev/null; then
    echo "  $(gh --version | head -1) (OK)"
else
    echo "  GitHub CLI (gh) not installed — needed for lab submission"
    echo "  Install: sudo apt install gh  OR  https://cli.github.com/"
fi
echo ""

echo "--- Optional: VS Code ---"
if command -v code &>/dev/null; then
    echo "  VS Code $(code --version | head -1) (OK)"
else
    echo "  VS Code not found"
    echo "  Download: https://code.visualstudio.com/"
fi
echo ""

# Summary
echo "============================================"
echo "  Initial setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your Groq API key:"
echo "     GROQ_API_KEY=gsk_your_key_here"
echo "     (Get one free at https://console.groq.com)"
echo ""
echo "  2. Set up Jupyter notebooks:"
echo "     bash scripts/install-notebook.sh"
echo ""
echo "  3. Run Day 1 setup:"
echo "     bash scripts/day1-setup.sh"
echo ""
echo "  4. Open the first lab in VS Code:"
echo "     code hands-on/session-1/lab01_meet_your_llm.ipynb"
echo ""
echo "Activate the virtual environment in any new terminal with:"
echo "  source $REPO_DIR/.venv/bin/activate"
echo ""
