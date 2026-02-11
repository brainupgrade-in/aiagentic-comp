"""
Lab 06: Tool Registry

Learn to build a dynamic tool registry that supports registration,
discovery (by query and tags), and routing of tool calls.

Key concepts:
- Registry pattern for tool management
- Discovery by text query and tag filtering
- Dynamic routing and invocation

Uses only Python standard library (json, os, fnmatch).
"""

import json
import os
import shutil

WORKDIR = "/tmp/aidev-lab-12-06"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: Registry Pattern ─────────────────────────────────────
print("=" * 70)
print("STEP 1: The Tool Registry Pattern")
print("=" * 70)

print("""
A tool registry is a central catalog of available tools/actions.
AI agents use registries to discover and invoke tools dynamically.

  Registry operations:
  ┌──────────────────┬──────────────────────────────────────────────┐
  │ Operation        │ Description                                  │
  ├──────────────────┼──────────────────────────────────────────────┤
  │ register         │ Add a tool with name, handler, description,  │
  │                  │ and tags                                     │
  │ discover         │ Search tools by query text and/or tags       │
  │ route            │ Look up a tool by name and call its handler  │
  │ list_all         │ Return all registered tool names             │
  │ get_schema       │ Return tool metadata (for LLM function call) │
  └──────────────────┴──────────────────────────────────────────────┘

  Internal storage (per tool):
    {
        "name": "analyze_code",
        "handler": <callable>,
        "description": "Analyze Python code for issues",
        "tags": ["analysis", "code_quality"]
    }
""")

# ── Step 2: Discovery and Routing ─────────────────────────────────
print("=" * 70)
print("STEP 2: Discovery and Routing Concepts")
print("=" * 70)

print("""
Discovery allows an agent to find relevant tools:

  By query (text search):
    registry.discover(query="analyze") → tools whose description
    contains "analyze" (case-insensitive)

  By tags:
    registry.discover(tags=["security"]) → tools that have ALL
    specified tags

  Combined:
    registry.discover(query="code", tags=["analysis"]) → must match
    BOTH the query and the tags

  Routing:
    registry.route("analyze_code", source="print('hi')")
    → Looks up "analyze_code" handler and calls it with kwargs
""")


# ── Sample tool handlers ──────────────────────────────────────────

def analyze_code_handler(source: str = "") -> dict:
    """Analyze code and return findings."""
    issues = []
    if "eval(" in source:
        issues.append("eval_usage")
    if "import os" in source:
        issues.append("os_import")
    return {"tool": "analyze_code", "issues": issues, "lines": source.count("\n") + 1}


def run_tests_handler(test_dir: str = "tests/") -> dict:
    """Run tests in the specified directory."""
    return {"tool": "run_tests", "test_dir": test_dir, "passed": 8, "failed": 1}


def format_code_handler(source: str = "", style: str = "pep8") -> dict:
    """Format code according to style guide."""
    return {"tool": "format_code", "style": style, "formatted": True}


def search_files_handler(pattern: str = "*", directory: str = ".") -> dict:
    """Search for files matching a pattern."""
    return {"tool": "search_files", "pattern": pattern, "directory": directory, "matches": []}


def generate_docs_handler(source: str = "") -> dict:
    """Generate documentation from source code."""
    return {"tool": "generate_docs", "sections": ["overview", "api", "examples"]}


# ── TODO 1: ToolRegistry Class with register ──────────────────────
print("=" * 70)
print("TODO 1: Implement ToolRegistry with register method")
print("=" * 70)

print("""
Create a ToolRegistry class with:

  __init__(self): Initialize an empty dict self._tools = {}

  register(self, name, handler, description="", tags=None):
    - Store a tool entry in self._tools[name] with keys:
      "name", "handler", "description", "tags" (default to empty list)
    - If name already exists, overwrite it
    - Return self (for method chaining)

  list_all(self):
    - Return a sorted list of all registered tool names

  get_schema(self, name):
    - Return a dict with "name", "description", "tags" for the tool
      (exclude handler — schema is for LLM consumption)
    - Return None if tool not found
""")


class ToolRegistry:
    """A registry for dynamically managing tools."""

    def __init__(self):
        # TODO: Initialize self._tools as empty dict
        self._tools = "___"

    def register(self, name: str, handler, description: str = "", tags: list = None) -> "ToolRegistry":
        # TODO: Store tool entry in self._tools[name]
        # TODO: Default tags to empty list if None
        # TODO: Return self for chaining
        return "___"

    def list_all(self) -> list:
        # TODO: Return sorted list of tool names
        return "___"

    def get_schema(self, name: str) -> dict:
        # TODO: Return schema dict without handler, or None if not found
        return "___"


# Validate TODO 1
total += 1
try:
    reg = ToolRegistry()
    reg.register("test_tool", lambda: None, "A test tool", ["test"])
    if "test_tool" in reg.list_all():
        print(f"  [PASS] ToolRegistry.register + list_all works")
        score += 1
    else:
        print(f"  [FAIL] 'test_tool' not in list_all: {reg.list_all()}")
except Exception as e:
    print(f"  [FAIL] ToolRegistry raised: {e}")

total += 1
try:
    reg = ToolRegistry()
    reg.register("a", lambda: None, "Tool A", ["x"]).register("b", lambda: None, "Tool B", ["y"])
    if reg.list_all() == ["a", "b"]:
        print(f"  [PASS] Method chaining works")
        score += 1
    else:
        print(f"  [FAIL] Chaining result: {reg.list_all()}")
except Exception as e:
    print(f"  [FAIL] Chaining raised: {e}")

total += 1
try:
    reg = ToolRegistry()
    reg.register("my_tool", lambda: None, "Desc", ["tag1"])
    schema = reg.get_schema("my_tool")
    if isinstance(schema, dict) and "handler" not in schema and schema.get("description") == "Desc":
        print(f"  [PASS] get_schema returns metadata without handler")
        score += 1
    else:
        print(f"  [FAIL] get_schema returned: {schema}")
except Exception as e:
    print(f"  [FAIL] get_schema raised: {e}")


# ── TODO 2: Discover Method ──────────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement discover(query, tags) method")
print("=" * 70)

print("""
Add a discover method to ToolRegistry:

  discover(self, query=None, tags=None):
    - If query is provided, filter tools whose description contains
      query (case-insensitive)
    - If tags is provided, filter tools that have ALL specified tags
    - If both are provided, tool must match BOTH criteria
    - If neither is provided, return all tools
    - Return a list of schema dicts (same format as get_schema)
""")


# Add discover method to the class — for the lab, students add it below
# (In the solution file, it's part of the class definition)

def _discover(self, query: str = None, tags: list = None) -> list:
    """Discover tools by query text and/or tags."""
    # TODO: Start with all tools
    # TODO: If query, filter by case-insensitive substring match in description
    # TODO: If tags, filter by ALL tags present in tool's tags
    # TODO: Return list of schema dicts
    results = "___"
    return results

ToolRegistry.discover = _discover


# Validate TODO 2
total += 1
try:
    reg = ToolRegistry()
    reg.register("analyze", analyze_code_handler, "Analyze Python code for issues", ["analysis", "code_quality"])
    reg.register("test", run_tests_handler, "Run tests in directory", ["testing"])
    reg.register("format", format_code_handler, "Format code according to style", ["code_quality", "formatting"])
    reg.register("search", search_files_handler, "Search for files matching pattern", ["search", "files"])
    reg.register("docs", generate_docs_handler, "Generate documentation from source", ["docs", "code_quality"])

    result = reg.discover(query="code")
    names = [r["name"] for r in result] if isinstance(result, list) else []
    if "analyze" in names and "format" in names:
        print(f"  [PASS] discover(query='code') found analyze and format")
        score += 1
    else:
        print(f"  [FAIL] Expected analyze, format in: {names}")
except Exception as e:
    print(f"  [FAIL] discover raised: {e}")

total += 1
try:
    result = reg.discover(tags=["code_quality"])
    names = [r["name"] for r in result] if isinstance(result, list) else []
    if len(names) == 3 and all(n in names for n in ["analyze", "format", "docs"]):
        print(f"  [PASS] discover(tags=['code_quality']) found 3 tools")
        score += 1
    else:
        print(f"  [FAIL] Expected [analyze, format, docs], got: {names}")
except Exception as e:
    print(f"  [FAIL] discover raised: {e}")

total += 1
try:
    result = reg.discover(query="code", tags=["analysis"])
    names = [r["name"] for r in result] if isinstance(result, list) else []
    if names == ["analyze"]:
        print(f"  [PASS] discover(query='code', tags=['analysis']) found only 'analyze'")
        score += 1
    else:
        print(f"  [FAIL] Expected ['analyze'], got: {names}")
except Exception as e:
    print(f"  [FAIL] discover raised: {e}")


# ── TODO 3: Route Method ─────────────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement route(tool_name, **kwargs) method")
print("=" * 70)

print("""
Add a route method to ToolRegistry:

  route(self, tool_name, **kwargs):
    - Look up the tool by name
    - If not found, return {"error": f"Tool '{tool_name}' not found"}
    - Call the handler with **kwargs
    - Return the handler's result
""")


def _route(self, tool_name: str, **kwargs):
    """Route a call to the named tool."""
    # TODO: Look up tool in self._tools
    # TODO: If not found, return error dict
    # TODO: Call handler with kwargs and return result
    result = "___"
    return result

ToolRegistry.route = _route


# Validate TODO 3
total += 1
try:
    result = reg.route("analyze", source="x = eval(input())")
    if isinstance(result, dict) and "eval_usage" in result.get("issues", []):
        print(f"  [PASS] route('analyze') called handler correctly")
        score += 1
    else:
        print(f"  [FAIL] route result: {result}")
except Exception as e:
    print(f"  [FAIL] route raised: {e}")

total += 1
try:
    result = reg.route("nonexistent")
    if isinstance(result, dict) and "error" in result:
        print(f"  [PASS] route('nonexistent') returns error dict")
        score += 1
    else:
        print(f"  [FAIL] Expected error dict, got: {result}")
except Exception as e:
    print(f"  [FAIL] route raised: {e}")

total += 1
try:
    result = reg.route("test", test_dir="my_tests/")
    if isinstance(result, dict) and result.get("test_dir") == "my_tests/":
        print(f"  [PASS] route passes kwargs to handler")
        score += 1
    else:
        print(f"  [FAIL] kwargs not passed: {result}")
except Exception as e:
    print(f"  [FAIL] route raised: {e}")


# ── TODO 4: Register and Exercise ─────────────────────────────────
print()
print("=" * 70)
print("TODO 4: Register 5 tools, discover by tag, route a call")
print("=" * 70)

print("""
Using the handlers defined above (analyze_code_handler, run_tests_handler,
format_code_handler, search_files_handler, generate_docs_handler):

  1. Create a fresh ToolRegistry
  2. Register all 5 tools with appropriate descriptions and tags
  3. Use discover to find all tools tagged "code_quality"
  4. Route a call to "analyze_code" with source containing "eval("

Store results in:
  discovered_tools = [...]  # list of schema dicts
  route_result = {...}      # result from routing analyze call
""")

# TODO: Create registry and register 5 tools
# TODO: Discover tools with tag "code_quality"
# TODO: Route a call to the analyze tool
discovered_tools = "___"
route_result = "___"


# Validate TODO 4
total += 1
try:
    if isinstance(discovered_tools, list) and len(discovered_tools) >= 2:
        print(f"  [PASS] Discovered {len(discovered_tools)} code_quality tools")
        score += 1
    else:
        print(f"  [FAIL] Expected >= 2 discovered tools: {discovered_tools}")
except Exception as e:
    print(f"  [FAIL] TODO 4 discovery raised: {e}")

total += 1
try:
    if isinstance(route_result, dict) and route_result.get("tool") == "analyze_code":
        print(f"  [PASS] Route result from analyze_code tool")
        score += 1
    else:
        print(f"  [FAIL] Expected analyze_code result: {route_result}")
except Exception as e:
    print(f"  [FAIL] TODO 4 routing raised: {e}")


# ── Write Registry State ─────────────────────────────────────────
print()
print("=" * 70)
print("Writing Registry State")
print("=" * 70)

try:
    registry_state = {
        "registered_tools": reg.list_all() if hasattr(reg, 'list_all') else [],
        "discovered_tools": discovered_tools if isinstance(discovered_tools, list) else [],
        "route_result": route_result if isinstance(route_result, dict) else {},
    }
except Exception:
    registry_state = {"error": "registry not configured"}

state_path = os.path.join(WORKDIR, "registry_state.json")
with open(state_path, "w") as f:
    json.dump(registry_state, f, indent=2, default=str)
print(f"  Registry state written to: {state_path}")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 06 Score: {score}/{total}")
print("=" * 70)
