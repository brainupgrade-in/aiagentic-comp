#!/bin/bash
set -e

echo "============================================"
echo "  Day 5: MCP, Safety & Capstone Setup"
echo "============================================"
echo ""

echo "Current resource usage:"
free -h | head -2
df -h / | tail -1 | awk '{print "Storage: "$3" used / "$2" total ("$5" used)"}'
echo ""

# Verify Python
echo "[1/3] Verifying Python..."
python3 --version || { echo "ERROR: Python 3 not found"; exit 1; }

# Verify pip and install MCP SDK
echo "[2/3] Installing MCP Python SDK..."
pip install --quiet mcp>=1.0 2>/dev/null || pip install mcp>=1.0

# Verify GROQ_API_KEY
echo "[3/3] Checking GROQ_API_KEY..."
if [ -z "$GROQ_API_KEY" ]; then
    if [ -f .env ]; then
        source .env
    fi
    if [ -z "$GROQ_API_KEY" ]; then
        echo ""
        echo "WARNING: GROQ_API_KEY not set."
        echo "  Set it in .env or export GROQ_API_KEY=gsk_..."
        echo "  Get your free key at: https://console.groq.com"
        echo ""
    else
        echo "  GROQ_API_KEY found in .env"
    fi
else
    echo "  GROQ_API_KEY is set"
fi

echo ""
echo "============================================"
echo "  Day 5 Ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 13: Model Context Protocol (MCP)"
echo "  Session 14: AI Safety & Guardrails"
echo "  Session 15: Capstone Project (2 time slots)"
echo ""
echo "Labs (open in VS Code or JupyterLab):"
echo "  hands-on/session-13/lab01_mcp_fundamentals.ipynb"
echo "  hands-on/session-14/lab01_prompt_injection_detection.ipynb"
echo "  hands-on/session-15/lab01_capstone_architecture.ipynb"
echo ""
echo "Resource usage: ~3-4 GB RAM (Python + MCP SDK only)"
echo "Day 5 is lightweight — no observability stack needed."
echo ""
