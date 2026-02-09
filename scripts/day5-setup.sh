#!/bin/bash
set -e

echo "============================================"
echo "  Day 5: Observability Stack Setup"
echo "============================================"
echo ""

echo "Current resource usage:"
free -h | head -2
df -h / | tail -1 | awk '{print "Storage: "$3" used / "$2" total ("$5" used)"}'
echo ""

COMPOSE_DIR=~/workspace/day5/observability

# Ensure docker-compose file is in place
if [ ! -f "$COMPOSE_DIR/docker-compose.yml" ]; then
  echo "Copying docker-compose.yml to workspace..."
  cp scripts/day5-docker-compose.yml "$COMPOSE_DIR/docker-compose.yml"
  cp scripts/prometheus.yml "$COMPOSE_DIR/prometheus.yml"
fi

# Start the observability stack
echo "Starting observability stack..."
cd "$COMPOSE_DIR"
docker compose up -d

echo ""
echo "Waiting for services to be healthy..."
sleep 10

echo ""
echo "============================================"
echo "  Observability stack running!"
echo "============================================"
echo ""
echo "Services:"
echo "  Prometheus:  http://localhost:9090"
echo "  Grafana:     http://localhost:3000  (admin/admin)"
echo "  LangFuse:    http://localhost:8080"
echo ""
echo "Check status:  docker compose -f $COMPOSE_DIR/docker-compose.yml ps"
echo "View logs:     docker compose -f $COMPOSE_DIR/docker-compose.yml logs -f"
echo ""
echo "To stop:       bash scripts/day5-cleanup.sh"
echo ""
