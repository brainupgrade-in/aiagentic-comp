#!/bin/bash
set -e

echo "============================================"
echo "  Day 3: Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Stop any running app servers
echo "[1/2] Stopping any running servers..."
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "fastapi" 2>/dev/null || true

# Clean temp files and Python cache
echo "[2/2] Cleaning temp files..."
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
find "$REPO_DIR" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
rm -rf /tmp/k8s-lab-07-* /tmp/k8s-lab-08-* /tmp/k8s-lab-09-*

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 3 cleanup complete. Ready for Day 4 (observability)."
echo ""
