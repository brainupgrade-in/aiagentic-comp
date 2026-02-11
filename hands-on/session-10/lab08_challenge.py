"""
Lab 08 Challenge: End-to-End Coding Agent Simulation
======================================================
Build a mini coding agent that combines everything from Session 10:
- Tool registry and dispatcher (Lab 01-02)
- Context management and token budgeting (Lab 03)
- Code generation from intent (Lab 05)
- AST-based code review (Lab 07)

The agent processes a natural-language task through:
  1. Register tools
  2. Parse the task into a plan
  3. Generate code files
  4. Review the generated code
  5. Produce a final report

No API key needed — pure Python standard library.
"""

import os
import shutil
import json
import ast
import fnmatch
import math

WORKDIR = "/tmp/aidev-lab-10-08"

print("=" * 60)
print("  Challenge: End-to-End Coding Agent Simulation")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# PROVIDED: Helper functions (from earlier labs)
# ============================================================

def read_file(path):
    """Read file contents."""
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"ERROR: File not found: {path}"
    except Exception as e:
        return f"ERROR: {e}"

def write_file(path, content):
    """Write content to file."""
    try:
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return f"OK: Wrote {len(content)} chars to {path}"
    except Exception as e:
        return f"ERROR: {e}"

def search_files(pattern, directory=WORKDIR):
    """Search for files matching a glob pattern."""
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                matches.append(os.path.join(root, filename))
    return matches

def token_counter(text):
    """Estimate token count."""
    words = text.split()
    if len(words) == 0:
        return 0
    return math.ceil(len(words) * 1.3)


# ============================================================
# TODO 1: Build the tool registry and dispatcher
# ============================================================

print("\n--- TODO 1: Tool Registry & Dispatcher ---\n")

print("  Create a tool_registry dict and a dispatch function.")
print("  The registry must include: read_file, write_file, search_files,")
print("  count_tokens (maps to token_counter), and review_code.\n")

# YOUR CODE HERE
# Step A: Define a review_code tool function
def review_code(code):
    """
    Analyse Python code and return a review dict with:
    - functions_count: number of function definitions
    - issues: list of issue strings (long functions > 15 lines, > 4 params)
    """
    # TODO: Parse with ast, walk tree, count functions,
    #       detect long functions (>15 lines) and too many params (>4)
    return "___"


# Step B: Create the tool registry
# tool_registry = { "read_file": read_file, "write_file": write_file, ... }
tool_registry = "___"


# Step C: Create the dispatcher
def dispatch(tool_name, **kwargs):
    """Dispatch a tool call. Return error for unknown tools."""
    # TODO: Look up tool_name in tool_registry, call with kwargs
    return "___"


score1 = 0
checks_1 = []

# Check review_code
test_review = review_code("def f(a, b, c, d, e):\n    pass\n")
if test_review == "___":
    checks_1.append(("review_code works", "TODO"))
else:
    if isinstance(test_review, dict) and "functions_count" in test_review:
        checks_1.append(("review_code works", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"review_code works (got {test_review})", "FAIL"))

# Check registry
if tool_registry == "___":
    checks_1.append(("Registry has 5 tools", "TODO"))
else:
    if isinstance(tool_registry, dict) and len(tool_registry) >= 5:
        checks_1.append(("Registry has 5+ tools", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"Registry has 5+ tools (got {len(tool_registry) if isinstance(tool_registry, dict) else '?'})", "FAIL"))

# Check dispatcher
test_dispatch = dispatch("write_file", path=os.path.join(WORKDIR, "test_dispatch.txt"), content="hello")
if test_dispatch == "___":
    checks_1.append(("Dispatcher routes calls", "TODO"))
else:
    if isinstance(test_dispatch, str) and "OK" in test_dispatch:
        checks_1.append(("Dispatcher routes calls", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"Dispatcher routes calls (got {test_dispatch})", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2: Parse task and create a plan
# ============================================================

print("\n\n--- TODO 2: Parse Task & Create Plan ---\n")

task_description = "Build a Python TODO list API with add, remove, and list operations"

print(f"  Task: \"{task_description}\"\n")

# YOUR CODE HERE
def create_plan(task):
    """
    Parse a task description and create an execution plan.

    Returns a dict with:
        "app_type": str (e.g., "api", "script", "cli")
        "language": str (e.g., "python")
        "files_to_create": list of file path strings
        "features": list of feature strings extracted from the task
    """
    # TODO: Detect app_type from keywords
    # TODO: Detect language
    # TODO: Generate file list based on app_type
    # TODO: Extract features (look for verbs/nouns: "add", "remove", "list", etc.)
    return "___"


score2 = 0
checks_2 = []

plan = create_plan(task_description)

if plan == "___":
    checks_2.append(("Returns a dict", "TODO"))
    checks_2.append(("Has app_type", "TODO"))
    checks_2.append(("Has files_to_create", "TODO"))
    checks_2.append(("Has features", "TODO"))
else:
    if isinstance(plan, dict):
        checks_2.append(("Returns a dict", "PASS"))
        score2 += 1
    else:
        checks_2.append(("Returns a dict", "FAIL"))

    if isinstance(plan, dict) and plan.get("app_type") == "api":
        checks_2.append(("app_type = 'api'", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"app_type = 'api' (got {plan.get('app_type') if isinstance(plan, dict) else plan})", "FAIL"))

    files = plan.get("files_to_create", []) if isinstance(plan, dict) else []
    if isinstance(files, list) and len(files) >= 2:
        checks_2.append(("Has files_to_create (2+)", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Has files_to_create (got {files})", "FAIL"))

    features = plan.get("features", []) if isinstance(plan, dict) else []
    if isinstance(features, list) and len(features) >= 2:
        checks_2.append(("Has features (2+)", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Has features (got {features})", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/4")


# ============================================================
# TODO 3: Generate code files
# ============================================================

print("\n\n--- TODO 3: Generate Code Files ---\n")

print("  Using the plan from TODO 2, generate Python source files.")
print("  Write each file to WORKDIR using the dispatch function.\n")

# YOUR CODE HERE
def generate_code(plan_dict):
    """
    Generate Python source files based on the plan.

    For each file in plan_dict["files_to_create"], generate appropriate
    skeleton code and write it to WORKDIR using dispatch("write_file", ...).

    The main file (e.g., main.py or app.py) should contain:
        - A class or functions matching the features
        - Proper Python syntax (must compile with ast.parse)

    Returns:
        list of file paths that were created
    """
    # TODO: For each file in the plan, generate appropriate content
    # TODO: Use dispatch("write_file", ...) to write each file
    # TODO: Return list of created file paths
    return "___"


score3 = 0
checks_3 = []

# Use a fallback plan if TODO 2 wasn't completed
if plan == "___":
    plan_for_gen = {
        "app_type": "api",
        "language": "python",
        "files_to_create": ["main.py", "tests/test_main.py", "README.md"],
        "features": ["add", "remove", "list"],
    }
else:
    plan_for_gen = plan

created_files = generate_code(plan_for_gen)

if created_files == "___":
    checks_3.append(("Files were created", "TODO"))
    checks_3.append(("Main file has valid Python", "TODO"))
else:
    if isinstance(created_files, list) and len(created_files) >= 1:
        checks_3.append(("Files were created", "PASS"))
        score3 += 1
    else:
        checks_3.append((f"Files were created (got {created_files})", "FAIL"))

    # Check that at least one .py file has valid syntax
    py_files = search_files("*.py", WORKDIR)
    valid_syntax = False
    for pf in py_files:
        content = read_file(pf)
        try:
            ast.parse(content)
            valid_syntax = True
            break
        except SyntaxError:
            pass

    if valid_syntax:
        checks_3.append(("Main file has valid Python", "PASS"))
        score3 += 1
    else:
        checks_3.append(("Main file has valid Python", "FAIL"))

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/2")


# ============================================================
# TODO 4: Review and produce final report
# ============================================================

print("\n\n--- TODO 4: Review & Final Report ---\n")

print("  Review all generated Python files and produce a final agent report.\n")

# YOUR CODE HERE
def agent_report(workdir):
    """
    Review all .py files in workdir and produce a comprehensive report.

    Returns a dict with:
        "task": str (the original task description)
        "files_created": list of file paths
        "total_functions": int (across all files)
        "total_issues": int (across all files)
        "reviews": list of per-file review dicts
        "status": "success" if no issues, "needs_review" otherwise
    """
    # TODO: Find all .py files in workdir
    # TODO: For each file, read it and run review_code
    # TODO: Aggregate results into the report
    return "___"


score4 = 0
checks_4 = []

report = agent_report(WORKDIR)

if report == "___":
    checks_4.append(("Report is a dict", "TODO"))
    checks_4.append(("Has files_created", "TODO"))
    checks_4.append(("Has status field", "TODO"))
else:
    if isinstance(report, dict):
        checks_4.append(("Report is a dict", "PASS"))
        score4 += 1
    else:
        checks_4.append(("Report is a dict", "FAIL"))

    fc = report.get("files_created", []) if isinstance(report, dict) else []
    if isinstance(fc, list) and len(fc) >= 1:
        checks_4.append(("Has files_created", "PASS"))
        score4 += 1
    else:
        checks_4.append((f"Has files_created (got {fc})", "FAIL"))

    status = report.get("status") if isinstance(report, dict) else None
    if status in ("success", "needs_review"):
        checks_4.append(("Has status field", "PASS"))
        score4 += 1
    else:
        checks_4.append((f"Has status field (got {status})", "FAIL"))

    # Save report
    if isinstance(report, dict):
        report_path = os.path.join(WORKDIR, "agent-report.json")
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"    Report saved to {report_path}")

for check, status in checks_4:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score4}/3")


# ============================================================
# Final Summary
# ============================================================

total = score1 + score2 + score3 + score4
max_total = 3 + 4 + 2 + 3

print(f"\n\n{'='*60}")
print(f"  Challenge Summary")
print(f"{'='*60}")
print(f"  You built a mini coding agent with:")
print(f"    - Tool registry + dispatcher (TODO 1)")
print(f"    - Task parsing + planning     (TODO 2)")
print(f"    - Code generation              (TODO 3)")
print(f"    - Review + reporting           (TODO 4)")
print(f"\n  TODO 1: {score1}/3  tool registry & dispatcher")
print(f"  TODO 2: {score2}/4  task parsing & planning")
print(f"  TODO 3: {score3}/2  code generation")
print(f"  TODO 4: {score4}/3  review & reporting")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
