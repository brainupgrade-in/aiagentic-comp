"""
Lab 01 Solution: Code Quality Analysis Server

Learn to build a code quality analysis tool using Python's ast module.
This simulates an MCP server that performs lint and complexity analysis.

Key concepts:
- AST (Abstract Syntax Tree) parsing
- Cyclomatic complexity calculation
- Static analysis for common code issues

Uses only Python standard library (ast, json, os).
"""

import ast
import json
import os
import shutil
import textwrap

WORKDIR = "/tmp/aidev-lab-12-01"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: AST Module Basics ──────────────────────────────────────
print("=" * 70)
print("STEP 1: Python AST Module Basics")
print("=" * 70)

print("""
The `ast` module parses Python source code into a tree of nodes.

  Key functions and node types:
  ┌──────────────────────────┬──────────────────────────────────────┐
  │ Function / Node          │ Purpose                              │
  ├──────────────────────────┼──────────────────────────────────────┤
  │ ast.parse(source)        │ Parse source string into AST tree    │
  │ ast.walk(tree)           │ Iterate all nodes in the tree        │
  │ ast.FunctionDef          │ Regular function definition          │
  │ ast.AsyncFunctionDef     │ Async function definition            │
  │ ast.ClassDef             │ Class definition                     │
  │ ast.If / ast.For         │ Control flow nodes                   │
  │ ast.While / ast.Try      │ Loop and exception nodes             │
  │ ast.ExceptHandler        │ Individual except clause             │
  │ ast.BoolOp               │ Boolean operation (and / or)         │
  └──────────────────────────┴──────────────────────────────────────┘

  Example — counting classes in source code:

    tree = ast.parse(source_code)
    class_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
""")

# ── Step 2: Complexity Counting ────────────────────────────────────
print("=" * 70)
print("STEP 2: Cyclomatic Complexity Concept")
print("=" * 70)

print("""
Cyclomatic complexity counts the number of independent execution paths
through a function. Each branch point adds 1 to the base complexity of 1.

  Branch-contributing nodes:
  ┌────────────────────┬──────────────────────────────────────────┐
  │ AST Node           │ Why It Adds Complexity                   │
  ├────────────────────┼──────────────────────────────────────────┤
  │ ast.If             │ Conditional branch                       │
  │ ast.For            │ Loop (may or may not execute body)       │
  │ ast.While          │ Loop with condition                      │
  │ ast.ExceptHandler  │ Exception handling path                  │
  │ ast.With           │ Context manager (cleanup path)           │
  │ ast.BoolOp         │ Short-circuit evaluation (and/or)        │
  └────────────────────┴──────────────────────────────────────────┘

  A function with complexity > 10 is considered hard to test/maintain.
""")

# ── Sample code for testing ────────────────────────────────────────

SAMPLE_CODE = textwrap.dedent("""\
    import os

    def greet(name):
        return f"Hello, {name}"

    async def fetch_data(url):
        pass

    def process_items(items, threshold=10):
        results = []
        for item in items:
            if item > threshold:
                results.append(item)
            elif item == threshold:
                results.append(item * 2)
            else:
                try:
                    results.append(int(item))
                except (ValueError, TypeError):
                    pass
        return results

    class Analyzer:
        def run(self):
            pass

    def simple():
        return 42
""")

COMPLEX_CODE = textwrap.dedent("""\
    def overly_complex(a, b, c, d, e, f):
        if a:
            for x in b:
                if x > 0:
                    while c:
                        try:
                            pass
                        except Exception:
                            pass
        elif d and e:
            for y in f:
                if y:
                    pass

    def bare_except_func():
        try:
            pass
        except:
            pass

    def nested_deep():
        def level1():
            def level2():
                def level3():
                    pass
""")


# ── TODO 1: Count Functions ────────────────────────────────────────
print("=" * 70)
print("TODO 1: Implement count_functions(source_code)")
print("=" * 70)

print("""
Count the total number of function definitions in source code.
Include both regular functions (FunctionDef) and async functions
(AsyncFunctionDef). Do NOT count methods inside classes separately
from top-level functions — count ALL function definitions found
anywhere in the AST.
""")


def count_functions(source_code: str) -> int:
    """Count all FunctionDef and AsyncFunctionDef nodes in source code."""
    tree = ast.parse(source_code)
    count = sum(
        1 for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    )
    return count


# Validate TODO 1
total += 1
try:
    result = count_functions(SAMPLE_CODE)
    # greet, fetch_data, process_items, Analyzer.run, simple = 5
    if result == 5:
        print(f"  [PASS] count_functions returned {result} (expected 5)")
        score += 1
    else:
        print(f"  [FAIL] count_functions returned {result} (expected 5)")
except Exception as e:
    print(f"  [FAIL] count_functions raised: {e}")


# ── TODO 2: Calculate Complexity ───────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement calculate_complexity(source_code)")
print("=" * 70)

print("""
Calculate per-function cyclomatic complexity. For each FunctionDef or
AsyncFunctionDef in the source, walk its child nodes and count branch
points: If, For, While, ExceptHandler, With, BoolOp.

Return a dict mapping function_name -> complexity_score.
Base complexity for each function is 1 (a straight-line function scores 1).
""")


def calculate_complexity(source_code: str) -> dict:
    """Calculate cyclomatic complexity per function."""
    tree = ast.parse(source_code)
    complexities = {}

    branch_types = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With, ast.BoolOp)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            branch_count = sum(
                1 for child in ast.walk(node)
                if isinstance(child, branch_types)
            )
            complexities[node.name] = 1 + branch_count

    return complexities


# Validate TODO 2
total += 1
try:
    result = calculate_complexity(SAMPLE_CODE)
    # process_items: 1 + for(1) + if(1) + if(1) + try->except(1) = 5
    if isinstance(result, dict) and "process_items" in result and result["process_items"] >= 4:
        print(f"  [PASS] calculate_complexity['process_items'] = {result['process_items']} (>= 4)")
        score += 1
    else:
        print(f"  [FAIL] calculate_complexity returned: {result}")
except Exception as e:
    print(f"  [FAIL] calculate_complexity raised: {e}")

total += 1
try:
    result = calculate_complexity(SAMPLE_CODE)
    if isinstance(result, dict) and "greet" in result and result["greet"] == 1:
        print(f"  [PASS] calculate_complexity['greet'] = {result['greet']} (expected 1)")
        score += 1
    else:
        print(f"  [FAIL] greet complexity: {result.get('greet', 'MISSING')}")
except Exception as e:
    print(f"  [FAIL] calculate_complexity raised: {e}")


# ── TODO 3: Find Issues ───────────────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement find_issues(source_code)")
print("=" * 70)

print("""
Detect common code quality issues:

  1. Bare except — an ExceptHandler with handler.type is None
  2. Too many params — FunctionDef with > 5 args (check args.args length)
  3. Deep nesting — functions defined inside functions at depth > 2

Return a list of dicts, each with keys: "issue", "function", "detail".
""")


def find_issues(source_code: str) -> list:
    """Find code quality issues using AST analysis."""
    issues = []
    tree = ast.parse(source_code)

    # Track function nesting depth
    def _walk_for_nesting(node, depth=0, enclosing="<module>"):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                new_depth = depth + 1
                if new_depth > 2:
                    issues.append({
                        "issue": "deep_nesting",
                        "function": child.name,
                        "detail": f"Nesting depth {new_depth}",
                    })
                _walk_for_nesting(child, new_depth, child.name)
            else:
                _walk_for_nesting(child, depth, enclosing)

    _walk_for_nesting(tree)

    # Check for bare except and too many params
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            # Find enclosing function
            enclosing = "<module>"
            for func_node in ast.walk(tree):
                if isinstance(func_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    for child in ast.walk(func_node):
                        if child is node:
                            enclosing = func_node.name
                            break
            issues.append({
                "issue": "bare_except",
                "function": enclosing,
                "detail": "Bare except clause",
            })

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            param_count = len(node.args.args)
            if param_count > 5:
                issues.append({
                    "issue": "too_many_params",
                    "function": node.name,
                    "detail": f"{param_count} parameters",
                })

    return issues


# Validate TODO 3
total += 1
try:
    result = find_issues(COMPLEX_CODE)
    issue_types = [i["issue"] for i in result] if isinstance(result, list) else []
    if "bare_except" in issue_types:
        print(f"  [PASS] find_issues detected bare_except")
        score += 1
    else:
        print(f"  [FAIL] find_issues did not detect bare_except: {result}")
except Exception as e:
    print(f"  [FAIL] find_issues raised: {e}")

total += 1
try:
    result = find_issues(COMPLEX_CODE)
    issue_types = [i["issue"] for i in result] if isinstance(result, list) else []
    if "too_many_params" in issue_types:
        print(f"  [PASS] find_issues detected too_many_params")
        score += 1
    else:
        print(f"  [FAIL] find_issues did not detect too_many_params: {result}")
except Exception as e:
    print(f"  [FAIL] find_issues raised: {e}")

total += 1
try:
    result = find_issues(COMPLEX_CODE)
    issue_types = [i["issue"] for i in result] if isinstance(result, list) else []
    if "deep_nesting" in issue_types:
        print(f"  [PASS] find_issues detected deep_nesting")
        score += 1
    else:
        print(f"  [FAIL] find_issues did not detect deep_nesting: {result}")
except Exception as e:
    print(f"  [FAIL] find_issues raised: {e}")


# ── Write Report ──────────────────────────────────────────────────
print()
print("=" * 70)
print("Writing Quality Report")
print("=" * 70)

try:
    report = {
        "function_count": count_functions(SAMPLE_CODE) if callable(count_functions) else 0,
        "complexities": calculate_complexity(SAMPLE_CODE) if callable(calculate_complexity) else {},
        "issues": find_issues(COMPLEX_CODE) if callable(find_issues) else [],
    }
except Exception:
    report = {"function_count": 0, "complexities": {}, "issues": []}

report_path = os.path.join(WORKDIR, "quality_report.json")
with open(report_path, "w") as f:
    json.dump(report, f, indent=2, default=str)
print(f"  Report written to: {report_path}")

total += 1
if os.path.exists(report_path):
    with open(report_path) as f:
        data = json.load(f)
    if "function_count" in data and "complexities" in data and "issues" in data:
        print(f"  [PASS] quality_report.json has correct structure")
        score += 1
    else:
        print(f"  [FAIL] quality_report.json missing keys")
else:
    print(f"  [FAIL] quality_report.json not found")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 01 Score: {score}/{total}")
print("=" * 70)
