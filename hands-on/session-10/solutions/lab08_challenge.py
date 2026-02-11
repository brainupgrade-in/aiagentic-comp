"""
Lab 08 Challenge Solution: End-to-End Coding Agent Simulation
================================================================
"""

import os
import shutil
import json
import ast
import fnmatch
import math

WORKDIR = "/tmp/aidev-lab-10-08"

print("=" * 60)
print("  Challenge Solution: End-to-End Coding Agent Simulation")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# PROVIDED: Helper functions
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
# TODO 1 Solution: Tool Registry & Dispatcher
# ============================================================

print("\n--- TODO 1: Tool Registry & Dispatcher ---\n")

def review_code(code):
    """Analyse Python code and return a review dict."""
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"functions_count": 0, "issues": [f"SyntaxError: {e}"]}

    functions_count = 0
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions_count += 1
            # Check line count
            length = node.end_lineno - node.lineno + 1
            if length > 15:
                issues.append(f"{node.name} is {length} lines (max 15)")
            # Check parameter count
            param_count = len(node.args.args)
            if param_count > 4:
                issues.append(f"{node.name} has {param_count} parameters (max 4)")

    return {"functions_count": functions_count, "issues": issues}


tool_registry = {
    "read_file": read_file,
    "write_file": write_file,
    "search_files": search_files,
    "count_tokens": token_counter,
    "review_code": review_code,
}


def dispatch(tool_name, **kwargs):
    """Dispatch a tool call. Return error for unknown tools."""
    if tool_name not in tool_registry:
        return f"ERROR: Unknown tool: {tool_name}"
    return tool_registry[tool_name](**kwargs)


score1 = 0
checks_1 = []

test_review = review_code("def f(a, b, c, d, e):\n    pass\n")
if isinstance(test_review, dict) and "functions_count" in test_review:
    checks_1.append(("review_code works", "PASS"))
    score1 += 1
else:
    checks_1.append((f"review_code works (got {test_review})", "FAIL"))

if isinstance(tool_registry, dict) and len(tool_registry) >= 5:
    checks_1.append(("Registry has 5+ tools", "PASS"))
    score1 += 1
else:
    checks_1.append(("Registry has 5+ tools", "FAIL"))

test_dispatch = dispatch("write_file", path=os.path.join(WORKDIR, "test_dispatch.txt"), content="hello")
if isinstance(test_dispatch, str) and "OK" in test_dispatch:
    checks_1.append(("Dispatcher routes calls", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Dispatcher routes calls (got {test_dispatch})", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2 Solution: Parse Task & Create Plan
# ============================================================

print("\n\n--- TODO 2: Parse Task & Create Plan ---\n")

task_description = "Build a Python TODO list API with add, remove, and list operations"
print(f"  Task: \"{task_description}\"\n")

def create_plan(task):
    """Parse a task description and create an execution plan."""
    desc = task.lower()

    # Detect app type
    if "api" in desc or "rest" in desc:
        app_type = "api"
    elif "web" in desc or "dashboard" in desc:
        app_type = "web"
    elif "cli" in desc or "command" in desc:
        app_type = "cli"
    else:
        app_type = "script"

    # Detect language
    if "javascript" in desc or "js " in desc:
        language = "javascript"
    elif "typescript" in desc or "ts " in desc:
        language = "typescript"
    elif "java" in desc and "javascript" not in desc:
        language = "java"
    else:
        language = "python"

    # Generate file list
    file_structures = {
        "api": ["main.py", "models.py", "routes.py", "tests/test_main.py", "README.md"],
        "web": ["app.py", "templates/index.html", "static/style.css", "tests/test_app.py", "README.md"],
        "cli": ["cli.py", "commands.py", "tests/test_cli.py", "README.md"],
        "script": ["main.py", "utils.py", "tests/test_main.py", "README.md"],
    }
    files = file_structures.get(app_type, file_structures["script"])

    # Extract features from task
    feature_keywords = ["add", "remove", "list", "delete", "update", "create",
                        "search", "filter", "sort", "auth", "login", "get"]
    features = [kw for kw in feature_keywords if kw in desc]

    return {
        "app_type": app_type,
        "language": language,
        "files_to_create": files,
        "features": features,
    }


score2 = 0
checks_2 = []

plan = create_plan(task_description)

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

print(f"\n  Plan: {json.dumps(plan, indent=4)}")
print(f"\n  Score: {score2}/4")


# ============================================================
# TODO 3 Solution: Generate Code Files
# ============================================================

print("\n\n--- TODO 3: Generate Code Files ---\n")

def generate_code(plan_dict):
    """Generate Python source files based on the plan."""
    created = []
    app_features = plan_dict.get("features", ["run"])

    for filepath in plan_dict.get("files_to_create", []):
        full_path = os.path.join(WORKDIR, filepath)

        if filepath == "main.py":
            # Generate main app file with a class
            methods = "\n".join(
                f"    def {feat}(self, item=None):\n"
                f"        \"\"\"Handle {feat} operation.\"\"\"\n"
                f"        pass\n"
                for feat in app_features
            )
            content = (
                f'"""\nMain application module.\n'
                f'App type: {plan_dict.get("app_type", "unknown")}\n"""\n\n\n'
                f'class TodoApp:\n'
                f'    """TODO list application."""\n\n'
                f'    def __init__(self):\n'
                f'        self.items = []\n\n'
                f'{methods}\n'
                f'\nif __name__ == "__main__":\n'
                f'    app = TodoApp()\n'
                f'    print("App initialized")\n'
            )
        elif filepath == "models.py":
            content = (
                '"""Data models."""\n\n\n'
                'class TodoItem:\n'
                '    """Represents a single TODO item."""\n\n'
                '    def __init__(self, title, done=False):\n'
                '        self.title = title\n'
                '        self.done = done\n\n'
                '    def to_dict(self):\n'
                '        return {"title": self.title, "done": self.done}\n'
            )
        elif filepath == "routes.py":
            content = (
                '"""API route handlers."""\n\n\n'
                'def register_routes(app):\n'
                '    """Register all API routes."""\n'
                '    pass\n'
            )
        elif filepath.endswith("test_main.py"):
            content = (
                '"""Tests for main application."""\n\n\n'
                'def test_app_init():\n'
                '    """Test app initialises correctly."""\n'
                '    assert True  # placeholder\n\n\n'
                'def test_add_item():\n'
                '    """Test adding an item."""\n'
                '    assert True  # placeholder\n'
            )
        elif filepath == "README.md":
            content = (
                f'# {plan_dict.get("app_type", "App").upper()} Application\n\n'
                f'Features: {", ".join(app_features)}\n'
            )
        else:
            content = f"# {filepath}\n# Auto-generated\n"

        result = dispatch("write_file", path=full_path, content=content)
        if "OK" in str(result):
            created.append(full_path)
            print(f"    Created: {filepath}")

    return created


score3 = 0
checks_3 = []

created_files = generate_code(plan)

if isinstance(created_files, list) and len(created_files) >= 1:
    checks_3.append(("Files were created", "PASS"))
    score3 += 1
else:
    checks_3.append((f"Files were created (got {created_files})", "FAIL"))

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
# TODO 4 Solution: Review & Final Report
# ============================================================

print("\n\n--- TODO 4: Review & Final Report ---\n")

def agent_report(workdir):
    """Review all .py files and produce a comprehensive report."""
    py_files = search_files("*.py", workdir)
    reviews = []
    total_functions = 0
    total_issues = 0

    for filepath in py_files:
        content = read_file(filepath)
        if content.startswith("ERROR"):
            continue
        review = review_code(content)
        total_functions += review["functions_count"]
        total_issues += len(review["issues"])
        reviews.append({
            "file": filepath,
            "functions_count": review["functions_count"],
            "issues": review["issues"],
        })

    status = "success" if total_issues == 0 else "needs_review"

    return {
        "task": task_description,
        "files_created": py_files,
        "total_functions": total_functions,
        "total_issues": total_issues,
        "reviews": reviews,
        "status": status,
    }


score4 = 0
checks_4 = []

report = agent_report(WORKDIR)

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

report_path = os.path.join(WORKDIR, "agent-report.json")
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)
print(f"    Report saved to {report_path}")

print(f"\n  Report summary:")
print(f"    Files created:    {len(report.get('files_created', []))}")
print(f"    Total functions:  {report.get('total_functions', 0)}")
print(f"    Total issues:     {report.get('total_issues', 0)}")
print(f"    Status:           {report.get('status', '?')}")

for check, status_str in checks_4:
    print(f"    [{status_str}] {check}")

print(f"\n  Score: {score4}/3")


# ============================================================
# Final Summary
# ============================================================

total = score1 + score2 + score3 + score4
max_total = 3 + 4 + 2 + 3

print(f"\n\n{'='*60}")
print(f"  Challenge Solution Summary")
print(f"{'='*60}")
print(f"  Built a mini coding agent with:")
print(f"    - Tool registry + dispatcher   (TODO 1: {score1}/3)")
print(f"    - Task parsing + planning      (TODO 2: {score2}/4)")
print(f"    - Code generation              (TODO 3: {score3}/2)")
print(f"    - Review + reporting           (TODO 4: {score4}/3)")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
