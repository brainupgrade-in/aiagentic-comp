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

# Python processes
echo "--- Python Processes ---"
PROCS=$(pgrep -fa 'python\|uvicorn' 2>/dev/null)
if [ -n "$PROCS" ]; then
  echo "  Running processes:"
  echo "$PROCS" | while read line; do echo "    - $line"; done
else
  echo "  No running Python/uvicorn processes"
fi
echo ""

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
