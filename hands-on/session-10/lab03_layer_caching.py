"""
Lab 03: Layer Caching Optimization
====================================
Understand Docker layer caching and optimize build times.

No Docker installation required — simulates caching behavior.
"""

import os
import shutil
import textwrap
import time
import hashlib

WORKDIR = "/tmp/docker-lab-03"

print("=" * 50)
print("  Lab 03: Layer Caching Optimization")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: How Layer Caching Works
# ============================================================

print("\n--- Step 1: How Layer Caching Works ---\n")

class DockerBuildSimulator:
    """Simulates Docker's layer caching behavior."""

    def __init__(self):
        self.cache = {}  # hash → layer result
        self.build_log = []

    def build_layer(self, instruction, file_hash=None):
        """Simulate building a single layer."""
        # Docker uses instruction + context hash to determine cache hit
        cache_key = f"{instruction}:{file_hash or 'none'}"

        if cache_key in self.cache:
            self.build_log.append(f"  CACHED  {instruction}")
            return 0.01  # Cache hit: instant

        # Cache miss: simulate build time
        if "pip install" in instruction:
            build_time = 3.0  # pip install takes ~3s
        elif "apt-get" in instruction:
            build_time = 2.0
        elif instruction.startswith("COPY"):
            build_time = 0.1
        else:
            build_time = 0.05

        self.cache[cache_key] = True
        self.build_log.append(f"  BUILD   {instruction} ({build_time:.1f}s)")
        return build_time

    def build(self, instructions, file_hashes):
        """Build all layers. Returns total time."""
        self.build_log = []
        total = 0
        cache_valid = True

        for instr, fhash in zip(instructions, file_hashes):
            if not cache_valid:
                # Once cache is busted, all subsequent layers must rebuild
                cache_key = f"{instr}:{fhash or 'none'}"
                if cache_key in self.cache:
                    # Even if this layer was cached, it must rebuild
                    # because a previous layer changed
                    del self.cache[cache_key]

            t = self.build_layer(instr, fhash)
            if t > 0.01:
                cache_valid = False  # This layer wasn't cached → bust all after
            total += t

        return total


sim = DockerBuildSimulator()

# Simulate: First build (nothing cached)
instructions = [
    "FROM python:3.11-slim",
    "COPY . .",
    "RUN pip install -r requirements.txt",
    "CMD uvicorn main:app",
]
hashes = ["base-v1", "code-v1", "req-v1", "cmd-v1"]

print("  Build 1: First build (nothing cached)")
t1 = sim.build(instructions, hashes)
for line in sim.build_log:
    print(f"  {line}")
print(f"  Total: {t1:.1f}s\n")

# Simulate: Code change → everything rebuilds!
print("  Build 2: Code change (main.py modified)")
hashes_v2 = ["base-v1", "code-v2", "req-v1", "cmd-v1"]  # code changed!
t2 = sim.build(instructions, hashes_v2)
for line in sim.build_log:
    print(f"  {line}")
print(f"  Total: {t2:.1f}s")
print(f"\n  Problem: pip install runs again even though requirements didn't change!")

# ============================================================
# Step 2: Bad vs Good Layer Ordering
# ============================================================

print("\n\n--- Step 2: Bad vs Good Layer Ordering ---\n")

# BAD: Copy everything first
bad_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN pip install --no-cache-dir -r requirements.txt
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# GOOD: Copy requirements first
good_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# Simulate rebuilds after code change
print("  BAD Ordering: COPY . . → pip install")
bad_sim = DockerBuildSimulator()
bad_instructions = ["FROM", "WORKDIR", "COPY . .", "RUN pip install", "ENV", "EXPOSE", "CMD"]
bad_hashes = ["base", "workdir", "all-files-v1", "pip-v1", "env", "expose", "cmd"]

# First build
bad_sim.build(bad_instructions, bad_hashes)
# Code change → rebuild
bad_hashes_v2 = ["base", "workdir", "all-files-v2", "pip-v1", "env", "expose", "cmd"]
t_bad = bad_sim.build(bad_instructions, bad_hashes_v2)
for line in bad_sim.build_log:
    print(f"  {line}")
print(f"  Rebuild time: {t_bad:.1f}s (pip reinstalls every time!)\n")

print("  GOOD Ordering: COPY requirements.txt → pip install → COPY . .")
good_sim = DockerBuildSimulator()
good_instructions = ["FROM", "WORKDIR", "COPY req.txt", "RUN pip install", "COPY . .", "ENV", "EXPOSE", "CMD"]
good_hashes = ["base", "workdir", "req-v1", "pip-v1", "code-v1", "env", "expose", "cmd"]

# First build
good_sim.build(good_instructions, good_hashes)
# Code change → only code layer rebuilds
good_hashes_v2 = ["base", "workdir", "req-v1", "pip-v1", "code-v2", "env", "expose", "cmd"]
t_good = good_sim.build(good_instructions, good_hashes_v2)
for line in good_sim.build_log:
    print(f"  {line}")
print(f"  Rebuild time: {t_good:.1f}s (pip cached!)")
print(f"\n  Speedup: {t_bad / t_good:.0f}x faster with proper layer ordering!")

# Write both Dockerfiles
with open(os.path.join(WORKDIR, "Dockerfile.bad"), "w") as f:
    f.write(bad_dockerfile)
with open(os.path.join(WORKDIR, "Dockerfile.good"), "w") as f:
    f.write(good_dockerfile)

# ============================================================
# Step 3: Caching Rules
# ============================================================

print("\n\n--- Step 3: Docker Caching Rules ---\n")

rules = [
    ("Rule 1", "Each instruction creates a layer",
     "FROM, RUN, COPY each create a cached layer"),
    ("Rule 2", "Cache is checked top-to-bottom",
     "Docker checks each layer against its cache sequentially"),
    ("Rule 3", "If a layer changes, ALL layers after it rebuild",
     "This is why order matters so much!"),
    ("Rule 4", "COPY invalidates cache if files change",
     "Docker hashes file contents to detect changes"),
    ("Rule 5", "RUN uses the instruction text as cache key",
     "'RUN pip install pkg' is cached unless preceding layers changed"),
]

for name, rule, detail in rules:
    print(f"  {name}: {rule}")
    print(f"    → {detail}\n")


# ============================================================
# TODO 1: Optimize a Dockerfile with multiple COPY steps
# ============================================================

print("\n--- TODO 1: Optimize Multi-File Copy ---\n")

# This Dockerfile copies 3 config files. Optimize it so that
# changing only main.py doesn't bust the dependency cache.
# The key: separate files that change often from files that change rarely.

unoptimized = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN pip install --no-cache-dir -r requirements.txt
    RUN python -c "import nltk; nltk.download('punkt')"
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# TODO: Rewrite with optimal layer ordering.
# Files that change rarely: requirements.txt, nltk_setup.py
# Files that change often: main.py, config.py, templates/

optimized = unoptimized  # Replace with your optimization

# Uncomment:
# optimized = textwrap.dedent('''\
#     FROM python:3.11-slim
#     WORKDIR /app
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir -r requirements.txt
#     RUN python -c "import nltk; nltk.download('punkt')"
#     COPY . .
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

# Validate
lines = [l.strip() for l in optimized.strip().split("\n")]
pip_idx = next((i for i, l in enumerate(lines) if "pip install" in l), -1)
copy_all_idx = next((i for i, l in enumerate(lines) if l in ("COPY . .", "COPY . /app")), -1)
copy_req_idx = next((i for i, l in enumerate(lines) if "requirements" in l and l.startswith("COPY")), -1)

if copy_req_idx != -1 and pip_idx != -1 and copy_all_idx != -1:
    order_ok = copy_req_idx < pip_idx < copy_all_idx
    print(f"  [{'PASS' if order_ok else 'FAIL'}] Layer order: COPY req → pip install → COPY . .")
else:
    print("  [TODO] Reorder: COPY requirements.txt → pip install → COPY . .")

if optimized != unoptimized:
    with open(os.path.join(WORKDIR, "Dockerfile.optimized"), "w") as f:
        f.write(optimized)
    print(f"  Saved to {WORKDIR}/Dockerfile.optimized")


# ============================================================
# TODO 2: Split requirements for AI apps
# ============================================================

print("\n\n--- TODO 2: Split Requirements ---\n")

# AI apps often have heavy base packages (langchain, chromadb) and
# lighter app-specific packages. Split them for better caching.

# TODO: Write a Dockerfile that:
# 1. First installs requirements-base.txt (heavy, rarely changes)
# 2. Then installs requirements-app.txt (light, changes more often)
# 3. Then copies the application code

requirements_base = textwrap.dedent('''\
    langchain-core==0.1.23
    langchain-groq==0.0.3
    langgraph==0.0.26
    chromadb==0.4.22
    sentence-transformers==2.3.1
''')

requirements_app = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    python-dotenv==1.0.0
    httpx==0.25.2
''')

# TODO: Write the split-requirements Dockerfile
split_dockerfile = ""

# Uncomment:
# split_dockerfile = textwrap.dedent('''\
#     FROM python:3.11-slim
#     WORKDIR /app
#
#     # Layer 1: Heavy base packages (cached most of the time)
#     COPY requirements-base.txt .
#     RUN pip install --no-cache-dir -r requirements-base.txt
#
#     # Layer 2: Lighter app packages (changes when you add a new dep)
#     COPY requirements-app.txt .
#     RUN pip install --no-cache-dir -r requirements-app.txt
#
#     # Layer 3: Application code (changes most often)
#     COPY . .
#
#     ENV PYTHONUNBUFFERED=1
#     EXPOSE 8000
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

if split_dockerfile:
    has_base = "requirements-base" in split_dockerfile
    has_app = "requirements-app" in split_dockerfile
    # Check order: base before app before COPY . .
    base_idx = split_dockerfile.find("requirements-base")
    app_idx = split_dockerfile.find("requirements-app")
    code_idx = split_dockerfile.find("COPY . .")
    order_ok = base_idx < app_idx < code_idx if all(i >= 0 for i in [base_idx, app_idx, code_idx]) else False

    print(f"  [{'PASS' if has_base else 'FAIL'}] Uses requirements-base.txt")
    print(f"  [{'PASS' if has_app else 'FAIL'}] Uses requirements-app.txt")
    print(f"  [{'PASS' if order_ok else 'FAIL'}] Correct order: base → app → code")

    with open(os.path.join(WORKDIR, "requirements-base.txt"), "w") as f:
        f.write(requirements_base)
    with open(os.path.join(WORKDIR, "requirements-app.txt"), "w") as f:
        f.write(requirements_app)
    with open(os.path.join(WORKDIR, "Dockerfile.split"), "w") as f:
        f.write(split_dockerfile)
    print(f"\n  Saved split requirements and Dockerfile.split to {WORKDIR}/")
else:
    print("  TODO: Write a Dockerfile with split requirements")
    print("  Pattern:")
    print("    COPY requirements-base.txt . → pip install (heavy, stable)")
    print("    COPY requirements-app.txt .  → pip install (light, changes)")
    print("    COPY . .                     → app code (changes most)")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 03 Summary ---\n")
print("  Layer caching rules:")
print("    1. Put things that change LESS frequently EARLIER")
print("    2. requirements.txt before application code")
print("    3. Split heavy deps (base) from light deps (app)")
print("    4. One changed layer busts ALL subsequent layers")
print("    5. Proper ordering: 30x faster rebuilds!")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
