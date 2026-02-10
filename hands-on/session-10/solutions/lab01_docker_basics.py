"""
Lab 01 Solution: Docker Basics Exploration
=============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-01"

print("=" * 50)
print("  Lab 01 Solution: Docker Basics")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1-3: Same as lab (concepts)
# ============================================================

print("\n--- Steps 1-3: Docker Concepts ---\n")

class VirtualMachine:
    def __init__(self, name, app_size_mb=100):
        self.name = name
        self.guest_os_mb = 2000
        self.hypervisor_mb = 200
        self.app_mb = app_size_mb
        self.total_mb = self.guest_os_mb + self.hypervisor_mb + self.app_mb
        self.startup_seconds = 60

class Container:
    def __init__(self, name, app_size_mb=100):
        self.name = name
        self.shared_kernel = True
        self.runtime_overhead_mb = 5
        self.app_mb = app_size_mb
        self.total_mb = self.runtime_overhead_mb + self.app_mb
        self.startup_seconds = 2

vm = VirtualMachine("ai-agent-vm", 150)
container = Container("ai-agent-container", 150)
print(f"  VM: {vm.total_mb} MB, {vm.startup_seconds}s startup")
print(f"  Container: {container.total_mb} MB, {container.startup_seconds}s startup")
print(f"  Container is {vm.total_mb / container.total_mb:.0f}x smaller")

# ============================================================
# Step 4: Create app files and Dockerfile
# ============================================================

print("\n\n--- Step 4: Create Dockerfile ---\n")

app_code = textwrap.dedent('''\
    from fastapi import FastAPI

    app = FastAPI(title="UniGPS Agent", version="1.0.0")

    @app.get("/health")
    async def health():
        return {"status": "healthy", "agent": "ready"}

    @app.get("/")
    async def root():
        return {"message": "UniGPS AI Agent is running"}
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn==0.24.0
''')

dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)
with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(dockerfile)

print(f"  Created Dockerfile, main.py, requirements.txt in {WORKDIR}/")

# ============================================================
# TODO 1 Solution: Instruction explanations
# ============================================================

print("\n\n--- TODO 1 Solution: Instruction Explanations ---\n")

instruction_quiz = {
    "FROM":    "Sets the base image to build on top of",
    "WORKDIR": "Sets the working directory for subsequent instructions",
    "COPY":    "Copies files from the host machine into the image",
    "RUN":     "Executes a command during the image build process",
    "ENV":     "Sets environment variables available at runtime",
    "EXPOSE":  "Documents which port the container listens on",
    "CMD":     "Specifies the default command to run when container starts",
}

for instr, explanation in instruction_quiz.items():
    print(f"    [DONE] {instr:<10} → {explanation}")

# ============================================================
# TODO 2 Solution: Fix the broken Dockerfile
# ============================================================

print("\n\n--- TODO 2 Solution: Fixed Dockerfile ---\n")

fixed_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# Validate
problems_found = []
lines = fixed_dockerfile.strip().split("\n")
lines_stripped = [l.strip() for l in lines]

copy_all_idx = None
copy_req_idx = None
for i, line in enumerate(lines_stripped):
    if line.startswith("COPY . ."):
        copy_all_idx = i
    if "requirements.txt" in line and line.startswith("COPY"):
        copy_req_idx = i

if copy_req_idx is None or (copy_all_idx is not None and copy_req_idx > copy_all_idx):
    problems_found.append("Layer caching: COPY requirements.txt before COPY . .")
if "--no-cache-dir" not in fixed_dockerfile:
    problems_found.append("Missing --no-cache-dir")
if 'CMD ["' not in fixed_dockerfile:
    problems_found.append("CMD should use exec form")

if problems_found:
    for p in problems_found:
        print(f"    ISSUE: {p}")
else:
    print("  All 3 problems fixed!")
    print("  Fixes:")
    print("    1. COPY requirements.txt before COPY . . (layer caching)")
    print("    2. Added --no-cache-dir to pip install (saves space)")
    print("    3. CMD uses exec form [\"cmd\", \"arg\"] (signal handling)")

with open(os.path.join(WORKDIR, "Dockerfile.fixed"), "w") as f:
    f.write(fixed_dockerfile)

print(f"\n  Saved to {WORKDIR}/Dockerfile.fixed")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print("- TODO 1: All 7 Dockerfile instructions explained")
print("- TODO 2: 3 Dockerfile problems fixed (caching, no-cache-dir, exec form)")
