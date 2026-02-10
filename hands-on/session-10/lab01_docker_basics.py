"""
Lab 01: Docker Basics Exploration
==================================
Learn Docker concepts through code analogies, then create your first Dockerfile.

No Docker installation required — this lab teaches concepts and generates files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-01"

print("=" * 50)
print("  Lab 01: Docker Basics Exploration")
print("=" * 50)

# Clean up previous run
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Containers vs VMs — Code Analogy
# ============================================================

print("\n--- Step 1: Containers vs VMs ---\n")

# Think of VMs vs Containers like this:

class VirtualMachine:
    """Each VM has its OWN operating system (heavy)."""
    def __init__(self, name, app_size_mb=100):
        self.name = name
        self.guest_os_mb = 2000     # Full Ubuntu/Windows
        self.hypervisor_mb = 200    # Virtualization layer
        self.app_mb = app_size_mb
        self.total_mb = self.guest_os_mb + self.hypervisor_mb + self.app_mb
        self.startup_seconds = 60   # Minutes to boot OS

class Container:
    """Containers SHARE the host kernel (lightweight)."""
    def __init__(self, name, app_size_mb=100):
        self.name = name
        self.shared_kernel = True   # No guest OS needed
        self.runtime_overhead_mb = 5
        self.app_mb = app_size_mb
        self.total_mb = self.runtime_overhead_mb + self.app_mb
        self.startup_seconds = 2    # Seconds to start process

# Compare
vm = VirtualMachine("ai-agent-vm", app_size_mb=150)
container = Container("ai-agent-container", app_size_mb=150)

print(f"  Virtual Machine: {vm.name}")
print(f"    Size: {vm.total_mb} MB (app={vm.app_mb} + OS={vm.guest_os_mb} + hypervisor={vm.hypervisor_mb})")
print(f"    Startup: ~{vm.startup_seconds}s")
print()
print(f"  Container: {container.name}")
print(f"    Size: {container.total_mb} MB (app={container.app_mb} + runtime={container.runtime_overhead_mb})")
print(f"    Startup: ~{container.startup_seconds}s")
print()
print(f"  Container is {vm.total_mb / container.total_mb:.0f}x smaller, {vm.startup_seconds / container.startup_seconds:.0f}x faster to start")

# ============================================================
# Step 2: Images vs Containers — Class vs Object
# ============================================================

print("\n\n--- Step 2: Images vs Containers (Class vs Object) ---\n")

class DockerImage:
    """An image is a READ-ONLY blueprint (like a Python class)."""
    def __init__(self, name, tag, layers):
        self.name = name
        self.tag = tag
        self.layers = layers  # Each layer is immutable
        self.read_only = True

    def run(self, container_name):
        """Create a container (running instance) from this image."""
        return DockerContainer(container_name, image=self)


class DockerContainer:
    """A container is a RUNNING INSTANCE (like a Python object)."""
    def __init__(self, name, image):
        self.name = name
        self.image = image
        self.writable_layer = {}  # Thin writable layer on top
        self.running = True

    def write_file(self, path, content):
        """Writes go to the writable layer, NOT the image."""
        self.writable_layer[path] = content


# Image (blueprint)
image = DockerImage(
    name="unigps-agent",
    tag="1.0",
    layers=[
        "python:3.11-slim (base OS + Python)",
        "pip install langchain fastapi (dependencies)",
        "COPY main.py (application code)",
    ]
)

print(f"  Image: {image.name}:{image.tag}")
print(f"  Read-only: {image.read_only}")
print(f"  Layers ({len(image.layers)}):")
for i, layer in enumerate(image.layers):
    print(f"    [{i}] {layer}")

# Create multiple containers from ONE image
containers = []
for i in range(3):
    c = image.run(f"agent-{i+1}")
    c.write_file("/app/logs/request.log", f"Request handled by agent-{i+1}")
    containers.append(c)

print(f"\n  Created {len(containers)} containers from 1 image:")
for c in containers:
    print(f"    {c.name}: running={c.running}, writable_files={len(c.writable_layer)}")

# ============================================================
# Step 3: Docker Layers — Stacked Filesystem
# ============================================================

print("\n\n--- Step 3: Docker Layers ---\n")

class LayerStack:
    """Each Dockerfile instruction creates a new layer."""
    def __init__(self):
        self.layers = []

    def add_layer(self, instruction, description, size_mb):
        self.layers.append({
            "instruction": instruction,
            "description": description,
            "size_mb": size_mb,
            "cached": False,
        })

    def display(self):
        total = sum(l["size_mb"] for l in self.layers)
        print(f"  {'Layer':<6} {'Instruction':<35} {'Size':>8}  {'Status'}")
        print("  " + "-" * 65)
        for i, layer in enumerate(reversed(self.layers)):
            status = "CACHED" if layer["cached"] else "NEW"
            print(f"  [{i}]    {layer['instruction']:<35} {layer['size_mb']:>6} MB  {status}")
        print("  " + "-" * 65)
        print(f"  {'Total':<42} {total:>6} MB")

stack = LayerStack()
stack.add_layer("FROM python:3.11-slim", "Base OS + Python runtime", 150)
stack.add_layer("RUN apt-get install curl", "System packages", 15)
stack.add_layer("COPY requirements.txt .", "Dependency list", 0)
stack.add_layer("RUN pip install -r req.txt", "Python packages", 200)
stack.add_layer("COPY . .", "Application code", 5)

print("  Image Layer Stack (bottom to top):\n")
stack.display()

print(f"\n  Key insight: If layer [3] changes, layers [4] must rebuild.")
print(f"  But layers [0]-[2] can be reused from cache!")


# ============================================================
# Step 4: Create Your First Dockerfile
# ============================================================

print("\n\n--- Step 4: Create Your First Dockerfile ---\n")

# First, create the app files that the Dockerfile will package
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

# Write app files
with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)

with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)

# Generate a Dockerfile
dockerfile = textwrap.dedent('''\
    # Base image: Python 3.11 (slim variant for smaller size)
    FROM python:3.11-slim

    # Set working directory inside the container
    WORKDIR /app

    # Copy requirements first (for layer caching)
    COPY requirements.txt .

    # Install Python dependencies
    RUN pip install --no-cache-dir -r requirements.txt

    # Copy application code
    COPY . .

    # Set environment variable for unbuffered output
    ENV PYTHONUNBUFFERED=1

    # Document the port the app listens on
    EXPOSE 8000

    # Default command to run the application
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(dockerfile)

print(f"  Created files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<25} ({size} bytes)")

print(f"\n  Dockerfile contents:")
for i, line in enumerate(dockerfile.strip().split("\n"), 1):
    print(f"    {i:>3}: {line}")


# ============================================================
# TODO 1: Explain each Dockerfile instruction
# ============================================================

print("\n\n--- TODO 1: Explain Dockerfile Instructions ---\n")

# TODO: Fill in the explanations for each Dockerfile instruction.
# Replace the "???" with a short description of what each instruction does.

instruction_quiz = {
    "FROM":    "???",   # What does FROM do?
    "WORKDIR": "???",   # What does WORKDIR do?
    "COPY":    "???",   # What does COPY do?
    "RUN":     "???",   # What does RUN do?
    "ENV":     "???",   # What does ENV do?
    "EXPOSE":  "???",   # What does EXPOSE do?
    "CMD":     "???",   # What does CMD do?
}

# Uncomment and fill in:
# instruction_quiz = {
#     "FROM":    "Sets the base image to build on top of",
#     "WORKDIR": "Sets the working directory for subsequent instructions",
#     "COPY":    "Copies files from the host machine into the image",
#     "RUN":     "Executes a command during the image build process",
#     "ENV":     "Sets environment variables available at runtime",
#     "EXPOSE":  "Documents which port the container listens on",
#     "CMD":     "Specifies the default command to run when container starts",
# }

print("  Your instruction explanations:")
for instr, explanation in instruction_quiz.items():
    status = "DONE" if explanation != "???" else "TODO"
    print(f"    [{status}] {instr:<10} → {explanation}")


# ============================================================
# TODO 2: Fix the broken Dockerfile
# ============================================================

print("\n\n--- TODO 2: Fix the Broken Dockerfile ---\n")

# This Dockerfile has 3 problems. Find and fix them.
# Hint: Think about layer caching, missing instructions, and the CMD format.

broken_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    COPY . .

    RUN pip install -r requirements.txt

    CMD uvicorn main:app --host 0.0.0.0
''')

# TODO: Write the fixed version below.
# Problems to fix:
# 1. Layer caching: COPY . . before pip install means every code change reinstalls packages
# 2. Missing: --no-cache-dir flag on pip install (wastes space in the image)
# 3. CMD format: Should use exec form ["uvicorn", ...] not shell form (proper signal handling)

fixed_dockerfile = broken_dockerfile  # Replace with your fix

# Uncomment to see the fix:
# fixed_dockerfile = textwrap.dedent('''\
#     FROM python:3.11-slim
#
#     WORKDIR /app
#
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir -r requirements.txt
#
#     COPY . .
#
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

# Validate the fix
problems_found = []
lines = fixed_dockerfile.strip().split("\n")
lines_stripped = [l.strip() for l in lines]

# Check 1: requirements.txt should be copied before COPY . .
copy_all_idx = None
copy_req_idx = None
for i, line in enumerate(lines_stripped):
    if line.startswith("COPY . .") or line.startswith("COPY . /"):
        copy_all_idx = i
    if "requirements.txt" in line and line.startswith("COPY"):
        copy_req_idx = i

if copy_req_idx is None or (copy_all_idx is not None and copy_req_idx > copy_all_idx):
    problems_found.append("Layer caching: COPY requirements.txt should come BEFORE COPY . .")

# Check 2: --no-cache-dir
if "--no-cache-dir" not in fixed_dockerfile:
    problems_found.append("Missing --no-cache-dir on pip install")

# Check 3: CMD exec form
if 'CMD ["' not in fixed_dockerfile and "CMD ['" not in fixed_dockerfile:
    problems_found.append("CMD should use exec form [\"cmd\", \"arg\"] not shell form")

if problems_found:
    print("  Issues remaining:")
    for p in problems_found:
        print(f"    - {p}")
else:
    print("  All 3 problems fixed!")
    with open(os.path.join(WORKDIR, "Dockerfile.fixed"), "w") as f:
        f.write(fixed_dockerfile)
    print(f"  Saved to {WORKDIR}/Dockerfile.fixed")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 01 Summary ---\n")
print("  Docker concepts covered:")
print("    1. Containers are lighter/faster than VMs (shared kernel)")
print("    2. Images are read-only blueprints; containers are running instances")
print("    3. Images are built from stacked layers (each instruction = 1 layer)")
print("    4. Dockerfile defines how to build an image")
print(f"\n  Files generated in: {WORKDIR}/")

# Check if Docker is available
docker_available = shutil.which("docker") is not None
if docker_available:
    print(f"\n  Docker detected! Try building:")
    print(f"    cd {WORKDIR}")
    print(f"    docker build -t my-first-ai-app:1.0 .")
    print(f"    docker run -p 8000:8000 my-first-ai-app:1.0")
else:
    print("\n  Docker not installed — that's OK! The generated files are valid.")
    print("  You can build them on any machine with Docker.")
