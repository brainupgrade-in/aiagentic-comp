#!/bin/bash
set -e

echo "============================================"
echo "  Day 2: Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Clean Python cache and temp files
echo "[1/1] Cleaning temp files..."
REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
find "$REPO_DIR" -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
rm -rf /tmp/ailab-04-* /tmp/ailab-05-* /tmp/ailab-06-*

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 2 cleanup complete. Ready for Day 3."
echo ""
