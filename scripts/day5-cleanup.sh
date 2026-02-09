#!/bin/bash
set -e

echo "============================================"
echo "  Day 5: Observability Stack Cleanup"
echo "============================================"
echo ""

COMPOSE_DIR=~/workspace/day5/observability

if [ -f "$COMPOSE_DIR/docker-compose.yml" ]; then
  echo "Stopping observability stack..."
  cd "$COMPOSE_DIR"
  docker compose down -v
fi

echo ""
echo "Pruning unused Docker resources..."
docker system prune -f
docker volume prune -f

echo ""
echo "Cleanup complete."
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
