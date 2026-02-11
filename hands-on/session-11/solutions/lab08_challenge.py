#!/usr/bin/env python3
"""
Lab 08 Solution: Challenge — Complete MCP System

Build a full MCP system: a server with 3 tools, 2 resources, and 1 prompt
template, plus a client that discovers and exercises every capability.

No external packages required — standard library only.
"""

import os
import ast
import json
import shutil
import fnmatch
from typing import Any, Dict, List, Optional

WORKDIR = "/tmp/aidev-lab-11-08"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create sample project for tools/resources to operate on
proj = os.path.join(WORKDIR, "sample_project")
os.makedirs(os.path.join(proj, "src"), exist_ok=True)
os.makedirs(os.path.join(proj, "tests"), exist_ok=True)

with open(os.path.join(proj, "src", "app.py"), "w") as f:
    f.write("""\
import os
import sys

class AppServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        print(f"Starting on {self.host}:{self.port}")

def create_app():
    return AppServer("localhost", 8000)

if __name__ == "__main__":
    app = create_app()
    app.start()
""")

with open(os.path.join(proj, "src", "utils.py"), "w") as f:
    f.write("import json\n\ndef load_config(path):\n    with open(path) as f:\n        return json.load(f)\n")

with open(os.path.join(proj, "tests", "test_app.py"), "w") as f:
    f.write("def test_create_app():\n    assert True\n\ndef test_start():\n    assert True\n")

with open(os.path.join(proj, "config.json"), "w") as f:
    json.dump({"debug": True, "log_level": "INFO", "max_retries": 3}, f, indent=2)

with open(os.path.join(proj, "README.md"), "w") as f:
    f.write("# Sample Project\nA demo project for MCP challenge lab.\n")

score = 0
total = 0

print("=" * 70)
print("CHALLENGE: Build a Complete MCP System")
print("=" * 70)
print()
print("  You will build:")
print("    - 3 tools:     analyze_code, search_files, run_linter")
print("    - 2 resources: project_structure, config_file")
print("    - 1 prompt:    code_review_prompt")
print("    - A client workflow that exercises all capabilities")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Define 3 Tool Functions                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Define 3 tool functions")
print("=" * 70)
print()

def analyze_code(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file and return metrics.

    Args:
        file_path: Absolute path to a Python file

    Returns:
        Dict with: file, line_count, function_count, class_count, import_count
    """
    with open(file_path) as f:
        source = f.read()
    tree = ast.parse(source)
    function_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    class_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    import_count = sum(1 for node in ast.walk(tree)
                       if isinstance(node, (ast.Import, ast.ImportFrom)))
    line_count = len(source.splitlines())
    return {
        "file": os.path.basename(file_path),
        "line_count": line_count,
        "function_count": function_count,
        "class_count": class_count,
        "import_count": import_count,
    }


def search_files(pattern: str, directory: str) -> List[str]:
    """Search for files matching a glob pattern.

    Args:
        pattern: Glob pattern (e.g. '*.py')
        directory: Root directory to search

    Returns:
        Sorted list of relative paths matching the pattern
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                full = os.path.join(root, filename)
                rel = os.path.relpath(full, directory)
                matches.append(rel)
    return sorted(matches)


def run_linter(file_path: str) -> Dict[str, Any]:
    """Run basic lint checks on a Python file.

    Checks:
        - Lines longer than 79 characters
        - Missing docstrings on functions
        - Use of 'import *'

    Args:
        file_path: Path to a Python file

    Returns:
        Dict with: file, issues (list of issue dicts), issue_count
    """
    with open(file_path) as f:
        source = f.read()
    lines = source.splitlines()
    issues = []

    # Check line length
    for i, line in enumerate(lines, 1):
        if len(line) > 79:
            issues.append({
                "line": i,
                "rule": "line-too-long",
                "message": f"Line {i} is {len(line)} chars (max 79)",
            })

    # Check wildcard imports
    for i, line in enumerate(lines, 1):
        if "import *" in line:
            issues.append({
                "line": i,
                "rule": "wildcard-import",
                "message": f"Wildcard import on line {i}",
            })

    # Check missing docstrings
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            has_docstring = (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            )
            if not has_docstring:
                issues.append({
                    "line": node.lineno,
                    "rule": "missing-docstring",
                    "message": f"Function '{node.name}' missing docstring",
                })

    return {
        "file": os.path.basename(file_path),
        "issues": issues,
        "issue_count": len(issues),
    }


# ── Validate TODO 1 ─────────────────────────────────────────────────────────
# Test analyze_code
total += 1
try:
    app_path = os.path.join(proj, "src", "app.py")
    analysis = analyze_code(app_path)
    checks = [
        isinstance(analysis, dict),
        analysis.get("file") == "app.py",
        analysis.get("line_count") == 16,
        analysis.get("function_count") == 3,  # __init__, start, create_app
        analysis.get("class_count") == 1,      # AppServer
        analysis.get("import_count") == 2,     # os, sys
    ]
    if all(checks):
        score += 1
        print(f"[PASS] analyze_code: {analysis}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] analyze_code checks failed at indices: {failed}")
        print(f"       Got: {analysis}")
except Exception as e:
    print(f"[FAIL] analyze_code exception: {e}")

# Test search_files
total += 1
try:
    found = search_files("*.py", proj)
    expected = sorted(["src/app.py", "src/utils.py", "tests/test_app.py"])
    if isinstance(found, list) and sorted(found) == expected:
        score += 1
        print(f"[PASS] search_files: {found}")
    else:
        print(f"[FAIL] search_files expected {expected}, got {found}")
except Exception as e:
    print(f"[FAIL] search_files exception: {e}")

# Test run_linter
total += 1
try:
    lint = run_linter(app_path)
    checks = [
        isinstance(lint, dict),
        lint.get("file") == "app.py",
        isinstance(lint.get("issues"), list),
        isinstance(lint.get("issue_count"), int),
        any(i.get("rule") == "missing-docstring" for i in lint.get("issues", [])),
    ]
    if all(checks):
        score += 1
        print(f"[PASS] run_linter found {lint['issue_count']} issues")
    else:
        print(f"[FAIL] run_linter: {lint}")
except Exception as e:
    print(f"[FAIL] run_linter exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Define 2 Resource Functions                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Define 2 resource functions")
print("=" * 70)
print()

def project_structure() -> str:
    """Return the project directory tree as a formatted string.

    Lists all files recursively with indentation showing depth.
    Static resource: project://structure

    Returns:
        Formatted directory tree string
    """
    lines = []
    for root, dirs, files in os.walk(proj):
        depth = root.replace(proj, "").count(os.sep)
        indent = "  " * depth
        dirname = os.path.basename(root)
        lines.append(f"{indent}{dirname}/")
        sub_indent = "  " * (depth + 1)
        for f in sorted(files):
            lines.append(f"{sub_indent}{f}")
    return "\n".join(lines)


def config_file() -> str:
    """Read and return the project configuration.

    Static resource: config://project

    Returns:
        JSON string of config.json contents
    """
    config_path = os.path.join(proj, "config.json")
    with open(config_path) as f:
        return f.read()


# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    tree = project_structure()
    checks = [
        isinstance(tree, str),
        "app.py" in tree,
        "config.json" in tree,
        "test_app.py" in tree,
        "src" in tree,
    ]
    if all(checks):
        score += 1
        print("[PASS] project_structure resource:")
        for line in tree.split("\n")[:10]:
            print(f"       {line}")
    else:
        print(f"[FAIL] project_structure: {tree!r}")
except Exception as e:
    print(f"[FAIL] project_structure exception: {e}")

total += 1
try:
    cfg = config_file()
    parsed = json.loads(cfg)
    checks = [
        parsed.get("debug") is True,
        parsed.get("log_level") == "INFO",
        parsed.get("max_retries") == 3,
    ]
    if all(checks):
        score += 1
        print(f"[PASS] config_file resource: {cfg.strip()}")
    else:
        print(f"[FAIL] config_file: {cfg!r}")
except Exception as e:
    print(f"[FAIL] config_file exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Define 1 Prompt Template                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Define a code_review_prompt template")
print("=" * 70)
print()

def code_review_prompt(file_name: str, code: str, metrics: str) -> List[Dict[str, str]]:
    """Build a code review prompt with context.

    Creates a structured prompt that an LLM would use to review code,
    incorporating the file metrics and source code.

    Args:
        file_name: Name of the file being reviewed
        code: Source code content
        metrics: JSON string of code metrics

    Returns:
        List of message dicts with "role" and "content" keys
    """
    return [
        {
            "role": "system",
            "content": ("You are a senior code reviewer. Analyze the code for "
                        "quality, security, and maintainability issues."),
        },
        {
            "role": "user",
            "content": (f"Please review the following file:\n\n"
                        f"File: {file_name}\n"
                        f"Metrics: {metrics}\n\n"
                        f"```python\n{code}\n```\n\n"
                        f"Provide specific, actionable feedback."),
        },
    ]

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    prompt_msgs = code_review_prompt("app.py", "print('hello')", '{"lines": 1}')
    checks = [
        isinstance(prompt_msgs, list),
        len(prompt_msgs) == 2,
        prompt_msgs[0].get("role") == "system",
        "reviewer" in prompt_msgs[0].get("content", "").lower(),
        prompt_msgs[1].get("role") == "user",
        "app.py" in prompt_msgs[1].get("content", ""),
        "print('hello')" in prompt_msgs[1].get("content", ""),
        '{"lines": 1}' in prompt_msgs[1].get("content", ""),
    ]
    if all(checks):
        score += 1
        print("[PASS] code_review_prompt generates correct messages")
        print(f"       System: {prompt_msgs[0]['content'][:60]}...")
        print(f"       User:   {prompt_msgs[1]['content'][:60]}...")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Prompt checks failed at indices: {failed}")
        print(f"       Got: {prompt_msgs}")
except Exception as e:
    print(f"[FAIL] code_review_prompt exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Client Workflow                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Build a client workflow exercising all capabilities")
print("=" * 70)
print()

def run_full_workflow() -> Dict[str, Any]:
    """Execute a complete client workflow against the MCP server."""
    # Step 1 — Capabilities
    capabilities = {
        "tools": ["analyze_code", "search_files", "run_linter"],
        "resources": ["project://structure", "config://project"],
        "prompts": ["code_review_prompt"],
    }

    # Step 2 — Call each tool
    app_path = os.path.join(proj, "src", "app.py")
    tool_results = {
        "analyze_code": analyze_code(app_path),
        "search_files": search_files("*.py", proj),
        "run_linter": run_linter(app_path),
    }

    # Step 3 — Read each resource
    resource_results = {
        "project://structure": project_structure(),
        "config://project": config_file(),
    }

    # Step 4 — Use the prompt
    with open(app_path) as f:
        code_content = f.read()
    metrics_json = json.dumps(tool_results["analyze_code"])
    prompt_result = code_review_prompt("app.py", code_content, metrics_json)

    return {
        "capabilities": capabilities,
        "tool_results": tool_results,
        "resource_results": resource_results,
        "prompt_result": prompt_result,
        "total_steps": 4,
    }

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    report = run_full_workflow()
    checks = [
        isinstance(report, dict),
        # Capabilities
        len(report.get("capabilities", {}).get("tools", [])) == 3,
        len(report.get("capabilities", {}).get("resources", [])) == 2,
        len(report.get("capabilities", {}).get("prompts", [])) == 1,
        # Tool results
        "analyze_code" in report.get("tool_results", {}),
        "search_files" in report.get("tool_results", {}),
        "run_linter" in report.get("tool_results", {}),
        isinstance(report.get("tool_results", {}).get("search_files"), list),
        # Resource results
        "project://structure" in report.get("resource_results", {}),
        "config://project" in report.get("resource_results", {}),
        # Prompt
        isinstance(report.get("prompt_result"), list),
        len(report.get("prompt_result", [])) == 2,
        # Steps
        report.get("total_steps") == 4,
    ]
    if all(checks):
        score += 1
        print("[PASS] Full workflow completed successfully!")
        cap = report["capabilities"]
        print(f"       Tools:     {cap['tools']}")
        print(f"       Resources: {cap['resources']}")
        print(f"       Prompts:   {cap['prompts']}")
        tr = report["tool_results"]
        print(f"       analyze_code: {tr['analyze_code'].get('line_count', '?')} lines")
        print(f"       search_files: {len(tr['search_files'])} files found")
        print(f"       run_linter:   {tr['run_linter'].get('issue_count', '?')} issues")

        # Save full report
        out_path = os.path.join(WORKDIR, "challenge_report.json")
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"       Report saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Workflow checks failed at indices: {failed}")
        if isinstance(report, dict):
            print(f"       Keys: {list(report.keys())}")
        else:
            print(f"       Got: {report}")
except Exception as e:
    print(f"[FAIL] Workflow exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Challenge Lab 08 Score: {score}/{total}")
print("=" * 70)
if score == total:
    print("Congratulations! You completed the MCP Challenge!")
else:
    print(f"Keep going — {total - score} check(s) remaining.")
print("=" * 70)
