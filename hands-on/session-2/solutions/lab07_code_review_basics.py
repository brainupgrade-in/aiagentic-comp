"""
Lab 07 Solution: Code Review Basics
======================================
"""

import os
import shutil
import json
import ast

WORKDIR = "/tmp/aidev-lab-02-07"

print("=" * 50)
print("  Lab 07: Code Review Basics (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Python ast Module Basics
# ============================================================

print("\n--- Step 1: Python ast Module Basics ---\n")

sample_code = '''
def greet(name):
    """Say hello."""
    return f"Hello, {name}!"

def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        return x * y
'''

tree = ast.parse(sample_code)

print("  Sample code parsed. Top-level nodes:")
for node in ast.iter_child_nodes(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"    FunctionDef: {node.name}  (line {node.lineno})")
    elif isinstance(node, ast.ClassDef):
        print(f"    ClassDef: {node.name}  (line {node.lineno})")
        for child in ast.iter_child_nodes(node):
            if isinstance(child, ast.FunctionDef):
                print(f"      FunctionDef: {child.name}  (line {child.lineno})")


# ============================================================
# Step 2: Detecting Issues with AST
# ============================================================

print("\n\n--- Step 2: Detecting Issues with AST ---\n")

checks_table = [
    ("Long functions",       "> 20 lines",       "Hard to read and test"),
    ("Too many parameters",  "> 5 params",        "Complex interface, consider refactoring"),
    ("No docstring",         "missing docstring", "Undocumented public function"),
    ("Deeply nested",        "> 3 nesting levels","Cyclomatic complexity concern"),
    ("Global variables",     "module-level var",  "Shared mutable state"),
]

print(f"  {'Check':<24} {'Threshold':<20} {'Why It Matters'}")
print(f"  {'-'*70}")
for check, threshold, why in checks_table:
    print(f"  {check:<24} {threshold:<20} {why}")


# ============================================================
# TODO 1 Solution: Implement count_functions
# ============================================================

print("\n\n--- TODO 1: Implement count_functions ---\n")

def count_functions(code):
    """Count all function definitions in Python source code."""
    tree = ast.parse(code)
    count = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            count += 1
    return count


test_code_1 = '''
def foo():
    pass

def bar():
    pass

class Baz:
    def method1(self):
        pass
    def method2(self):
        pass
'''

score1 = 0
checks_1 = []

r1 = count_functions(test_code_1)

if isinstance(r1, int) and r1 == 4:
    checks_1.append(("Counts all 4 functions/methods", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Counts all 4 functions/methods (got {r1})", "FAIL"))

r2 = count_functions("x = 1\ny = 2\n")
if isinstance(r2, int) and r2 == 0:
    checks_1.append(("Returns 0 for code with no functions", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Returns 0 for code with no functions (got {r2})", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/2")


# ============================================================
# TODO 2 Solution: Implement find_long_functions
# ============================================================

print("\n\n--- TODO 2: Implement find_long_functions ---\n")

def find_long_functions(code, max_lines=20):
    """Find functions longer than max_lines."""
    tree = ast.parse(code)
    long_funcs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            length = node.end_lineno - node.lineno + 1
            if length > max_lines:
                long_funcs.append({
                    "name": node.name,
                    "lines": length,
                    "start_line": node.lineno,
                })
    return long_funcs


test_code_2 = "def short_func():\n    pass\n\n"
test_code_2 += "def long_func():\n"
for i in range(25):
    test_code_2 += f"    x_{i} = {i}\n"
test_code_2 += "    return x_0\n"

score2 = 0
checks_2 = []

r1 = find_long_functions(test_code_2, max_lines=20)

if isinstance(r1, list):
    checks_2.append(("Returns a list", "PASS"))
    score2 += 1
else:
    checks_2.append(("Returns a list", "FAIL"))

found_names = [f["name"] for f in r1] if isinstance(r1, list) else []
if "long_func" in found_names:
    checks_2.append(("Finds long_func", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Finds long_func (got {found_names})", "FAIL"))

if "short_func" not in found_names:
    checks_2.append(("Skips short_func", "PASS"))
    score2 += 1
else:
    checks_2.append(("Skips short_func", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3 Solution: Generate a review report
# ============================================================

print("\n\n--- TODO 3: Generate a Review Report ---\n")

review_code = '''
def process_data(data, config, logger, db, cache, extra):
    """Process the incoming data."""
    result = []
    for item in data:
        if item.get("active"):
            if item.get("type") == "A":
                val = item["value"] * config["multiplier"]
                result.append(val)
            elif item.get("type") == "B":
                val = item["value"] + config["offset"]
                result.append(val)
    return result

def helper():
    return 42

class DataService:
    def run(self):
        pass
    def stop(self):
        pass
'''

# Build the report
functions_count = count_functions(review_code)
long_funcs = find_long_functions(review_code, max_lines=10)

issues = []

# Check for long functions
for lf in long_funcs:
    issues.append(f"{lf['name']} is {lf['lines']} lines (max 10)")

# Check for too many parameters
tree = ast.parse(review_code)
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        param_count = len(node.args.args)
        if param_count > 5:
            issues.append(f"{node.name} has {param_count} parameters (max 5)")

review_report = {
    "file": "review_sample.py",
    "functions_count": functions_count,
    "issues_count": len(issues),
    "issues": issues,
}

score3 = 0
checks_3 = []

if isinstance(review_report, dict):
    checks_3.append(("Report is a dict", "PASS"))
    score3 += 1
else:
    checks_3.append(("Report is a dict", "FAIL"))

fc = review_report.get("functions_count")
if fc == 4:
    checks_3.append(("functions_count = 4", "PASS"))
    score3 += 1
else:
    checks_3.append((f"functions_count = 4 (got {fc})", "FAIL"))

issues = review_report.get("issues", [])
if len(issues) >= 1 and any("process_data" in str(i) for i in issues):
    checks_3.append(("Issues mention process_data", "PASS"))
    score3 += 1
else:
    checks_3.append((f"Issues mention process_data (got {issues})", "FAIL"))

report_path = os.path.join(WORKDIR, "review-report.json")
with open(report_path, "w") as f:
    json.dump(review_report, f, indent=2)
print(f"    Report saved to {report_path}")

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 2 + 3 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 07 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. ast.parse() + ast.walk() = programmatic code analysis")
print(f"    2. AI agents use AST analysis for automated code review")
print(f"    3. Structured reports capture function counts, line lengths, parameter counts")
print(f"\n  TODO 1: {score1}/2 count_functions checks passed")
print(f"  TODO 2: {score2}/3 find_long_functions checks passed")
print(f"  TODO 3: {score3}/3 review report checks passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
