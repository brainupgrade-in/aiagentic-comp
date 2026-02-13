#!/bin/bash
set -e

echo "============================================"
echo "  Jupyter Notebook Setup for VS Code"
echo "============================================"
echo ""

# Step 1: Install VS Code Jupyter extension
echo "[1/3] Installing VS Code Jupyter extension..."
if command -v code &>/dev/null; then
  code --install-extension ms-toolsai.jupyter --force 2>/dev/null && \
    echo "  Jupyter extension installed" || \
    echo "  WARNING: Could not install extension (install manually: ms-toolsai.jupyter)"
else
  echo "  'code' CLI not found — install the extension manually in VS Code:"
  echo "    Extensions sidebar → search 'Jupyter' → Install"
fi
echo ""

# Step 2: Install ipykernel
echo "[2/3] Installing ipykernel..."
if [ -f /home/vscode/.venv/bin/python ]; then
  source /home/vscode/.venv/bin/activate
fi
pip install --quiet ipykernel 2>/dev/null || pip install ipykernel
python -m ipykernel install --user --name agentic-ai --display-name "Agentic AI (Python)" 2>/dev/null || true
echo "  ipykernel installed"
echo ""

# Step 3: Verify with antigravity
echo "[3/3] Verifying Python + notebook setup..."
python -c "
import sys
print(f'  Python:    {sys.version.split()[0]}')

import ipykernel
print(f'  ipykernel: {ipykernel.__version__}')

# antigravity — Python Easter egg!
# (In a script it just confirms the module exists; in a notebook it opens xkcd.com/353)
import antigravity
print(f'  antigravity: loaded (try \"import antigravity\" in a notebook!)')

print()
print('  All checks passed!')
"

echo ""
echo "============================================"
echo "  Notebook setup complete!"
echo "============================================"
echo ""
echo "How to use:"
echo "  1. Open any .ipynb file in VS Code"
echo "  2. Select kernel: 'Agentic AI (Python)' or '~/.venv/bin/python'"
echo "  3. Run cells with Shift+Enter"
echo ""
echo "Try it:"
echo "  Open hands-on/session-1/lab01_meet_your_llm.ipynb"
echo ""
echo "Fun first cell to try in a notebook:"
echo "  import antigravity"
echo ""
