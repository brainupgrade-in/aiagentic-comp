#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: Observability & Production Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Clean up lab temp files
echo "[1/2] Removing lab temp files..."
rm -rf /tmp/k8s-lab-10-* /tmp/k8s-lab-11-* /tmp/prod-lab-12-*
echo "  Removed temp directories"

# Stop stale processes
echo "[2/2] Stopping stale processes..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
pkill -f "fastapi" 2>/dev/null || true

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 4 cleanup complete. Ready for Day 5 (MCP + Capstone)."
echo ""
