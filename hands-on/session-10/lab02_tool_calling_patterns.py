"""
Lab 02: Tool Calling Patterns
================================
Build actual tool functions and a dispatcher that routes
tool calls by name — the core mechanism inside every coding agent.

What you'll learn:
- Implementing file read/write/search tools
- Dispatcher pattern for tool routing
- Chaining multiple tool calls in sequence

No API key needed — pure Python standard library.
"""

import os
import shutil
import json
import fnmatch

WORKDIR = "/tmp/aidev-lab-10-02"

print("=" * 50)
print("  Lab 02: Tool Calling Patterns")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Define Tool Functions
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
print("  These handle errors gracefully and return status strings.")

# Demo
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

print("  A dispatcher maps tool names to functions, then routes calls:\n")

print("""  Example dispatcher:

    TOOLS = {
        "read_file":  read_file,
        "write_file": write_file,
        "search_files": search_files,
    }

    def dispatch(tool_name, **kwargs):
        if tool_name not in TOOLS:
            return f"ERROR: Unknown tool: {tool_name}"
        return TOOLS[tool_name](**kwargs)

  The LLM outputs a tool call like:
    {"tool": "write_file", "args": {"path": "app.py", "content": "..."}}
  The dispatcher executes it and returns the result to the LLM.
""")


# ============================================================
# TODO 1: Implement search_files
# ============================================================

print("\n--- TODO 1: Implement search_files ---\n")

print("  Implement a function that finds files matching a glob pattern")
print("  within a given directory using os.walk + fnmatch.\n")

# YOUR CODE HERE: Replace the body with a real implementation
def search_files(pattern, directory=WORKDIR):
    """
    Search for files matching a glob pattern in directory.

    Args:
        pattern: glob pattern (e.g., "*.py", "*.txt")
        directory: root directory to search in

    Returns:
        List of matching file paths (absolute)
    """
    # TODO: Use os.walk to traverse directory
    # TODO: Use fnmatch.fnmatch to match filenames against pattern
    # TODO: Return list of full paths
    return "___"


# Create test files for validation
write_file(os.path.join(WORKDIR, "app.py"), "print('hello')")
write_file(os.path.join(WORKDIR, "test_app.py"), "assert True")
write_file(os.path.join(WORKDIR, "README.md"), "# My App")
write_file(os.path.join(WORKDIR, "sub", "utils.py"), "def helper(): pass")

score1 = 0
checks_1 = []

result1 = search_files("*.py", WORKDIR)

if result1 == "___":
    checks_1.append(("Returns a list", "TODO"))
    checks_1.append(("Finds *.py files", "TODO"))
    checks_1.append(("Finds files in subdirectories", "TODO"))
else:
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

    paths_str = " ".join(py_files)
    if any("sub" in p for p in py_files):
        checks_1.append(("Finds files in subdirectories", "PASS"))
        score1 += 1
    else:
        checks_1.append(("Finds files in subdirectories", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2: Implement tool_dispatcher
# ============================================================

print("\n\n--- TODO 2: Implement tool_dispatcher ---\n")

print("  Build a dispatcher that routes tool calls to the correct function.")
print("  It should handle: read_file, write_file, search_files")
print("  Return an error message for unknown tools.\n")

# YOUR CODE HERE: Replace the body with a real implementation
def tool_dispatcher(tool_name, **kwargs):
    """
    Dispatch a tool call to the correct function.

    Args:
        tool_name: name of the tool to call
        **kwargs:  arguments to pass to the tool

    Returns:
        Result from the tool function, or error string
    """
    # TODO: Create a dict mapping tool names to functions
    # TODO: Look up tool_name in the dict
    # TODO: Call the function with **kwargs
    # TODO: Return error for unknown tools
    return "___"


score2 = 0
checks_2 = []

# Test dispatching write_file
r1 = tool_dispatcher("write_file", path=os.path.join(WORKDIR, "dispatched.txt"), content="via dispatcher")
if r1 == "___":
    checks_2.append(("Dispatches write_file", "TODO"))
    checks_2.append(("Dispatches read_file", "TODO"))
    checks_2.append(("Handles unknown tool", "TODO"))
else:
    if isinstance(r1, str) and "OK" in r1:
        checks_2.append(("Dispatches write_file", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Dispatches write_file (got: {r1})", "FAIL"))

    # Test dispatching read_file
    r2 = tool_dispatcher("read_file", path=os.path.join(WORKDIR, "dispatched.txt"))
    if isinstance(r2, str) and "via dispatcher" in r2:
        checks_2.append(("Dispatches read_file", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Dispatches read_file (got: {r2})", "FAIL"))

    # Test unknown tool
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
# TODO 3: Chain 3 tool calls
# ============================================================

print("\n\n--- TODO 3: Chain 3 Tool Calls ---\n")

print("  Simulate an agent performing a 3-step task:")
print("    1. Write a Python file using tool_dispatcher")
print("    2. Read it back using tool_dispatcher")
print("    3. Search for *.py files using tool_dispatcher\n")

# YOUR CODE HERE: Use tool_dispatcher for each step
# Step A: Write a file called "agent_output.py" with content "# Generated by agent\nprint('done')"
step_a_result = "___"

# Step B: Read the file back
step_b_result = "___"

# Step C: Search for all .py files
step_c_result = "___"

score3 = 0
checks_3 = []

if step_a_result == "___":
    checks_3.append(("Step A: write file", "TODO"))
    checks_3.append(("Step B: read file back", "TODO"))
    checks_3.append(("Step C: search for .py files", "TODO"))
else:
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
print(f"  Lab 02 Summary")
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
