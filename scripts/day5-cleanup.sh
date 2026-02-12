#!/bin/bash
set -e

echo "============================================"
echo "  Day 5: Final Cleanup"
echo "============================================"
echo ""

# Clean up lab temp files
echo "[1/2] Removing lab temp files..."
rm -rf /tmp/aidev-lab-13-* /tmp/safety-lab-14-* /tmp/capstone-lab-15-*
echo "  Removed MCP, safety, and capstone temp directories"

# Kill any stale processes
echo "[2/2] Stopping stale processes..."
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "mcp.*server" 2>/dev/null || true

echo ""
echo "Cleanup complete."
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Course complete! Thank you for participating."
echo ""
