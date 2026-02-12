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

# Stop any running ChromaDB containers
echo "[1/2] Stopping any ChromaDB containers..."
docker stop chromadb 2>/dev/null || true
docker rm chromadb 2>/dev/null || true

# Clean Python cache and temp files
echo "[2/2] Cleaning temp files..."
find ~/workspace -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
rm -rf /tmp/k8s-lab-04-* /tmp/k8s-lab-05-* /tmp/k8s-lab-06-*

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 2 cleanup complete. Ready for Day 3."
echo ""
