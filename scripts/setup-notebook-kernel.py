#!/usr/bin/env python3
"""
Setup Jupyter notebook kernel for all labs.
Registers the .venv as a Jupyter kernel and updates all notebooks to use it.
"""
import json
import subprocess
import sys
from pathlib import Path

def register_kernel():
    """Register the virtual environment as a Jupyter kernel."""
    print("Registering virtual environment as Jupyter kernel...")

    # Check if we're in a virtual environment
    venv_python = Path(__file__).parent.parent / ".venv" / "bin" / "python"
    if not venv_python.exists():
        print(f"ERROR: Virtual environment not found at {venv_python}")
        print("Please create it first with: python3 -m venv .venv")
        sys.exit(1)

    # Register the kernel
    try:
        subprocess.run([
            str(venv_python),
            "-m",
            "ipykernel",
            "install",
            "--user",
            "--name=gheware-agentic-ai",
            "--display-name=Python 3 (Gheware Agentic AI)"
        ], check=True)
        print("✓ Kernel registered successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to register kernel: {e}")
        return False
    except FileNotFoundError:
        print("ERROR: ipykernel not installed. Installing...")
        subprocess.run([str(venv_python), "-m", "pip", "install", "ipykernel"], check=True)
        return register_kernel()

def update_notebook_kernel(notebook_path):
    """Update a single notebook to use the registered kernel."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Update kernelspec
        if 'metadata' not in notebook:
            notebook['metadata'] = {}

        notebook['metadata']['kernelspec'] = {
            "display_name": "Python 3 (Gheware Agentic AI)",
            "language": "python",
            "name": "gheware-agentic-ai"
        }

        # Update language_info if present
        if 'language_info' in notebook['metadata']:
            notebook['metadata']['language_info']['name'] = 'python'

        # Write back
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline

        return True
    except Exception as e:
        print(f"ERROR updating {notebook_path}: {e}")
        return False

def main():
    """Main function to setup all notebooks."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    hands_on_dir = project_root / "hands-on"

    # Register the kernel
    if not register_kernel():
        print("\nFailed to register kernel. Exiting.")
        sys.exit(1)

    # Find all notebooks
    notebooks = list(hands_on_dir.rglob("*.ipynb"))
    print(f"\nFound {len(notebooks)} notebooks")

    # Update each notebook
    updated = 0
    failed = 0

    for nb_path in sorted(notebooks):
        relative_path = nb_path.relative_to(project_root)
        if update_notebook_kernel(nb_path):
            print(f"✓ {relative_path}")
            updated += 1
        else:
            print(f"✗ {relative_path}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total notebooks: {len(notebooks)}")
    print(f"  Updated: {updated}")
    print(f"  Failed: {failed}")
    print(f"{'='*60}")

    if failed > 0:
        sys.exit(1)

    print("\n✓ All notebooks configured to use: Python 3 (Gheware Agentic AI)")
    print("  Kernel location: .venv/bin/python")

if __name__ == "__main__":
    main()
