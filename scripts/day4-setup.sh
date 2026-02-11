#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: AI Coding Agents & MCP Setup"
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
echo "  Day 4 Ready!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 10: AI Coding Agents & Vibe Coding"
echo "  Session 11: Model Context Protocol (MCP)"
echo "  Session 12: Building Custom AI Dev Tools"
echo ""
echo "Labs:"
echo "  python hands-on/session-10/lab01_coding_agent_anatomy.py"
echo "  python hands-on/session-11/lab01_mcp_fundamentals.py"
echo "  python hands-on/session-12/lab01_code_quality_server.py"
echo ""
echo "Resource usage: ~3-4 GB RAM (Python + MCP SDK only)"
echo ""
