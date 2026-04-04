#!/bin/bash
# initial-setup.sh — One-time environment setup for Linux/macOS participants
# Sets up Python venv, installs all packages, registers the Jupyter kernel,
# and configures every notebook to auto-select it.
#
# Usage (from repo root):
#   source scripts/initial-setup.sh   ← activates venv in current shell (recommended)
#   bash scripts/initial-setup.sh     ← runs setup only (activate manually after)
#
# Use return when sourced, exit when run directly
_exit_or_return() { local code=${1:-1}; [[ "${BASH_SOURCE[0]}" != "${0}" ]] && return "$code" || exit "$code"; }

set -e

KERNEL_NAME="gheware-agentic-ai"
KERNEL_DISPLAY="Python 3 (Gheware Agentic AI)"

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$REPO_DIR/.venv/bin/python"

echo "============================================"
echo "  Agentic AI Course — Initial Setup"
echo "  (Linux/macOS)"
echo "============================================"
echo ""

# Step 1: Check Python installation
echo "[1/6] Checking Python installation..."
if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version)
    PY_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    if [ "$PY_MINOR" -ge 10 ]; then
        echo "  $PY_VER (OK)"
    else
        echo "  $PY_VER (too old — need 3.10+)"
        echo "  Install Python 3.12+: sudo apt install python3.12 python3.12-venv"
        _exit_or_return 1
    fi
else
    echo "  Python 3 not found!"
    echo "  Install: sudo apt install python3 python3-venv python3-pip"
    _exit_or_return 1
fi
echo ""

# Step 2: Create virtual environment
echo "[2/6] Creating virtual environment..."
if [ -f "$VENV_PYTHON" ]; then
    echo "  Virtual environment already exists at $REPO_DIR/.venv"
else
    echo "  Creating .venv in $REPO_DIR ..."
    python3 -m venv "$REPO_DIR/.venv"
    echo "  Virtual environment created"
fi
source "$REPO_DIR/.venv/bin/activate"
echo "  Activated: $(python --version)"
echo ""

# Step 3: Install requirements
echo "[3/6] Installing Python packages (this may take a few minutes)..."
if [ -f "$REPO_DIR/requirements.txt" ]; then
    pip install --upgrade pip --quiet
    # Install CPU-only PyTorch first to avoid downloading multi-GB NVIDIA/CUDA packages
    pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet
    pip install -r "$REPO_DIR/requirements.txt"
    echo ""
    echo "  Packages installed successfully"
else
    echo "  WARNING: requirements.txt not found at $REPO_DIR/requirements.txt"
    echo "  Install packages manually: pip install langchain langchain-groq langgraph chromadb fastapi uvicorn"
fi
echo ""

# Step 4: Set up .env file
echo "[4/6] Setting up environment file..."
if [ -f "$REPO_DIR/.env" ]; then
    echo "  .env file already exists"
elif [ -f "$REPO_DIR/.env.example" ]; then
    cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"
    echo "  Created .env from .env.example"
    echo "  IMPORTANT: Edit .env and add your GROQ_API_KEY!"
else
    echo "  WARNING: .env.example not found"
fi
echo ""

# Step 5: Register Jupyter kernel from .venv
echo "[5/6] Registering Jupyter kernel '$KERNEL_NAME'..."
if command -v code &>/dev/null; then
    code --install-extension ms-toolsai.jupyter --force 2>/dev/null && \
        echo "  VS Code Jupyter extension installed" || \
        echo "  WARNING: Could not install Jupyter extension (install manually: ms-toolsai.jupyter)"
else
    echo "  'code' CLI not found — install the Jupyter extension manually in VS Code"
fi
"$VENV_PYTHON" -m pip install --quiet ipykernel
"$VENV_PYTHON" -m ipykernel install --user \
    --name "$KERNEL_NAME" \
    --display-name "$KERNEL_DISPLAY"
echo "  Kernel '$KERNEL_NAME' registered"
echo ""

# Step 6: Embed kernel spec into all notebooks
echo "[6/6] Configuring all notebooks to auto-select kernel..."
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

# Check optional tools
echo "--- Optional: GitHub CLI ---"
if command -v gh &>/dev/null; then
    echo "  $(gh --version | head -1) (OK)"
else
    echo "  GitHub CLI (gh) not installed — needed for lab submission"
    echo "  Install: sudo apt install gh  OR  https://cli.github.com/"
fi
echo ""

# Summary
echo "============================================"
echo "  Initial setup complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env and add your Groq API key:"
echo "     GROQ_API_KEY=gsk_your_key_here"
echo "     (Get one free at https://console.groq.com)"
echo ""
echo "  2. Run Day 1 setup:"
echo "     bash scripts/day1-setup.sh"
echo ""
echo "  3. Open the first lab — kernel auto-selects:"
echo "     code hands-on/session-1/lab01_meet_your_llm.ipynb"
echo ""

# Activate venv in the current shell if the script was sourced
if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
    source "$REPO_DIR/.venv/bin/activate"
    echo "  Virtual environment activated in this shell: $(python --version)"
else
    echo "To activate the virtual environment in this terminal, run:"
    echo "  source $REPO_DIR/.venv/bin/activate"
fi
echo ""
