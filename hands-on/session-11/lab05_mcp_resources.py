#!/usr/bin/env python3
"""
Lab 05: MCP Resources — Static and Dynamic Resources

Understand MCP resources: static resources with fixed URIs and dynamic
resources with URI templates.  Build a resource registry with resolution.

No external packages required — standard library only.
"""

import os
import re
import json
import shutil
from typing import Callable, Dict, Optional, Any

WORKDIR = "/tmp/aidev-lab-11-05"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create sample project structure
os.makedirs(os.path.join(WORKDIR, "project", "src"), exist_ok=True)
os.makedirs(os.path.join(WORKDIR, "project", "docs"), exist_ok=True)

with open(os.path.join(WORKDIR, "project", "src", "app.py"), "w") as f:
    f.write("print('hello world')\n")
with open(os.path.join(WORKDIR, "project", "src", "config.py"), "w") as f:
    f.write("DEBUG = True\nPORT = 8000\n")
with open(os.path.join(WORKDIR, "project", "docs", "guide.md"), "w") as f:
    f.write("# Guide\nWelcome to the guide.\n")
with open(os.path.join(WORKDIR, "project", "README.md"), "w") as f:
    f.write("# My Project\n")

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Static vs Dynamic Resources                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Static vs Dynamic Resources")
print("=" * 70)
print()
print("  Static resources have a fixed URI known at registration time:")
print('    @mcp.resource("config://app/settings")')
print("    async def get_settings() -> str: ...")
print()
print("  Dynamic resources use URI templates with placeholders:")
print('    @mcp.resource("file://{path}")')
print("    async def read_file(path: str) -> str: ...")
print()
print("  ┌──────────┬────────────────────────────┬──────────────────────┐")
print("  │ Type     │ URI Example                │ When to Use          │")
print("  ├──────────┼────────────────────────────┼──────────────────────┤")
print("  │ Static   │ config://app/settings      │ Known, fixed data    │")
print("  │ Dynamic  │ file://{path}              │ Parameterized access │")
print("  │ Dynamic  │ db://users/{user_id}       │ Entity lookups       │")
print("  └──────────┴────────────────────────────┴──────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — URI Template Patterns                                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: URI Template Patterns (RFC 6570 simplified)")
print("=" * 70)
print()
print("  MCP uses a simplified URI template syntax:")
print("    file://{path}          matches  file://src/app.py")
print("    db://users/{id}        matches  db://users/42")
print("    log://{service}/{date} matches  log://api/2025-01-15")
print()
print("  Placeholders are extracted as named parameters passed to the handler.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement a Static Resource                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement a static resource (project structure)")
print("=" * 70)
print()

project_dir = os.path.join(WORKDIR, "project")

def get_project_structure() -> str:
    """Return the project directory listing as a formatted string.

    Lists all files and directories in the project_dir, one per line,
    sorted alphabetically.  Directories should end with '/'.

    Returns:
        A newline-separated string of entries.
    """
    # TODO: Use os.listdir(project_dir) to get entries.
    #   For each entry, append '/' if it is a directory (os.path.isdir).
    #   Sort the list and join with newlines.
    #
    # Hint:
    #   entries = []
    #   for name in sorted(os.listdir(project_dir)):
    #       full = os.path.join(project_dir, name)
    #       entries.append(name + "/" if os.path.isdir(full) else name)
    #   return "\n".join(entries)

    return "___"  # Replace with your implementation

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    result = get_project_structure()
    expected_parts = ["README.md", "docs/", "src/"]
    checks = [
        isinstance(result, str),
        all(part in result for part in expected_parts),
        "src/" in result,
        "docs/" in result,
    ]
    if all(checks):
        score += 1
        print("[PASS] Static resource returns project structure:")
        for line in result.split("\n"):
            print(f"       {line}")
    else:
        print(f"[FAIL] Expected entries including {expected_parts}")
        print(f"       Got: {result!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Implement a Dynamic Resource                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement a dynamic resource (file reader)")
print("=" * 70)
print()

def read_file_resource(path: str) -> str:
    """Read a file from the project directory.

    This simulates a dynamic resource with URI template file://{path}.

    Args:
        path: Relative path within the project directory

    Returns:
        File contents as a string, or "ERROR: File not found" if missing.
    """
    # TODO: Build the full path by joining project_dir and path.
    #   If the file exists, read and return its contents.
    #   Otherwise return "ERROR: File not found".
    #
    # Hint:
    #   full_path = os.path.join(project_dir, path)
    #   if os.path.isfile(full_path):
    #       with open(full_path) as f:
    #           return f.read()
    #   return "ERROR: File not found"

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    content = read_file_resource("src/config.py")
    missing = read_file_resource("nonexistent.py")
    checks = [
        "DEBUG = True" in content,
        "PORT = 8000" in content,
        missing == "ERROR: File not found",
    ]
    if all(checks):
        score += 1
        print("[PASS] Dynamic resource reads files correctly")
        print(f"       config.py content: {content.strip()!r}")
    else:
        print(f"[FAIL] content={content!r}, missing={missing!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Resource Registry with URI Resolution                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Build a resource registry with URI resolution")
print("=" * 70)
print()

class ResourceRegistry:
    """Registry that maps URI patterns to handler functions."""

    def __init__(self):
        self._static: Dict[str, Callable] = {}
        self._dynamic: list = []  # list of (regex, param_names, handler)

    def register_static(self, uri: str, handler: Callable):
        """Register a static resource with a fixed URI."""
        self._static[uri] = handler

    def register_dynamic(self, uri_template: str, handler: Callable):
        """Register a dynamic resource with a URI template.

        Converts a template like 'file://{path}' into a regex pattern
        and stores the parameter names for extraction.
        """
        # TODO: Convert the URI template into a regex.
        #   1. Find all {param} placeholders using re.findall(r'\{(\w+)\}', uri_template)
        #   2. Replace each {param} with a named capture group: (?P<param>.+)
        #   3. Compile the regex and store (regex, param_names, handler)
        #
        # Hint:
        #   param_names = re.findall(r'\{(\w+)\}', uri_template)
        #   pattern = uri_template
        #   for name in param_names:
        #       pattern = pattern.replace("{" + name + "}", f"(?P<{name}>.+)")
        #   regex = re.compile(f"^{pattern}$")
        #   self._dynamic.append((regex, param_names, handler))

        pass  # Replace with your implementation

    def resolve(self, uri: str) -> Optional[str]:
        """Resolve a URI to a resource value.

        Checks static resources first, then tries dynamic patterns.

        Returns:
            The resource value (string), or None if no match.
        """
        # TODO:
        #   1. Check self._static for an exact match — if found, call handler()
        #   2. Loop through self._dynamic — try regex.match(uri)
        #      If a match is found, extract named groups and call handler(**groups)
        #   3. Return None if nothing matches
        #
        # Hint:
        #   if uri in self._static:
        #       return self._static[uri]()
        #   for regex, param_names, handler in self._dynamic:
        #       m = regex.match(uri)
        #       if m:
        #           return handler(**m.groupdict())
        #   return None

        return "___"  # Replace with your implementation

# Build and populate the registry
registry = ResourceRegistry()
registry.register_static("project://structure", get_project_structure)
registry.register_dynamic("file://{path}", read_file_resource)

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    # Test static resolution
    static_result = registry.resolve("project://structure")
    # Test dynamic resolution
    dynamic_result = registry.resolve("file://src/app.py")
    # Test miss
    miss_result = registry.resolve("unknown://something")

    checks = [
        static_result is not None and "src/" in static_result,
        dynamic_result is not None and "hello world" in dynamic_result,
        miss_result is None,
    ]
    if all(checks):
        score += 1
        print("[PASS] Resource registry resolves URIs correctly")
        print(f"       Static:  project://structure -> entries found")
        print(f"       Dynamic: file://src/app.py   -> {dynamic_result.strip()!r}")
        print(f"       Miss:    unknown://something  -> None")
    else:
        print(f"[FAIL] static={static_result!r}, dynamic={dynamic_result!r}, miss={miss_result!r}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ── Save registry info ──────────────────────────────────────────────────────
registry_info = {
    "static_uris": list(registry._static.keys()) if hasattr(registry, '_static') else [],
    "dynamic_count": len(registry._dynamic) if hasattr(registry, '_dynamic') else 0,
}
out_path = os.path.join(WORKDIR, "registry.json")
with open(out_path, "w") as f:
    json.dump(registry_info, f, indent=2)
print(f"Registry info saved to {out_path}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 05 Score: {score}/{total}")
print("=" * 70)
