#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: MicroK8s Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Remove MicroK8s
echo "[1/2] Removing MicroK8s..."
sudo microk8s stop 2>/dev/null || true
sudo snap remove microk8s --purge

# Clean up kubectl alias
echo "[2/2] Cleaning up..."
sed -i '/alias kubectl/d' ~/.bashrc 2>/dev/null || true

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "MicroK8s removed. Resources freed for Day 5 labs."
echo ""
