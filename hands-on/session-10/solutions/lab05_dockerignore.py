"""
Lab 05 Solution: .dockerignore and Build Context
==================================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-05"

print("=" * 50)
print("  Lab 05 Solution: .dockerignore")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Complete .dockerignore
# ============================================================

print("\n--- TODO 1 Solution: Complete .dockerignore ---\n")

fixed_dockerignore = textwrap.dedent('''\
    # Python
    __pycache__
    *.pyc
    *.pyo
    .venv/
    venv/
    *.egg-info

    # Version control
    .git
    .gitignore

    # Environment files (SECRETS)
    .env
    .env.*

    # Jupyter
    .ipynb_checkpoints/
    *.ipynb

    # Large model files
    models/
    *.bin
    *.onnx
    *.pt

    # Test data
    test_data/
    tests/

    # IDE
    .vscode/
    .idea/

    # Tools
    .mypy_cache
    .pytest_cache

    # Docker
    Dockerfile
    Dockerfile.*
    docker-compose*.yml
    .dockerignore

    # Docs
    docs/
    *.md
''')

with open(os.path.join(WORKDIR, ".dockerignore"), "w") as f:
    f.write(fixed_dockerignore)

must_have = [".env", ".venv", ".git", "__pycache__", "*.pyc"]
nice_to_have = ["models/", "tests/", ".vscode/", "Dockerfile", "*.md"]

print("  Required patterns:")
for pattern in must_have:
    found = pattern in fixed_dockerignore
    print(f"    [{'PASS' if found else 'FAIL'}] {pattern}")

print("\n  Recommended patterns:")
for pattern in nice_to_have:
    found = pattern in fixed_dockerignore
    print(f"    [{'PASS' if found else 'FAIL'}] {pattern}")

print("\n  Additional patterns for AI projects:")
print("    *.ipynb              — Jupyter notebooks (not needed at runtime)")
print("    .ipynb_checkpoints/  — Jupyter auto-saves")
print("    *.bin, *.onnx, *.pt — Model weight files (use volumes)")
print("    test_data/           — Test fixtures and sample data")


# ============================================================
# TODO 2 Solution: Build context calculator
# ============================================================

print("\n\n--- TODO 2 Solution: Build Context Calculator ---\n")

def calculate_context_size(files: dict, dockerignore: str) -> dict:
    """Calculate build context size with .dockerignore applied."""
    patterns = []
    for line in dockerignore.strip().split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.append(line)

    included_kb = 0
    excluded_kb = 0

    for path, size_kb in files.items():
        is_excluded = False
        for pat in patterns:
            clean = pat.rstrip("/")
            if pat.startswith("*."):
                # Extension pattern: *.pyc, *.bin
                ext = pat[1:]
                if path.endswith(ext):
                    is_excluded = True
                    break
            elif path.startswith(clean) or f"/{clean}" in f"/{path}":
                # Directory/file pattern: .git, .env, models/
                is_excluded = True
                break

        if is_excluded:
            excluded_kb += size_kb
        else:
            included_kb += size_kb

    total = included_kb + excluded_kb
    return {
        "included_kb": included_kb,
        "excluded_kb": excluded_kb,
        "reduction_percent": round(excluded_kb / total * 100, 1) if total > 0 else 0,
    }


# Test with a realistic AI project
test_files = {
    "main.py": 5,
    "config.py": 2,
    "requirements.txt": 1,
    "Dockerfile": 1,
    "README.md": 5,
    ".env": 1,
    ".env.production": 1,
    ".git/objects/pack": 50_000,
    ".git/HEAD": 1,
    ".venv/lib/python3.11": 200_000,
    "__pycache__/main.cpython-311.pyc": 10,
    "__pycache__/config.cpython-311.pyc": 8,
    "tests/test_main.py": 3,
    "docs/api.md": 10,
    "data/vectors.db": 500_000,
    "models/model.bin": 800_000,
    ".mypy_cache/3.11": 5_000,
    ".pytest_cache/v": 500,
}

result = calculate_context_size(test_files, fixed_dockerignore)
print(f"  Realistic AI project ({len(test_files)} files):")
print(f"    Total:    {sum(test_files.values())/1024:.0f} MB")
print(f"    Included: {result['included_kb']/1024:.1f} MB (sent to Docker)")
print(f"    Excluded: {result['excluded_kb']/1024:.0f} MB (skipped)")
print(f"    Reduction: {result['reduction_percent']}%")

# Test with minimal .dockerignore
minimal_ignore = ".git\n__pycache__\n"
minimal_result = calculate_context_size(test_files, minimal_ignore)
print(f"\n  With minimal .dockerignore:")
print(f"    Included: {minimal_result['included_kb']/1024:.0f} MB")
print(f"    Reduction: {minimal_result['reduction_percent']}%")

print(f"\n  Complete .dockerignore saves {result['reduction_percent'] - minimal_result['reduction_percent']:.0f}% more!")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print("- TODO 1: Complete .dockerignore with AI-specific patterns")
print("- TODO 2: Build context calculator (pattern matching, size computation)")
