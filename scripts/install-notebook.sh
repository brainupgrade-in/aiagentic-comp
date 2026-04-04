#!/bin/bash
# install-notebook.sh — Set up Jupyter notebooks for VS Code
# Installs the Jupyter extension, registers the .venv kernel, and
# embeds the kernel spec into every .ipynb so VS Code auto-selects it.
#
# Usage (from repo root):
#   bash scripts/install-notebook.sh
#
set -e

KERNEL_NAME="gheware-agentic-ai"
KERNEL_DISPLAY="Python 3 (Gheware Agentic AI)"

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$REPO_DIR/.venv/bin/python"

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

# Step 2: Register kernel from .venv
echo "[2/3] Registering kernel '$KERNEL_NAME'..."
if [ ! -f "$VENV_PYTHON" ]; then
    echo "  ERROR: .venv not found at $REPO_DIR/.venv"
    echo "  Run first: bash scripts/initial-setup.sh"
    exit 1
fi

"$VENV_PYTHON" -m pip install --quiet ipykernel
"$VENV_PYTHON" -m ipykernel install --user \
    --name "$KERNEL_NAME" \
    --display-name "$KERNEL_DISPLAY"
echo "  Kernel '$KERNEL_NAME' registered"
echo ""

# Step 3: Embed kernel spec into all notebooks
echo "[3/3] Configuring all notebooks to auto-select kernel..."

"$VENV_PYTHON" - <<PYEOF
import json, sys
from pathlib import Path

kernel_name    = "$KERNEL_NAME"
kernel_display = "$KERNEL_DISPLAY"
repo_root      = Path("$REPO_DIR")
hands_on_dir   = repo_root / "hands-on"

notebooks = [nb for nb in hands_on_dir.rglob("*.ipynb") if "README" not in nb.name]
if not notebooks:
    print("  No notebooks found!")
    sys.exit(1)

print(f"  Found {len(notebooks)} notebooks")
ok = fail = 0
for nb_path in sorted(notebooks):
    try:
        nb = json.loads(nb_path.read_text(encoding="utf-8"))
        nb.setdefault("metadata", {})
        nb["metadata"]["kernelspec"] = {
            "display_name": kernel_display,
            "language": "python",
            "name": kernel_name,
        }
        nb["metadata"].setdefault("language_info", {})["name"] = "python"
        nb_path.write_text(json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"  ✓ {nb_path.relative_to(repo_root)}")
        ok += 1
    except Exception as e:
        print(f"  ✗ {nb_path.relative_to(repo_root)}: {e}")
        fail += 1

print(f"\n  Updated: {ok}  Failed: {fail}  Total: {len(notebooks)}")
if fail:
    sys.exit(1)
PYEOF

echo ""
echo "============================================"
echo "  Notebook setup complete!"
echo "============================================"
echo ""
echo "Every .ipynb is now pre-configured for kernel: $KERNEL_DISPLAY"
echo "VS Code will auto-select it when you open any lab."
echo ""
echo "Try it:"
echo "  code $REPO_DIR/hands-on/session-1/lab01_meet_your_llm.ipynb"
echo ""
