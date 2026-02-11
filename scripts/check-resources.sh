#!/bin/bash

echo "============================================"
echo "  Resource Monitor"
echo "============================================"
echo ""

# Memory
echo "--- Memory ---"
free -h | awk '
  /Mem:/ {printf "  Total: %s | Used: %s | Available: %s\n", $2, $3, $7}
  /Swap:/ {printf "  Swap:  %s total | %s used\n", $2, $3}
'
echo ""

# Storage
echo "--- Storage ---"
df -h / | tail -1 | awk '{printf "  Total: %s | Used: %s (%s) | Available: %s\n", $2, $3, $5, $4}'
echo ""

# Docker
if command -v docker &>/dev/null; then
  echo "--- Docker ---"
  CONTAINERS=$(docker ps --format '{{.Names}} ({{.Status}})' 2>/dev/null)
  if [ -n "$CONTAINERS" ]; then
    echo "  Running containers:"
    echo "$CONTAINERS" | while read line; do echo "    - $line"; done
  else
    echo "  No running containers"
  fi
  DOCKER_DISK=$(docker system df --format 'table {{.Type}}\t{{.Size}}' 2>/dev/null)
  echo "  Disk usage:"
  echo "$DOCKER_DISK" | while read line; do echo "    $line"; done
  echo ""
fi

# Ollama
if command -v ollama &>/dev/null; then
  echo "--- Ollama ---"
  echo "  Installed models:"
  ollama list 2>/dev/null | while read line; do echo "    $line"; done
  echo ""
fi

# Top processes by memory
echo "--- Top 5 Processes (by memory) ---"
ps aux --sort=-%mem | head -6 | awk 'NR==1{printf "  %-10s %s\n","MEM%","COMMAND"} NR>1{printf "  %-10s %s\n",$4,$11}'
echo ""
