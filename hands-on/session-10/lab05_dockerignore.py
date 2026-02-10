"""
Lab 05: .dockerignore and Build Context
==========================================
Optimize Docker builds by controlling what gets sent to the daemon.

No Docker installation required — generates and validates .dockerignore files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-05"

print("=" * 50)
print("  Lab 05: .dockerignore and Build Context")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: What is the Build Context?
# ============================================================

print("\n--- Step 1: What is the Build Context? ---\n")

print("  When you run: docker build -t myapp:1.0 .")
print("                                              ^")
print("                                              |")
print("                              This '.' is the build context")
print()
print("  Docker sends ALL files in this directory to the daemon.")
print("  If you have .git/, .venv/, data files → they ALL get sent!")

# Simulate a project directory
project_files = {
    "main.py":              2,       # 2 KB
    "config.py":            1,
    "requirements.txt":     1,
    "Dockerfile":           1,
    "README.md":            5,
    ".env":                 1,       # Secrets!
    ".env.production":      1,       # More secrets!
    ".git/objects/pack":    50_000,  # 50 MB git history
    ".git/HEAD":            1,
    ".venv/lib/python3.11": 200_000, # 200 MB virtual env
    "__pycache__/main.cpython-311.pyc": 10,
    "__pycache__/config.cpython-311.pyc": 8,
    "tests/test_main.py":  3,
    "tests/test_config.py": 2,
    "docs/api.md":          10,
    "docs/setup.md":        5,
    "data/vectors.db":      500_000, # 500 MB vector database
    "models/model.bin":     800_000, # 800 MB model file
    ".mypy_cache/3.11":     5_000,
    ".pytest_cache/v":      500,
    "docker-compose.yml":   2,
}

total_kb = sum(project_files.values())
total_mb = total_kb / 1024

print(f"\n  Project files ({len(project_files)} items):")
print(f"  {'File':<45} {'Size':>10}")
print("  " + "-" * 58)
for path, size_kb in sorted(project_files.items(), key=lambda x: -x[1]):
    if size_kb >= 1024:
        size_str = f"{size_kb/1024:.0f} MB"
    else:
        size_str = f"{size_kb} KB"
    print(f"  {path:<45} {size_str:>10}")
print("  " + "-" * 58)
print(f"  {'TOTAL':<45} {total_mb:>8.0f} MB")

print(f"\n  Without .dockerignore: Docker sends ALL {total_mb:.0f} MB to the daemon!")
print(f"  Most of it is unnecessary for the build.")


# ============================================================
# Step 2: Create a .dockerignore
# ============================================================

print("\n\n--- Step 2: Create a .dockerignore ---\n")

dockerignore = textwrap.dedent('''\
    # Version control
    .git
    .gitignore

    # Python
    __pycache__
    *.pyc
    *.pyo
    .venv/
    venv/
    *.egg-info

    # Environment files (SECRETS!)
    .env
    .env.*

    # IDE and tools
    .mypy_cache
    .pytest_cache
    .vscode/
    .idea/

    # Documentation (not needed at runtime)
    docs/
    README.md
    *.md

    # Docker files (don't need inside the image)
    Dockerfile
    Dockerfile.*
    docker-compose.yml
    docker-compose.*.yml
    .dockerignore

    # Large data files
    data/
    models/

    # Tests (not needed in production image)
    tests/
''')

with open(os.path.join(WORKDIR, ".dockerignore"), "w") as f:
    f.write(dockerignore)

# Calculate what gets excluded
excluded_patterns = [
    ".git", "__pycache__", ".venv", ".env", ".mypy_cache",
    ".pytest_cache", "docs/", "README.md", "Dockerfile",
    "docker-compose", ".dockerignore", "data/", "models/", "tests/",
]

included_files = {}
excluded_files = {}
for path, size in project_files.items():
    is_excluded = any(
        path.startswith(pat.rstrip("/")) or
        path.endswith(pat.lstrip("*")) or
        pat.rstrip("/") in path
        for pat in excluded_patterns
    )
    if is_excluded:
        excluded_files[path] = size
    else:
        included_files[path] = size

included_mb = sum(included_files.values()) / 1024
excluded_mb = sum(excluded_files.values()) / 1024

print("  With .dockerignore:")
print(f"\n  INCLUDED (sent to Docker daemon): {included_mb:.1f} MB")
for path, size in sorted(included_files.items()):
    print(f"    + {path}")

print(f"\n  EXCLUDED (not sent): {excluded_mb:.0f} MB")
for path, size in sorted(excluded_files.items()):
    print(f"    - {path}")

print(f"\n  Build context reduced: {total_mb:.0f} MB → {included_mb:.1f} MB")
print(f"  That's {(1 - included_mb/total_mb)*100:.0f}% smaller!")


# ============================================================
# Step 3: Security — What MUST Be Excluded
# ============================================================

print("\n\n--- Step 3: Security-Critical Exclusions ---\n")

dangerous_files = [
    (".env",              "API keys, database passwords, secrets"),
    (".env.production",   "Production secrets"),
    (".git/",             "Full commit history, potentially leaked secrets"),
    ("*.pem",             "SSL/TLS certificates and private keys"),
    ("credentials.json",  "Cloud provider credentials"),
    (".ssh/",             "SSH private keys"),
]

print("  ALWAYS exclude these (security risk if baked into image):")
print()
for pattern, reason in dangerous_files:
    print(f"    {pattern:<25} — {reason}")

print("\n  Why?")
print("    - Docker images can be pulled by anyone with registry access")
print("    - Image layers can be inspected (docker history, dive)")
print("    - Even if you delete a file in a later layer, it's still")
print("      in the earlier layer and can be extracted!")


# ============================================================
# TODO 1: Fix the .dockerignore for an AI project
# ============================================================

print("\n\n--- TODO 1: Fix the .dockerignore ---\n")

# This .dockerignore is incomplete. Add the missing patterns.
# The project has: Python code, .env files, Jupyter notebooks,
# model weights, vector databases, and test data.

incomplete_dockerignore = textwrap.dedent('''\
    # TODO: This is incomplete! Add missing patterns.

    # Python
    __pycache__
    *.pyc

    # Version control
    .git
''')

# TODO: Add patterns for:
# 1. Virtual environments (.venv/, venv/)
# 2. Environment files (.env, .env.*)
# 3. Jupyter notebooks and checkpoints (.ipynb_checkpoints/)
# 4. Large model files (models/, *.bin, *.onnx)
# 5. Test data (test_data/, tests/)
# 6. IDE files (.vscode/, .idea/)

fixed_dockerignore = incomplete_dockerignore  # Replace with your fix

# Uncomment:
# fixed_dockerignore = textwrap.dedent('''\
#     # Python
#     __pycache__
#     *.pyc
#     *.pyo
#     .venv/
#     venv/
#     *.egg-info
#
#     # Version control
#     .git
#     .gitignore
#
#     # Environment files (SECRETS)
#     .env
#     .env.*
#
#     # Jupyter
#     .ipynb_checkpoints/
#     *.ipynb
#
#     # Large model files
#     models/
#     *.bin
#     *.onnx
#     *.pt
#
#     # Test data
#     test_data/
#     tests/
#
#     # IDE
#     .vscode/
#     .idea/
#
#     # Tools
#     .mypy_cache
#     .pytest_cache
#
#     # Docker
#     Dockerfile
#     Dockerfile.*
#     docker-compose*.yml
#     .dockerignore
#
#     # Docs
#     docs/
#     *.md
# ''')

# Validate
must_have = [".env", ".venv", ".git", "__pycache__", "*.pyc"]
nice_to_have = ["models/", "tests/", ".vscode/", "Dockerfile", "*.md"]

print("  Required patterns:")
for pattern in must_have:
    found = pattern in fixed_dockerignore
    print(f"    [{'PASS' if found else 'TODO'}] {pattern}")

print("\n  Recommended patterns:")
for pattern in nice_to_have:
    found = pattern in fixed_dockerignore
    print(f"    [{'PASS' if found else 'TODO'}] {pattern}")


# ============================================================
# TODO 2: Calculate build context savings
# ============================================================

print("\n\n--- TODO 2: Calculate Build Context Savings ---\n")

# TODO: Write a function that takes a list of project files
# and a .dockerignore content, and calculates the build context size.

# def calculate_context_size(files: dict, dockerignore: str) -> dict:
#     """Calculate included vs excluded file sizes.
#
#     Args:
#         files: dict of {path: size_kb}
#         dockerignore: content of .dockerignore file
#
#     Returns:
#         dict with included_kb, excluded_kb, reduction_percent
#     """
#     # TODO: Parse dockerignore patterns and match against files
#     # Hint: For each pattern, check if the file path starts with
#     # the pattern (for directories) or matches the extension (for globs)
#     pass

# Uncomment:
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
                # Extension pattern
                ext = pat[1:]  # e.g., ".pyc"
                if path.endswith(ext):
                    is_excluded = True
                    break
            elif path.startswith(clean) or f"/{clean}" in f"/{path}":
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


# Test the function
test_files = {
    "main.py": 5,
    "requirements.txt": 1,
    ".git/objects": 50_000,
    ".venv/lib": 200_000,
    "__pycache__/main.pyc": 10,
    ".env": 1,
    "models/bert.bin": 400_000,
}

result = calculate_context_size(test_files, dockerignore)
if result:
    print(f"  Test project:")
    print(f"    Included: {result['included_kb']/1024:.1f} MB")
    print(f"    Excluded: {result['excluded_kb']/1024:.0f} MB")
    print(f"    Reduction: {result['reduction_percent']}%")
else:
    print("  TODO: Implement calculate_context_size function")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 05 Summary ---\n")
print("  .dockerignore best practices:")
print("    1. ALWAYS exclude .env files (secrets!)")
print("    2. Exclude .git/ (huge, contains full history)")
print("    3. Exclude .venv/ (hundreds of MBs, rebuilt in image)")
print("    4. Exclude large data/model files (use volumes instead)")
print("    5. Exclude tests and docs (not needed at runtime)")
print("    6. A good .dockerignore reduces context by 95%+")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
