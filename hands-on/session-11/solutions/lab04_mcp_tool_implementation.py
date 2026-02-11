#!/usr/bin/env python3
"""
Lab 04 Solution: MCP Tool Implementation — Typed Tool Functions

Build real tool functions that an MCP server would expose: file_search and
code_metrics.  Learn how JSON schemas are derived from type annotations.

No external packages required — standard library only.
"""

import os
import ast
import json
import shutil
import fnmatch
import inspect
from typing import Dict, List, Any, get_type_hints

WORKDIR = "/tmp/aidev-lab-11-04"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create sample files for tools to operate on
sample_dir = os.path.join(WORKDIR, "project")
os.makedirs(os.path.join(sample_dir, "src"), exist_ok=True)
os.makedirs(os.path.join(sample_dir, "tests"), exist_ok=True)

with open(os.path.join(sample_dir, "src", "main.py"), "w") as f:
    f.write("""\
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

class Logger:
    def log(self, message):
        print(message)

def main():
    calc = Calculator()
    print(calc.add(1, 2))

if __name__ == "__main__":
    main()
""")

with open(os.path.join(sample_dir, "src", "utils.py"), "w") as f:
    f.write("def helper():\n    pass\n")

with open(os.path.join(sample_dir, "tests", "test_main.py"), "w") as f:
    f.write("def test_add():\n    assert 1 + 1 == 2\n\ndef test_sub():\n    assert 3 - 1 == 2\n")

with open(os.path.join(sample_dir, "README.md"), "w") as f:
    f.write("# Sample Project\n")

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — How Tools Are Defined                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: How MCP Tools Are Defined")
print("=" * 70)
print()
print("  In MCP, each tool is a function with:")
print("    - A name       (derived from function name)")
print("    - A description (derived from docstring)")
print("    - Parameters   (derived from type annotations)")
print("    - A return type (usually str or dict)")
print()
print("  Example:")
print("    async def search_files(pattern: str, directory: str) -> list:")
print('        """Find files matching a glob pattern in a directory."""')
print("        ...")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — JSON Schema from Type Hints                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: JSON Schema Derived from Type Hints")
print("=" * 70)
print()
print("  Python type  -->  JSON Schema type")
print("  ──────────────────────────────────")
print("  str          -->  { type: 'string' }")
print("  int          -->  { type: 'integer' }")
print("  float        -->  { type: 'number' }")
print("  bool         -->  { type: 'boolean' }")
print("  list         -->  { type: 'array' }")
print("  dict         -->  { type: 'object' }")
print()
print("  The MCP SDK auto-generates inputSchema from annotations.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement file_search()                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement file_search(pattern, directory)")
print("=" * 70)
print()

def file_search(pattern: str, directory: str) -> List[str]:
    """Search for files matching a glob pattern in a directory tree.

    Args:
        pattern: Glob pattern to match (e.g. '*.py')
        directory: Root directory to search from

    Returns:
        List of matching file paths (relative to directory)
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, pattern):
                full = os.path.join(root, filename)
                rel = os.path.relpath(full, directory)
                matches.append(rel)
    return sorted(matches)

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    result = file_search("*.py", sample_dir)
    expected = sorted(["src/main.py", "src/utils.py", "tests/test_main.py"])
    if isinstance(result, list) and sorted(result) == expected:
        score += 1
        print(f"[PASS] file_search found: {result}")
    else:
        print(f"[FAIL] Expected {expected}")
        print(f"       Got {result}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Implement code_metrics()                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement code_metrics(file_path)")
print("=" * 70)
print()

def code_metrics(file_path: str) -> Dict[str, int]:
    """Analyze a Python file and return code metrics.

    Args:
        file_path: Path to a Python file

    Returns:
        Dict with keys: function_count, class_count, line_count
    """
    with open(file_path) as f:
        source = f.read()
    tree = ast.parse(source)
    functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    lines = len(source.splitlines())
    return {"function_count": functions, "class_count": classes, "line_count": lines}

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    main_py = os.path.join(sample_dir, "src", "main.py")
    result = code_metrics(main_py)
    checks = [
        isinstance(result, dict),
        result.get("function_count") == 4,
        result.get("class_count") == 2,
        result.get("line_count") == 16,
    ]
    if all(checks):
        score += 1
        print(f"[PASS] code_metrics returned: {result}")
    else:
        print(f"[FAIL] Expected function_count=4, class_count=2, line_count=16")
        print(f"       Got: {result}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Build a JSON Schema from Annotations                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Build a JSON schema for a tool function")
print("=" * 70)
print()

PYTHON_TO_JSON_TYPE = {
    str:   "string",
    int:   "integer",
    float: "number",
    bool:  "boolean",
    list:  "array",
    dict:  "object",
}

def build_tool_schema(func) -> Dict[str, Any]:
    """Build a JSON Schema (MCP inputSchema) from a function's type hints and docstring.

    Args:
        func: A typed Python function

    Returns:
        Dict in JSON Schema format with: name, description, inputSchema
    """
    hints = get_type_hints(func)
    params = list(inspect.signature(func).parameters.keys())
    properties = {}
    for p in params:
        py_type = hints.get(p, str)
        # Handle generic types like List[str] — fall back to the origin
        origin = getattr(py_type, "__origin__", None)
        if origin is not None:
            py_type = origin
        json_type = PYTHON_TO_JSON_TYPE.get(py_type, "string")
        properties[p] = {"type": json_type}

    doc = (func.__doc__ or "").strip().split("\n")[0].strip()

    return {
        "name": func.__name__,
        "description": doc,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": params,
        },
    }

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    schema = build_tool_schema(file_search)
    checks = [
        isinstance(schema, dict),
        schema.get("name") == "file_search",
        "description" in schema,
        schema.get("inputSchema", {}).get("type") == "object",
        "pattern" in schema.get("inputSchema", {}).get("properties", {}),
        "directory" in schema.get("inputSchema", {}).get("properties", {}),
        schema["inputSchema"]["properties"]["pattern"]["type"] == "string",
        schema["inputSchema"]["properties"]["directory"]["type"] == "string",
        sorted(schema["inputSchema"].get("required", [])) == ["directory", "pattern"],
    ]
    if all(checks):
        score += 1
        print("[PASS] Tool schema is correct")
        out_path = os.path.join(WORKDIR, "tool_schema.json")
        with open(out_path, "w") as f:
            json.dump(schema, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Schema checks failed at indices: {failed}")
        print(f"       Got: {json.dumps(schema, indent=2) if isinstance(schema, dict) else schema}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 04 Score: {score}/{total}")
print("=" * 70)
