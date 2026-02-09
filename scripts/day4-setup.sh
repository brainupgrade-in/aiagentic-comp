#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: MicroK8s Setup"
echo "============================================"
echo ""

echo "Current resource usage:"
free -h | head -2
df -h / | tail -1 | awk '{print "Storage: "$3" used / "$2" total ("$5" used)"}'
echo ""

# Install MicroK8s
echo "[1/3] Installing MicroK8s..."
sudo snap install microk8s --classic --channel=1.31/stable

# Configure permissions
echo "[2/3] Configuring access..."
sudo usermod -a -G microk8s vscode
sudo chown -R vscode ~/.kube 2>/dev/null || true

# Wait for MicroK8s to be ready
echo "[3/3] Waiting for MicroK8s to start..."
sudo microk8s status --wait-ready --timeout 120

# Enable essential addons
sudo microk8s enable dns
sudo microk8s enable hostpath-storage

# Create kubectl alias
echo 'alias kubectl="sudo microk8s kubectl"' >> ~/.bashrc
source ~/.bashrc

echo ""
echo "============================================"
echo "  MicroK8s ready!"
echo "============================================"
echo ""
echo "Quick test:"
echo "  sudo microk8s kubectl get nodes"
echo "  sudo microk8s kubectl get pods -A"
echo ""
echo "Deploy your app:"
echo "  sudo microk8s kubectl apply -f deployment.yaml"
echo ""
echo "IMPORTANT: Run 'bash scripts/day4-cleanup.sh' after the K8s demo"
echo "to free resources for Day 5 observability labs."
echo ""
