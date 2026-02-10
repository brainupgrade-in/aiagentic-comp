"""
Lab 03 Solution: Layer Caching Optimization
=============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-03"

print("=" * 50)
print("  Lab 03 Solution: Layer Caching")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Steps 1-3: Same as lab (caching concepts)
# ============================================================

print("\n--- Steps 1-3: Caching Concepts ---\n")
print("  Rule: Things that change less → earlier in Dockerfile")
print("  Rule: When a layer changes, ALL after it rebuild")
print("  Rule: COPY invalidates cache if file contents change")

# ============================================================
# TODO 1 Solution: Optimized multi-file Dockerfile
# ============================================================

print("\n\n--- TODO 1 Solution: Optimized Layer Ordering ---\n")

optimized = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    RUN python -c "import nltk; nltk.download('punkt')"
    COPY . .
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

lines = [l.strip() for l in optimized.strip().split("\n")]
pip_idx = next((i for i, l in enumerate(lines) if "pip install" in l), -1)
copy_all_idx = next((i for i, l in enumerate(lines) if l == "COPY . ."), -1)
copy_req_idx = next((i for i, l in enumerate(lines) if "requirements" in l and l.startswith("COPY")), -1)

order_ok = copy_req_idx < pip_idx < copy_all_idx
print(f"  [{'PASS' if order_ok else 'FAIL'}] Layer order: COPY req → pip install → COPY . .")

with open(os.path.join(WORKDIR, "Dockerfile.optimized"), "w") as f:
    f.write(optimized)

print("\n  Optimization explained:")
print("    1. COPY requirements.txt .          ← Rarely changes (cached)")
print("    2. RUN pip install -r req.txt        ← Cached if req unchanged")
print("    3. RUN python -c 'nltk.download()'   ← Cached if pip unchanged")
print("    4. COPY . .                          ← Changes often, but previous cached")
print()
print("  When you edit main.py: only step 4 rebuilds (~0.1s)")
print("  Without optimization: steps 2-4 all rebuild (~5+ min)")


# ============================================================
# TODO 2 Solution: Split requirements
# ============================================================

print("\n\n--- TODO 2 Solution: Split Requirements ---\n")

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

split_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app

    # Layer 1: Heavy base packages (cached most of the time)
    COPY requirements-base.txt .
    RUN pip install --no-cache-dir -r requirements-base.txt

    # Layer 2: Lighter app packages (changes when you add a new dep)
    COPY requirements-app.txt .
    RUN pip install --no-cache-dir -r requirements-app.txt

    # Layer 3: Application code (changes most often)
    COPY . .

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

has_base = "requirements-base" in split_dockerfile
has_app = "requirements-app" in split_dockerfile
base_idx = split_dockerfile.find("requirements-base")
app_idx = split_dockerfile.find("requirements-app")
code_idx = split_dockerfile.find("COPY . .")
order_ok = base_idx < app_idx < code_idx

print(f"  [{'PASS' if has_base else 'FAIL'}] Uses requirements-base.txt")
print(f"  [{'PASS' if has_app else 'FAIL'}] Uses requirements-app.txt")
print(f"  [{'PASS' if order_ok else 'FAIL'}] Correct order: base → app → code")

with open(os.path.join(WORKDIR, "requirements-base.txt"), "w") as f:
    f.write(requirements_base)
with open(os.path.join(WORKDIR, "requirements-app.txt"), "w") as f:
    f.write(requirements_app)
with open(os.path.join(WORKDIR, "Dockerfile.split"), "w") as f:
    f.write(split_dockerfile)

print("\n  Split strategy:")
print("    requirements-base.txt: ~2 GB packages (langchain, chromadb, transformers)")
print("    requirements-app.txt:  ~50 MB packages (fastapi, uvicorn, httpx)")
print()
print("  Scenario: You add 'httpx' to requirements-app.txt")
print("    - Layer 1 (base): CACHED (langchain etc unchanged)")
print("    - Layer 2 (app):  REBUILDS (new package added)")
print("    - Layer 3 (code): REBUILDS (after layer 2)")
print("    - Savings: Skip reinstalling 2 GB of base packages!")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Optimized layer ordering (requirements before code)")
print("- TODO 2: Split requirements (base 2GB cached, app 50MB changes)")
