#!/bin/bash
# set-notebook-kernels.sh — Force all notebooks to use the gheware-agentic-ai kernel
# Run from repo root: bash scripts/set-notebook-kernels.sh

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_PYTHON="$REPO_DIR/.venv/bin/python"
KERNEL_NAME="gheware-agentic-ai"
KERNEL_DISPLAY="Python 3 (Gheware Agentic AI)"

if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: venv not found at $REPO_DIR/.venv — run initial-setup.sh first"
    exit 1
fi

echo "Setting kernel to '$KERNEL_NAME' in all notebooks..."

"$VENV_PYTHON" - <<PYEOF
import json, sys
from pathlib import Path

kernel_name    = "$KERNEL_NAME"
kernel_display = "$KERNEL_DISPLAY"
repo_root      = Path("$REPO_DIR")
hands_on_dir   = repo_root / "hands-on"

notebooks = [nb for nb in hands_on_dir.rglob("*.ipynb") if "README" not in nb.name]
print(f"Found {len(notebooks)} notebooks")
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

print(f"\nUpdated: {ok}  Failed: {fail}  Total: {len(notebooks)}")
if fail:
    sys.exit(1)
PYEOF
