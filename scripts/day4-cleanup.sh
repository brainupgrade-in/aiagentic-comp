#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: AI Coding Agents & MCP Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Clean up lab temp files
echo "[1/2] Removing lab temp files..."
rm -rf /tmp/aidev-lab-10-* /tmp/aidev-lab-11-* /tmp/aidev-lab-12-*
echo "  Removed /tmp/aidev-lab-* directories"

# Kill any stale Python processes from labs
echo "[2/2] Stopping stale processes..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
pkill -f "mcp.*server" 2>/dev/null || true

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 4 cleanup complete. Ready for Day 5 observability labs."
echo ""
