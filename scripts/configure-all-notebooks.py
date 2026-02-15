#!/usr/bin/env python3
"""
Configure Jupyter notebook kernels for ALL notebooks (student labs + solutions).
Updates the kernelspec metadata to use the Python kernel from .venv/bin/python
"""

import json
import sys
from pathlib import Path

def update_notebook_kernel(notebook_path):
    """Update a single notebook's kernel configuration."""
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        # Update kernelspec metadata
        if 'metadata' not in notebook:
            notebook['metadata'] = {}

        notebook['metadata']['kernelspec'] = {
            "display_name": "Python 3 (Gheware Agentic AI)",
            "language": "python",
            "name": "gheware-agentic-ai"
        }

        # Ensure language_info is set
        if 'language_info' not in notebook['metadata']:
            notebook['metadata']['language_info'] = {}

        notebook['metadata']['language_info']['name'] = 'python'

        # Write back
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
            f.write('\n')  # Add trailing newline

        return True, None
    except Exception as e:
        return False, str(e)

def main():
    # Find project root (where this script is located)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    hands_on_dir = project_root / 'hands-on'

    if not hands_on_dir.exists():
        print(f"Error: hands-on directory not found at {hands_on_dir}")
        sys.exit(1)

    # Find all notebooks (student labs + solutions, but exclude README notebooks)
    all_notebooks = [
        nb for nb in hands_on_dir.glob('**/*.ipynb')
        if 'README' not in nb.name
    ]

    if not all_notebooks:
        print("No notebooks found!")
        sys.exit(1)

    print(f"Found {len(all_notebooks)} notebooks")
    print("Updating kernel configuration...\n")

    success_count = 0
    failed_count = 0

    for notebook_path in sorted(all_notebooks):
        relative_path = notebook_path.relative_to(project_root)
        success, error = update_notebook_kernel(notebook_path)

        if success:
            print(f"✓ {relative_path}")
            success_count += 1
        else:
            print(f"✗ {relative_path}: {error}")
            failed_count += 1

    print(f"\n{'='*60}")
    print(f"Successfully updated: {success_count}")
    print(f"Failed: {failed_count}")
    print(f"Total: {len(all_notebooks)}")

    if failed_count > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()
