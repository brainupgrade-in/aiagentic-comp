"""
Lab 02 Solution: Tool Calling Patterns
========================================
"""

import os
import shutil
import json
import fnmatch

WORKDIR = "/tmp/aidev-lab-10-02"

print("=" * 50)
print("  Lab 02: Tool Calling Patterns (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Core Tool Functions
# ============================================================

print("\n--- Step 1: Core Tool Functions ---\n")

def read_file(path):
    """Read and return file contents. Returns error string on failure."""
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR: {e}"


def write_file(path, content):
    """Write content to a file. Creates parent directories if needed."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"OK: Wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"ERROR: {e}"


print("  Defined: read_file(path), write_file(path, content)")

demo_path = os.path.join(WORKDIR, "demo.txt")
result = write_file(demo_path, "Hello from the coding agent!")
print(f"\n  write_file demo: {result}")
result = read_file(demo_path)
print(f"  read_file demo:  {result}")
result = read_file("/tmp/nonexistent_file_xyz.txt")
print(f"  read_file error: {result}")


# ============================================================
# Step 2: Dispatcher Pattern
# ============================================================

print("\n\n--- Step 2: Dispatcher Pattern ---\n")

print("  A dispatcher maps tool names to functions, then routes calls.")


# ============================================================
# TODO 1 Solution: Implement search_files
# ============================================================

print("\n--- TODO 1: Implement search_files ---\n")

def search_files(pattern, directory=WORKDIR):
    """
    Search for files matching a glob pattern in directory.
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                matches.append(os.path.join(root, filename))
    return matches


# Create test files
write_file(os.path.join(WORKDIR, "app.py"), "print('hello')")
write_file(os.path.join(WORKDIR, "test_app.py"), "assert True")
write_file(os.path.join(WORKDIR, "README.md"), "# My App")
write_file(os.path.join(WORKDIR, "sub", "utils.py"), "def helper(): pass")

score1 = 0
checks_1 = []

result1 = search_files("*.py", WORKDIR)

if isinstance(result1, list):
    checks_1.append(("Returns a list", "PASS"))
    score1 += 1
else:
    checks_1.append(("Returns a list", "FAIL"))

py_files = result1 if isinstance(result1, list) else []
if len(py_files) >= 3:
    checks_1.append(("Finds *.py files", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Finds *.py files (got {len(py_files)}, expected >= 3)", "FAIL"))

if any("sub" in p for p in py_files):
    checks_1.append(("Finds files in subdirectories", "PASS"))
    score1 += 1
else:
    checks_1.append(("Finds files in subdirectories", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2 Solution: Implement tool_dispatcher
# ============================================================

print("\n\n--- TODO 2: Implement tool_dispatcher ---\n")

def tool_dispatcher(tool_name, **kwargs):
    """Dispatch a tool call to the correct function."""
    tools = {
        "read_file": read_file,
        "write_file": write_file,
        "search_files": search_files,
    }
    if tool_name not in tools:
        return f"ERROR: Unknown tool: {tool_name}"
    return tools[tool_name](**kwargs)


score2 = 0
checks_2 = []

r1 = tool_dispatcher("write_file", path=os.path.join(WORKDIR, "dispatched.txt"), content="via dispatcher")
if isinstance(r1, str) and "OK" in r1:
    checks_2.append(("Dispatches write_file", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Dispatches write_file (got: {r1})", "FAIL"))

r2 = tool_dispatcher("read_file", path=os.path.join(WORKDIR, "dispatched.txt"))
if isinstance(r2, str) and "via dispatcher" in r2:
    checks_2.append(("Dispatches read_file", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Dispatches read_file (got: {r2})", "FAIL"))

r3 = tool_dispatcher("delete_everything")
if isinstance(r3, str) and "error" in r3.lower():
    checks_2.append(("Handles unknown tool", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Handles unknown tool (got: {r3})", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3 Solution: Chain 3 tool calls
# ============================================================

print("\n\n--- TODO 3: Chain 3 Tool Calls ---\n")

# Step A: Write a file
step_a_result = tool_dispatcher(
    "write_file",
    path=os.path.join(WORKDIR, "agent_output.py"),
    content="# Generated by agent\nprint('done')"
)

# Step B: Read it back
step_b_result = tool_dispatcher(
    "read_file",
    path=os.path.join(WORKDIR, "agent_output.py")
)

# Step C: Search for .py files
step_c_result = tool_dispatcher(
    "search_files",
    pattern="*.py",
    directory=WORKDIR
)

score3 = 0
checks_3 = []

if isinstance(step_a_result, str) and "OK" in step_a_result:
    checks_3.append(("Step A: write file", "PASS"))
    score3 += 1
else:
    checks_3.append((f"Step A: write file (got: {step_a_result})", "FAIL"))

if isinstance(step_b_result, str) and "Generated by agent" in step_b_result:
    checks_3.append(("Step B: read file back", "PASS"))
    score3 += 1
else:
    checks_3.append((f"Step B: read file back (got: {step_b_result})", "FAIL"))

if isinstance(step_c_result, list) and len(step_c_result) >= 1:
    checks_3.append(("Step C: search for .py files", "PASS"))
    score3 += 1
else:
    checks_3.append((f"Step C: search for .py files (got: {step_c_result})", "FAIL"))

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 3 + 3 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 02 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Tool functions wrap OS operations with error handling")
print(f"    2. A dispatcher routes tool calls by name to functions")
print(f"    3. Agents chain multiple tool calls to accomplish tasks")
print(f"\n  TODO 1: {score1}/3 search_files checks passed")
print(f"  TODO 2: {score2}/3 dispatcher checks passed")
print(f"  TODO 3: {score3}/3 chain steps passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
