#!/bin/bash
set -e

echo "============================================"
echo "  Day 1: Cleanup (freeing ~2 GB)"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Stop Ollama
echo "[1/4] Stopping Ollama..."
pkill ollama 2>/dev/null || true
sleep 1

# Remove model
echo "[2/4] Removing llama3.2:1b model..."
ollama rm llama3.2:1b 2>/dev/null || true

# Uninstall Ollama
echo "[3/4] Uninstalling Ollama..."
sudo rm -f /usr/local/bin/ollama
sudo rm -rf /usr/share/ollama
rm -rf ~/.ollama

# Clean temp files from Day 1 labs
echo "[4/4] Cleaning lab temp files..."
rm -rf /tmp/aidev-lab-02-* /tmp/k8s-lab-03-*

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Done! From Day 2 onwards, use Groq API (free, cloud-hosted)."
echo ""
