"""
Lab 02: LangFuse Setup & Deployment
======================================
Set up LangFuse SDK in mock mode (local JSON logging)
and configure environment variables.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-11-02"

print("=" * 50)
print("  Lab 02: LangFuse Setup & Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: LangFuse Architecture (Mock Mode)
# ============================================================

print("\n--- Step 1: LangFuse Architecture (Mock Mode) ---\n")

print("  LangFuse mock mode components:\n")
print("    LangChain App")
print("        │")
print("        ▼")
print("    LangFuse SDK / CallbackHandler")
print("        │")
print("        ▼")
print("    MockLangfuse (local JSON logging)")
print("        │")
print("        ▼")
print("    JSON files (trace storage)")
print()
print("  Mock mode: Same SDK patterns, data saved to local JSON files")
print("  In production: Point LANGFUSE_HOST to a real LangFuse server")


# ============================================================
# Step 2: MockLangfuse Reference
# ============================================================

print("\n\n--- Step 2: MockLangfuse Reference ---\n")

mock_ref = textwrap.dedent("""\
    import json
    import os
    from datetime import datetime

    class MockLangfuse:
        \"\"\"Mock LangFuse client that logs traces to local JSON files.\"\"\"

        def __init__(self, public_key, secret_key, host, output_dir="/tmp/langfuse-traces"):
            self.public_key = public_key
            self.secret_key = secret_key
            self.host = host
            self.output_dir = output_dir
            os.makedirs(output_dir, exist_ok=True)
            self._traces = []

        def trace(self, name, metadata=None):
            trace_data = {
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
                "generations": [],
            }
            self._traces.append(trace_data)
            return MockTrace(trace_data)

        def flush(self):
            output_file = os.path.join(self.output_dir, "traces.json")
            with open(output_file, "w") as f:
                json.dump(self._traces, f, indent=2)
            return len(self._traces)

        def get_traces(self):
            output_file = os.path.join(self.output_dir, "traces.json")
            if os.path.exists(output_file):
                with open(output_file) as f:
                    return json.load(f)
            return []

    class MockTrace:
        def __init__(self, trace_data):
            self._data = trace_data

        def generation(self, name, model=None, input=None, output=None):
            gen = {"name": name, "model": model, "input": input, "output": output}
            self._data["generations"].append(gen)
            return gen
""")

print("  Reference MockLangfuse class:\n")
for line in mock_ref.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "mock_langfuse_reference.py"), "w") as f:
    f.write(mock_ref)


# ============================================================
# Step 3: Environment Variables
# ============================================================

print("\n\n--- Step 3: Environment Variables ---\n")

print("  Client-side (your Python app):\n")
env_vars = [
    ("LANGFUSE_PUBLIC_KEY",  "pk-lf-mock-...",            "API public key"),
    ("LANGFUSE_SECRET_KEY",  "sk-lf-mock-...",            "API secret key"),
    ("LANGFUSE_HOST",        "http://localhost:8000",      "LangFuse server URL (or mock)"),
]
for name, example, desc in env_vars:
    print(f"    {name:<25} {example:<30} # {desc}")

print("\n  Mock mode configuration:\n")
mock_vars = [
    ("output_dir",           "/tmp/langfuse-traces"),
    ("flush()",              "Writes traces to JSON file"),
    ("get_traces()",         "Reads back traces from JSON"),
]
for name, desc in mock_vars:
    print(f"    {name:<20} {desc}")


# ============================================================
# TODO 1: Create MockLangfuse Setup
# ============================================================

print("\n\n--- TODO 1: MockLangfuse Configuration ---\n")

print("  Create a MockLangfuse setup with:")
print("    - MockLangfuse class with __init__, trace, flush, get_traces")
print("    - trace() creates a trace dict with name, timestamp, metadata, generations")
print("    - generation() adds to the trace's generations list")
print("    - flush() writes all traces to a JSON file")
print("    - get_traces() reads traces back from the JSON file")

# SOLUTION: MockLangfuse setup for local trace logging
todo1_code = textwrap.dedent("""\
    import json
    import os
    from datetime import datetime

    class MockLangfuse:
        def __init__(self, public_key, secret_key, host, output_dir="/tmp/langfuse-traces"):
            self.public_key = public_key
            self.secret_key = secret_key
            self.host = host
            self.output_dir = output_dir
            os.makedirs(output_dir, exist_ok=True)
            self._traces = []

        def trace(self, name, metadata=None):
            trace_data = {
                "name": name,
                "timestamp": datetime.now().isoformat(),
                "metadata": metadata or {},
                "generations": [],
            }
            self._traces.append(trace_data)
            return MockTrace(trace_data)

        def flush(self):
            output_file = os.path.join(self.output_dir, "traces.json")
            with open(output_file, "w") as f:
                json.dump(self._traces, f, indent=2)
            return len(self._traces)

        def get_traces(self):
            output_file = os.path.join(self.output_dir, "traces.json")
            if os.path.exists(output_file):
                with open(output_file) as f:
                    return json.load(f)
            return []

    class MockTrace:
        def __init__(self, trace_data):
            self._data = trace_data

        def generation(self, name, model=None, input=None, output=None):
            gen = {"name": name, "model": model, "input": input, "output": output}
            self._data["generations"].append(gen)
            return gen
""")

with open(os.path.join(WORKDIR, "mock_langfuse.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has class MockLangfuse",     "class MockLangfuse" in todo1_code),
    ("Has __init__ method",        "__init__" in todo1_code),
    ("Has output_dir param",       "output_dir" in todo1_code),
    ("Has trace method",           "def trace" in todo1_code),
    ("Has timestamp",              "timestamp" in todo1_code or "datetime" in todo1_code),
    ("Has generations list",       "generations" in todo1_code),
    ("Has flush method",           "def flush" in todo1_code),
    ("Has json.dump",              "json.dump" in todo1_code),
    ("Has get_traces method",      "def get_traces" in todo1_code),
    ("Has json.load",              "json.load" in todo1_code),
    ("Has MockTrace class",        "class MockTrace" in todo1_code or "MockTrace" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"\n  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Client environment setup
# ============================================================

print("\n\n--- TODO 2: Client Environment Setup ---\n")

print("  Create the Python code to initialize LangFuse client.")
print("  Include: environment variables, Langfuse() client, health check.\n")

# SOLUTION: LangFuse client initialization
todo2_code = textwrap.dedent("""\
    import os
    from langfuse import Langfuse

    # Set environment variables for LangFuse
    os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-mock-public-key"
    os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-mock-secret-key"
    os.environ["LANGFUSE_HOST"] = "http://localhost:8000"

    # Create LangFuse client
    langfuse = Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ["LANGFUSE_HOST"],
    )

    # Health check
    print("LangFuse client initialized successfully")
    print(f"Host: {os.environ['LANGFUSE_HOST']}")
""")

with open(os.path.join(WORKDIR, "langfuse_client.py"), "w") as f:
    f.write(todo2_code)

checks2 = [
    ("Has os import",              "import os" in todo2_code or "from os" in todo2_code),
    ("Has LANGFUSE_PUBLIC_KEY",    "LANGFUSE_PUBLIC_KEY" in todo2_code),
    ("Has LANGFUSE_SECRET_KEY",    "LANGFUSE_SECRET_KEY" in todo2_code),
    ("Has LANGFUSE_HOST",          "LANGFUSE_HOST" in todo2_code),
    ("Has Langfuse import",        "Langfuse" in todo2_code or "langfuse" in todo2_code),
    ("Has client creation",        "Langfuse(" in todo2_code),
]

score2 = sum(1 for _, ok in checks2 if ok)
print(f"  Validating ({score2}/{len(checks2)}):\n")
for name, ok in checks2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. Mock LangFuse: Same SDK patterns, traces saved to local JSON")
print("    2. MockLangfuse: trace(), generation(), flush(), get_traces()")
print("    3. Client env vars: LANGFUSE_PUBLIC_KEY, SECRET_KEY, HOST")
print("    4. In production: Point LANGFUSE_HOST to a real LangFuse server")
print(f"\n  TODO 1: {score1}/{len(checks1)} MockLangfuse checks passed")
print(f"  TODO 2: {score2}/{len(checks2)} client setup checks passed")
print(f"\n  Files generated in {WORKDIR}/")
