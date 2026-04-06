#!/bin/bash
# install-opencode.sh — Install opencode AI coding assistant
#
# Usage (from repo root):
#   bash scripts/install-opencode.sh
#
# What it does:
#   1. Installs opencode via official installer
#   2. Verifies the installation
#   3. Prints auth and usage instructions

set -e

echo "============================================"
echo "  OpenCode: AI Coding Assistant Setup"
echo "============================================"
echo ""

# ── Step 1: Install opencode ──────────────────────────────────────────────────
echo "[1/2] Installing opencode..."

if command -v opencode &>/dev/null; then
  echo "  opencode already installed: $(opencode --version 2>&1 || echo 'version unknown')"
else
  curl -fsSL https://opencode.ai/install | bash
  # Reload PATH so 'opencode' is available in this session
  export PATH="$HOME/.local/bin:$PATH"
  if ! command -v opencode &>/dev/null; then
    echo ""
    echo "  opencode installed but not yet on PATH."
    echo "  Open a new terminal or run:"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "  Then re-run this script to verify."
    exit 0
  fi
  echo "  opencode installed: $(opencode --version 2>&1 || echo 'ok')"
fi
echo ""

# ── Step 2: Verify ────────────────────────────────────────────────────────────
echo "[2/2] Verifying installation..."
OPENCODE_PATH=$(command -v opencode)
echo "  Binary: $OPENCODE_PATH"
echo ""

echo "============================================"
echo "  OpenCode ready!"
echo "============================================"
echo ""
echo "Authentication (choose one):"
echo "  Option A — GitHub Copilot (free tier available):"
echo "    opencode        # launch TUI, then type /connect"
echo ""
echo "  Option B — Groq API (free, no login needed):"
echo "    export GROQ_API_KEY=gsk_your_key_here"
echo "    # or add GROQ_API_KEY to .env in the repo root"
echo ""
echo "Usage:"
echo "  opencode                     # interactive TUI"
echo "  opencode 'explain this code' # single prompt"
echo ""
echo "TUI tips:"
echo "  Tab          — switch between build / plan agents"
echo "  /connect     — authenticate with a provider"
echo "  /help        — show all commands"
echo ""
