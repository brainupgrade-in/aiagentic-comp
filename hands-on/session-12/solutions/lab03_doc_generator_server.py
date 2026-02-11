"""
Lab 03 Solution: Documentation Generator Server

Learn to build a documentation generation tool using AST-based
docstring extraction and Markdown README generation.

Key concepts:
- Extracting docstrings from Python source via ast
- Detecting undocumented functions
- Generating structured Markdown documentation

Uses only Python standard library (ast, json, os, textwrap).
"""

import ast
import json
import os
import shutil
import textwrap

WORKDIR = "/tmp/aidev-lab-12-03"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: AST-Based Docstring Extraction ─────────────────────────
print("=" * 70)
print("STEP 1: Extracting Docstrings with AST")
print("=" * 70)

print("""
Python stores docstrings as the first statement in a function/class body.
The ast module provides `ast.get_docstring(node)` to extract them.

  Approach:
  ┌──────────────────────────────────────────────────────────────────┐
  │ 1. Parse source with ast.parse(source)                         │
  │ 2. Walk the tree for FunctionDef / AsyncFunctionDef / ClassDef │
  │ 3. Call ast.get_docstring(node) for each                       │
  │ 4. Returns the docstring string, or None if absent             │
  └──────────────────────────────────────────────────────────────────┘

  Example:

    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            doc = ast.get_docstring(node)
            print(f"{node.name}: {doc or 'NO DOCSTRING'}")
""")

# ── Step 2: README Template Structure ─────────────────────────────
print("=" * 70)
print("STEP 2: README Template Structure")
print("=" * 70)

print("""
A generated README should follow this structure:

  # Project Name

  Description paragraph.

  ## Functions

  ### `function_name(param1, param2)`

  Docstring text here.

  ### `another_function()`

  Docstring text here.

  ## Undocumented Functions

  - `missing_docs_func`
  - `another_missing`

  ---
  *Auto-generated documentation*
""")

# ── Sample source code ────────────────────────────────────────────

SAMPLE_SOURCE = textwrap.dedent('''\
    """
    Sample module for documentation generation.
    This module provides utility functions for data processing.
    """

    def fetch_data(url: str, timeout: int = 30) -> dict:
        """Fetch data from a remote URL.

        Args:
            url: The URL to fetch from.
            timeout: Request timeout in seconds.

        Returns:
            A dictionary containing the response data.
        """
        pass

    def transform_data(data: dict, format: str = "json") -> str:
        """Transform data into the specified format.

        Args:
            data: Input data dictionary.
            format: Output format (json, csv, xml).

        Returns:
            Formatted string representation.
        """
        pass

    def validate_input(data):
        pass

    def save_results(results, path):
        pass

    async def stream_data(source: str):
        """Stream data from the given source in chunks."""
        pass

    class DataProcessor:
        """A processor for batch data operations."""

        def process(self, items):
            """Process a list of items."""
            pass

        def cleanup(self):
            pass
''')


# ── TODO 1: Extract Docstrings ─────────────────────────────────────
print("=" * 70)
print("TODO 1: Implement extract_docstrings(source_code)")
print("=" * 70)

print("""
Parse source_code and extract docstrings for all functions, async
functions, and classes.

Return a list of tuples: [(name, docstring_or_None), ...]

Include:
  - Module-level docstring as ("__module__", docstring) if present
  - FunctionDef and AsyncFunctionDef nodes
  - ClassDef nodes (but not methods inside classes for this function)

Order: as they appear in the source (use ast.iter_child_nodes on the
module node, not ast.walk, to get top-level items only).
""")


def extract_docstrings(source_code: str) -> list:
    """Extract docstrings from all top-level definitions in source code."""
    results = []
    tree = ast.parse(source_code)

    # Check for module docstring
    module_doc = ast.get_docstring(tree)
    if module_doc is not None:
        results.append(("__module__", module_doc))

    # Iterate top-level nodes only
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            doc = ast.get_docstring(node)
            results.append((node.name, doc))

    return results


# Validate TODO 1
total += 1
try:
    result = extract_docstrings(SAMPLE_SOURCE)
    if isinstance(result, list) and len(result) >= 6:
        names = [r[0] for r in result]
        if "__module__" in names and "fetch_data" in names:
            print(f"  [PASS] extract_docstrings found {len(result)} items incl. module + fetch_data")
            score += 1
        else:
            print(f"  [FAIL] Missing __module__ or fetch_data in: {names}")
    else:
        print(f"  [FAIL] Expected >= 6 items, got: {result}")
except Exception as e:
    print(f"  [FAIL] extract_docstrings raised: {e}")

total += 1
try:
    result = extract_docstrings(SAMPLE_SOURCE)
    documented = [r for r in result if r[1] is not None]
    if len(documented) >= 4:
        print(f"  [PASS] extract_docstrings found {len(documented)} documented items")
        score += 1
    else:
        print(f"  [FAIL] Expected >= 4 documented items, got {len(documented)}")
except Exception as e:
    print(f"  [FAIL] extract_docstrings raised: {e}")


# ── TODO 2: Check Missing Docs ────────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement check_missing_docs(source_code)")
print("=" * 70)

print("""
Find all functions and classes that are missing docstrings.
This time, search ALL levels (use ast.walk), not just top-level.

Return a list of dicts:
  [{"name": <name>, "type": "function"|"async_function"|"class", "line": <lineno>}]

A definition is "missing" if ast.get_docstring(node) returns None.
""")


def check_missing_docs(source_code: str) -> list:
    """Find functions and classes without docstrings."""
    missing = []
    tree = ast.parse(source_code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if ast.get_docstring(node) is None:
                missing.append({"name": node.name, "type": "function", "line": node.lineno})
        elif isinstance(node, ast.AsyncFunctionDef):
            if ast.get_docstring(node) is None:
                missing.append({"name": node.name, "type": "async_function", "line": node.lineno})
        elif isinstance(node, ast.ClassDef):
            if ast.get_docstring(node) is None:
                missing.append({"name": node.name, "type": "class", "line": node.lineno})

    return missing


# Validate TODO 2
total += 1
try:
    result = check_missing_docs(SAMPLE_SOURCE)
    if isinstance(result, list):
        names = [r["name"] for r in result]
        if "validate_input" in names and "save_results" in names:
            print(f"  [PASS] check_missing_docs found validate_input and save_results")
            score += 1
        else:
            print(f"  [FAIL] Expected validate_input and save_results in: {names}")
    else:
        print(f"  [FAIL] check_missing_docs returned: {result}")
except Exception as e:
    print(f"  [FAIL] check_missing_docs raised: {e}")

total += 1
try:
    result = check_missing_docs(SAMPLE_SOURCE)
    if isinstance(result, list):
        names = [r["name"] for r in result]
        # cleanup method inside DataProcessor also has no docstring
        if "cleanup" in names:
            print(f"  [PASS] check_missing_docs found nested 'cleanup' method")
            score += 1
        else:
            print(f"  [FAIL] Expected 'cleanup' in missing docs: {names}")
    else:
        print(f"  [FAIL] check_missing_docs returned: {result}")
except Exception as e:
    print(f"  [FAIL] check_missing_docs raised: {e}")

total += 1
try:
    result = check_missing_docs(SAMPLE_SOURCE)
    if isinstance(result, list) and all("line" in r for r in result):
        print(f"  [PASS] check_missing_docs includes line numbers")
        score += 1
    else:
        print(f"  [FAIL] Missing 'line' key in results")
except Exception as e:
    print(f"  [FAIL] check_missing_docs raised: {e}")


# ── TODO 3: Generate README ───────────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement generate_readme(project_name, description, functions_list)")
print("=" * 70)

print("""
Generate a Markdown README string.

Parameters:
  - project_name: str — used as the heading
  - description: str — paragraph under the heading
  - functions_list: list of (name, docstring_or_None) tuples

Output format (as a string):
  # {project_name}

  {description}

  ## Functions

  ### `{name}`

  {docstring}

  (repeat for each function with a docstring)

  ## Undocumented

  - `{name}` (for each function without a docstring)

  ---
  *Auto-generated documentation*
""")


def generate_readme(project_name: str, description: str, functions_list: list) -> str:
    """Generate a Markdown README from function documentation."""
    lines = [f"# {project_name}", "", description, ""]

    # Documented functions
    lines.append("## Functions")
    lines.append("")
    for name, docstring in functions_list:
        if docstring is not None:
            lines.append(f"### `{name}`")
            lines.append("")
            lines.append(docstring)
            lines.append("")

    # Undocumented functions
    undocumented = [name for name, doc in functions_list if doc is None]
    if undocumented:
        lines.append("## Undocumented")
        lines.append("")
        for name in undocumented:
            lines.append(f"- `{name}`")
        lines.append("")

    lines.append("---")
    lines.append("*Auto-generated documentation*")
    lines.append("")

    return "\n".join(lines)


# Validate TODO 3
total += 1
try:
    funcs = [
        ("fetch_data", "Fetch data from URL."),
        ("transform_data", "Transform data."),
        ("validate_input", None),
    ]
    result = generate_readme("MyProject", "A test project.", funcs)
    if isinstance(result, str) and "# MyProject" in result:
        print(f"  [PASS] generate_readme includes project heading")
        score += 1
    else:
        print(f"  [FAIL] Missing heading in: {result[:100]}")
except Exception as e:
    print(f"  [FAIL] generate_readme raised: {e}")

total += 1
try:
    result = generate_readme("MyProject", "A test project.", funcs)
    if "### `fetch_data`" in result and "Fetch data from URL." in result:
        print(f"  [PASS] generate_readme includes documented functions")
        score += 1
    else:
        print(f"  [FAIL] Missing function docs in output")
except Exception as e:
    print(f"  [FAIL] generate_readme raised: {e}")

total += 1
try:
    result = generate_readme("MyProject", "A test project.", funcs)
    if "## Undocumented" in result and "`validate_input`" in result:
        print(f"  [PASS] generate_readme includes undocumented section")
        score += 1
    else:
        print(f"  [FAIL] Missing undocumented section")
except Exception as e:
    print(f"  [FAIL] generate_readme raised: {e}")


# ── Write Generated README ────────────────────────────────────────
print()
print("=" * 70)
print("Writing Generated README")
print("=" * 70)

try:
    docs = extract_docstrings(SAMPLE_SOURCE)
    if isinstance(docs, list):
        module_doc = ""
        func_docs = []
        for name, doc in docs:
            if name == "__module__":
                module_doc = doc or ""
            else:
                func_docs.append((name, doc))
        readme = generate_readme("Sample Module", module_doc, func_docs)
    else:
        readme = "# Documentation generation failed"
except Exception:
    readme = "# Documentation generation failed"

readme_path = os.path.join(WORKDIR, "README.md")
with open(readme_path, "w") as f:
    f.write(readme if isinstance(readme, str) else str(readme))
print(f"  README written to: {readme_path}")

total += 1
if os.path.exists(readme_path):
    with open(readme_path) as f:
        content = f.read()
    if len(content) > 50 and "# " in content:
        print(f"  [PASS] README.md generated ({len(content)} chars)")
        score += 1
    else:
        print(f"  [FAIL] README.md too short or malformed")
else:
    print(f"  [FAIL] README.md not found")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 03 Score: {score}/{total}")
print("=" * 70)
