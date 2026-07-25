#!/usr/bin/env python3
"""Point every lab notebook at the course Jupyter kernel.

Rewrites the kernelspec metadata in all hands-on/**/*.ipynb (student labs and
solutions) so VS Code / JupyterLab auto-select the right kernel on open.

Called by scripts/setup.sh. Run it standalone if a notebook loses its kernel:
    .venv/bin/python scripts/configure-notebooks.py
"""

import json
import sys
from pathlib import Path

KERNEL_NAME = "gheware-agentic-ai"
KERNEL_DISPLAY = "Python 3 (Gheware Agentic AI)"

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDS_ON = REPO_ROOT / "hands-on"


def main():
    notebooks = sorted(nb for nb in HANDS_ON.rglob("*.ipynb") if "README" not in nb.name)
    if not notebooks:
        print(f"  No notebooks found under {HANDS_ON}")
        return 1

    kernelspec = {
        "display_name": KERNEL_DISPLAY,
        "language": "python",
        "name": KERNEL_NAME,
    }

    print(f"  Found {len(notebooks)} notebooks")
    updated = already = fail = 0
    for nb_path in notebooks:
        try:
            nb = json.loads(nb_path.read_text(encoding="utf-8"))
            metadata = nb.setdefault("metadata", {})

            # Skip untouched so we don't reformat notebooks that are already correct
            if (
                metadata.get("kernelspec") == kernelspec
                and metadata.get("language_info", {}).get("name") == "python"
            ):
                already += 1
                continue

            metadata["kernelspec"] = kernelspec
            metadata.setdefault("language_info", {})["name"] = "python"
            nb_path.write_text(
                json.dumps(nb, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            updated += 1
        except Exception as exc:
            print(f"  [FAIL] {nb_path.relative_to(REPO_ROOT)}: {exc}")
            fail += 1

    print(
        f"  [OK]   kernel '{KERNEL_DISPLAY}': "
        f"{updated} updated, {already} already correct"
        + (f", {fail} failed" if fail else "")
    )
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
