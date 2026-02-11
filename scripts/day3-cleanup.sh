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
echo "[1/3] Stopping any running servers..."
pkill -f "uvicorn" 2>/dev/null || true
pkill -f "fastapi" 2>/dev/null || true

# Stop ChromaDB container if running
echo "[2/3] Stopping ChromaDB container..."
docker stop chromadb 2>/dev/null || true
docker rm chromadb 2>/dev/null || true

# Clean temp files and Python cache
echo "[3/3] Cleaning temp files..."
find ~/workspace/day3 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find /tmp -type d -name "k8s-lab-*" -exec rm -rf {} + 2>/dev/null || true

# Light Docker prune
docker container prune -f 2>/dev/null || true

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 3 cleanup complete. Ready for Day 4 (Docker + Kubernetes)."
echo ""
