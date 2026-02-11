#!/usr/bin/env python3
"""
Lab 03: MCP Server Skeleton — Code Generation

Learn the structure of an MCP server by generating a complete Python server
file from templates.  The generated file uses the FastMCP pattern.

No external packages required — standard library only.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/aidev-lab-11-03"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Anatomy of an MCP Server File                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Anatomy of an MCP Server File")
print("=" * 70)
print()
print("  A minimal MCP server using the FastMCP SDK has these parts:")
print()
print("  1. Imports        — from mcp.server.fastmcp import FastMCP")
print("  2. Server init    — mcp = FastMCP('server-name')")
print("  3. Tool defs      — @mcp.tool() decorated async functions")
print("  4. Resource defs  — @mcp.resource('uri') decorated functions")
print("  5. Prompt defs    — @mcp.prompt() decorated functions")
print("  6. Entry point    — mcp.run()")
print()
print("  Example tool:")
print('    @mcp.tool()')
print('    async def greet(name: str) -> str:')
print('        """Greet a user by name."""')
print('        return f"Hello, {name}!"')
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Template Strings for Code Generation                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Templates for Server Code Generation")
print("=" * 70)
print()

IMPORT_TEMPLATE = 'from mcp.server.fastmcp import FastMCP'

SERVER_INIT_TEMPLATE = 'mcp = FastMCP("{server_name}")'

TOOL_TEMPLATE = textwrap.dedent("""\
@mcp.tool()
async def {func_name}({params}) -> str:
    \"\"\"{description}\"\"\"
    # Tool implementation
    return "result"
""")

RESOURCE_TEMPLATE = textwrap.dedent("""\
@mcp.resource("{uri}")
async def {func_name}() -> str:
    \"\"\"{description}\"\"\"
    return "resource data"
""")

ENTRY_TEMPLATE = textwrap.dedent("""\
if __name__ == "__main__":
    mcp.run()
""")

print("  Templates loaded.  You will combine them in TODO 1.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Generate a Complete MCP Server File                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Generate a complete MCP server Python file")
print("=" * 70)
print()

server_name = "code-assistant"

tool_definitions = [
    {
        "func_name": "search_files",
        "params": "pattern: str, directory: str",
        "description": "Search for files matching a glob pattern.",
    },
    {
        "func_name": "count_lines",
        "params": "file_path: str",
        "description": "Count lines in a source file.",
    },
    {
        "func_name": "lint_check",
        "params": "file_path: str",
        "description": "Run a basic lint check on a Python file.",
    },
]

# TODO: Build the full server source string by combining the templates.
#
#   1. Start with the import line (IMPORT_TEMPLATE)
#   2. Add a blank line
#   3. Add the server init line using SERVER_INIT_TEMPLATE.format(server_name=server_name)
#   4. Add a blank line
#   5. For each tool in tool_definitions, add TOOL_TEMPLATE.format(**tool) + blank line
#   6. End with ENTRY_TEMPLATE
#
#   Join all parts with "\n".

generated_source = "___"  # Replace with the assembled source string

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
checks_1 = [
    isinstance(generated_source, str),
    "from mcp.server.fastmcp import FastMCP" in generated_source,
    f'FastMCP("{server_name}")' in generated_source,
    "@mcp.tool()" in generated_source,
    "async def search_files" in generated_source,
    "async def count_lines" in generated_source,
    "async def lint_check" in generated_source,
    "mcp.run()" in generated_source,
]
if all(checks_1):
    score += 1
    print("[PASS] Generated source contains all required elements")
else:
    failed = [i for i, c in enumerate(checks_1) if not c]
    print(f"[FAIL] Checks failed at indices: {failed}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Write the Generated File to Disk                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Write the generated server to disk")
print("=" * 70)
print()

output_path = os.path.join(WORKDIR, "my_server.py")

# TODO: Write generated_source to output_path.
#   Use open(output_path, "w") and write the content.

# ___  # Replace with file-writing code

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
if os.path.exists(output_path):
    with open(output_path) as f:
        content = f.read()
    if "FastMCP" in content and "@mcp.tool()" in content:
        score += 1
        print(f"[PASS] Server file written to {output_path}")
    else:
        print(f"[FAIL] File exists but content is incomplete")
else:
    print(f"[FAIL] File not found at {output_path}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Validate the Generated File                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Validate the generated file contents")
print("=" * 70)
print()

# TODO: Read the file back from output_path and verify it contains:
#   1. Exactly 3 occurrences of "@mcp.tool()"
#   2. The string 'mcp = FastMCP("code-assistant")'
#   3. The string "if __name__"
#
# Set validation_result to True if all checks pass, False otherwise.

validation_result = "___"  # Replace with True/False based on checks

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
if validation_result is True:
    score += 1
    print("[PASS] Generated file passes all validation checks")
else:
    print("[FAIL] validation_result should be True")
    print("       Hint: read the file, count '@mcp.tool()' occurrences")
print()

# ── Print generated file for reference ───────────────────────────────────────
if os.path.exists(output_path):
    print("-" * 70)
    print("Generated server file:")
    print("-" * 70)
    with open(output_path) as f:
        for i, line in enumerate(f, 1):
            print(f"  {i:3d} | {line}", end="")
    print()
    print("-" * 70)
    print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 03 Score: {score}/{total}")
print("=" * 70)
