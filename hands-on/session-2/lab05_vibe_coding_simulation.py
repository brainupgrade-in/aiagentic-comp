"""
Lab 05: Vibe Coding Simulation
=================================
Simulate the "vibe coding" workflow — going from a natural-language
description to file structure and generated code, without an LLM.

What you'll learn:
- Parsing intent from natural language descriptions
- Generating project file structures from app type
- Creating Python class skeletons from descriptions

No API key needed — pure Python standard library.
"""

import os
import shutil
import json
import re

WORKDIR = "/tmp/aidev-lab-02-05"

print("=" * 50)
print("  Lab 05: Vibe Coding Simulation")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: NL-to-App Flow
# ============================================================

print("\n--- Step 1: NL-to-App Flow ---\n")

flow_steps = [
    ("1. Parse Intent",       "Extract app type, features, language from NL description"),
    ("2. File Structure",     "Generate the list of files and directories to create"),
    ("3. Code Generation",    "Produce skeleton code for each file"),
    ("4. Refinement",         "Iterate based on user feedback or test results"),
]

print(f"  {'Step':<24} {'Description'}")
print(f"  {'-'*70}")
for step, desc in flow_steps:
    print(f"  {step:<24} {desc}")

print("""
  'Vibe coding' = describe what you want in plain English,
  let the AI figure out the rest. Works best with clear intent.
""")


# ============================================================
# Step 2: Simple Intent Parser Example
# ============================================================

print("\n--- Step 2: Intent Parser Example ---\n")

print("  Given: 'Build a Python REST API with user authentication'\n")

example_intent = {
    "app_type": "api",
    "features": ["authentication"],
    "language": "python",
}
print(f"  Parsed intent: {json.dumps(example_intent, indent=4)}")

print("""
  The parser looks for keywords:
    - App type:  'api', 'web app', 'cli', 'script', 'dashboard'
    - Features:  'auth', 'database', 'caching', 'logging', 'testing'
    - Language:  'python', 'javascript', 'typescript', 'java'
""")


# ============================================================
# TODO 1: Implement parse_intent
# ============================================================

print("\n--- TODO 1: Implement parse_intent ---\n")

print("  Parse a natural-language description into structured intent.\n")

# YOUR CODE HERE: Replace the body with a real implementation
def parse_intent(description):
    """
    Parse a natural-language app description into structured intent.

    Args:
        description: string like "Build a Python REST API with auth and caching"

    Returns:
        dict with keys:
            app_type: str - one of "api", "web", "cli", "script" (default "script")
            features: list[str] - detected features
            language: str - one of "python", "javascript", "typescript", "java" (default "python")
    """
    # TODO: Convert description to lowercase for matching
    # TODO: Detect app_type from keywords: "api"/"rest" -> "api", "web"/"dashboard" -> "web",
    #       "cli"/"command" -> "cli", else "script"
    # TODO: Detect features from keywords: "auth" -> "authentication",
    #       "database"/"db"/"sql" -> "database", "cache"/"caching" -> "caching",
    #       "log"/"logging" -> "logging", "test" -> "testing"
    # TODO: Detect language: "python", "javascript"/"js", "typescript"/"ts", "java"
    return "___"


score1 = 0
checks_1 = []

r1 = parse_intent("Build a Python REST API with authentication and caching")

if r1 == "___":
    checks_1.append(("Returns a dict", "TODO"))
    checks_1.append(("Detects app_type", "TODO"))
    checks_1.append(("Detects features", "TODO"))
    checks_1.append(("Detects language", "TODO"))
else:
    if isinstance(r1, dict):
        checks_1.append(("Returns a dict", "PASS"))
        score1 += 1
    else:
        checks_1.append(("Returns a dict", "FAIL"))

    if isinstance(r1, dict) and r1.get("app_type") == "api":
        checks_1.append(("Detects app_type='api'", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"Detects app_type='api' (got {r1.get('app_type') if isinstance(r1, dict) else r1})", "FAIL"))

    features = r1.get("features", []) if isinstance(r1, dict) else []
    if "authentication" in features and "caching" in features:
        checks_1.append(("Detects features", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"Detects features (got {features})", "FAIL"))

    if isinstance(r1, dict) and r1.get("language") == "python":
        checks_1.append(("Detects language='python'", "PASS"))
        score1 += 1
    else:
        checks_1.append((f"Detects language (got {r1.get('language') if isinstance(r1, dict) else r1})", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/4")


# ============================================================
# TODO 2: Implement generate_file_structure
# ============================================================

print("\n\n--- TODO 2: Implement generate_file_structure ---\n")

print("  Given an app type, return a list of files to create.\n")

# YOUR CODE HERE: Replace the body with a real implementation
def generate_file_structure(app_type, language="python"):
    """
    Generate a list of file paths for the given app type.

    Args:
        app_type: "api", "web", "cli", or "script"
        language: programming language (default "python")

    Returns:
        list[str] of file paths (relative)

    Expected structures:
        api:    ["main.py", "routes/__init__.py", "routes/api.py",
                 "models/__init__.py", "models/schemas.py",
                 "tests/test_api.py", "requirements.txt", "README.md"]
        web:    ["app.py", "templates/index.html", "static/style.css",
                 "tests/test_app.py", "requirements.txt", "README.md"]
        cli:    ["cli.py", "commands/__init__.py", "commands/main.py",
                 "tests/test_cli.py", "requirements.txt", "README.md"]
        script: ["main.py", "utils.py", "tests/test_main.py", "README.md"]
    """
    # TODO: Return the appropriate file list based on app_type
    return "___"


score2 = 0
checks_2 = []

r1 = generate_file_structure("api")
r2 = generate_file_structure("cli")

if r1 == "___":
    checks_2.append(("Returns list for 'api'", "TODO"))
    checks_2.append(("API has main.py + routes", "TODO"))
    checks_2.append(("Returns list for 'cli'", "TODO"))
else:
    if isinstance(r1, list) and len(r1) >= 4:
        checks_2.append(("Returns list for 'api'", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Returns list for 'api' (got {r1})", "FAIL"))

    r1_str = " ".join(r1) if isinstance(r1, list) else ""
    if "main.py" in r1_str and "route" in r1_str.lower():
        checks_2.append(("API has main.py + routes", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"API has main.py + routes (got {r1})", "FAIL"))

    if isinstance(r2, list) and len(r2) >= 3:
        checks_2.append(("Returns list for 'cli'", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Returns list for 'cli' (got {r2})", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3: Generate a Python file with a class skeleton
# ============================================================

print("\n\n--- TODO 3: Generate a Class Skeleton ---\n")

print("  Given a class name and a list of methods, generate a Python file")
print("  with a class skeleton (method stubs with 'pass').\n")

# YOUR CODE HERE: Replace the body with a real implementation
def generate_class_skeleton(class_name, methods, description=""):
    """
    Generate Python source code for a class skeleton.

    Args:
        class_name: name of the class (e.g., "UserService")
        methods: list of method name strings (e.g., ["create_user", "get_user"])
        description: optional class docstring

    Returns:
        str: Python source code with class definition and method stubs.
        Each method should have 'self' as first param and 'pass' as body.
        Include a docstring for the class if description is provided.
    """
    # TODO: Build a class definition string
    # TODO: Add docstring if description is provided
    # TODO: Add __init__(self) method
    # TODO: Add each method with (self) and pass body
    return "___"


score3 = 0
checks_3 = []

r1 = generate_class_skeleton("UserService", ["create_user", "get_user", "delete_user"],
                              "Manages user CRUD operations")

if r1 == "___":
    checks_3.append(("Contains class definition", "TODO"))
    checks_3.append(("Contains all methods", "TODO"))
    checks_3.append(("Valid Python syntax", "TODO"))
else:
    if "class UserService" in r1:
        checks_3.append(("Contains class definition", "PASS"))
        score3 += 1
    else:
        checks_3.append(("Contains class definition", "FAIL"))

    has_all_methods = all(f"def {m}" in r1 for m in ["create_user", "get_user", "delete_user"])
    if has_all_methods:
        checks_3.append(("Contains all methods", "PASS"))
        score3 += 1
    else:
        checks_3.append(("Contains all methods", "FAIL"))

    # Try to compile
    try:
        compile(r1, "<string>", "exec")
        checks_3.append(("Valid Python syntax", "PASS"))
        score3 += 1
    except SyntaxError as e:
        checks_3.append((f"Valid Python syntax (error: {e})", "FAIL"))

    # Write to file
    out_path = os.path.join(WORKDIR, "user_service.py")
    with open(out_path, "w") as f:
        f.write(r1)
    print(f"    Generated file: {out_path}")

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 4 + 3 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 05 Summary")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Vibe coding = NL description -> intent -> files -> code")
print(f"    2. Intent parsing extracts app_type, features, language from text")
print(f"    3. File structure and code skeletons can be generated from templates")
print(f"\n  TODO 1: {score1}/4 intent parser checks passed")
print(f"  TODO 2: {score2}/3 file structure checks passed")
print(f"  TODO 3: {score3}/3 class skeleton checks passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
