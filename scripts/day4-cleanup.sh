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

# Stop observability stack
COMPOSE_DIR=~/workspace/day4/observability
if [ -f "$COMPOSE_DIR/docker-compose.yml" ]; then
  echo "[1/3] Stopping observability stack..."
  cd "$COMPOSE_DIR"
  docker compose down -v
fi

# Clean up lab temp files
echo "[2/3] Removing lab temp files..."
rm -rf /tmp/k8s-lab-10-* /tmp/k8s-lab-11-* /tmp/prod-lab-12-*
echo "  Removed temp directories"

# Stop stale processes and prune Docker
echo "[3/3] Stopping stale processes and pruning Docker..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
docker system prune -f 2>/dev/null || true
docker volume prune -f 2>/dev/null || true

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 4 cleanup complete. Ready for Day 5 (MCP + Capstone)."
echo ""
