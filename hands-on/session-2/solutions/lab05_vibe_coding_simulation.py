"""
Lab 05 Solution: Vibe Coding Simulation
==========================================
"""

import os
import shutil
import json
import re

WORKDIR = "/tmp/aidev-lab-02-05"

print("=" * 50)
print("  Lab 05: Vibe Coding Simulation (Solution)")
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


# ============================================================
# Step 2: Intent Parser Example
# ============================================================

print("\n\n--- Step 2: Intent Parser Example ---\n")

example_intent = {
    "app_type": "api",
    "features": ["authentication"],
    "language": "python",
}
print(f"  Parsed intent: {json.dumps(example_intent, indent=4)}")


# ============================================================
# TODO 1 Solution: Implement parse_intent
# ============================================================

print("\n\n--- TODO 1: Implement parse_intent ---\n")

def parse_intent(description):
    """Parse a natural-language app description into structured intent."""
    desc = description.lower()

    # Detect app type
    if "api" in desc or "rest" in desc:
        app_type = "api"
    elif "web" in desc or "dashboard" in desc:
        app_type = "web"
    elif "cli" in desc or "command" in desc:
        app_type = "cli"
    else:
        app_type = "script"

    # Detect features
    features = []
    if "auth" in desc:
        features.append("authentication")
    if "database" in desc or "db" in desc or "sql" in desc:
        features.append("database")
    if "cache" in desc or "caching" in desc:
        features.append("caching")
    if "log" in desc:
        features.append("logging")
    if "test" in desc:
        features.append("testing")

    # Detect language
    if "javascript" in desc or "js" in desc:
        language = "javascript"
    elif "typescript" in desc or "ts" in desc:
        language = "typescript"
    elif "java" in desc and "javascript" not in desc:
        language = "java"
    else:
        language = "python"

    return {
        "app_type": app_type,
        "features": features,
        "language": language,
    }


score1 = 0
checks_1 = []

r1 = parse_intent("Build a Python REST API with authentication and caching")

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
# TODO 2 Solution: Implement generate_file_structure
# ============================================================

print("\n\n--- TODO 2: Implement generate_file_structure ---\n")

def generate_file_structure(app_type, language="python"):
    """Generate a list of file paths for the given app type."""
    structures = {
        "api": [
            "main.py", "routes/__init__.py", "routes/api.py",
            "models/__init__.py", "models/schemas.py",
            "tests/test_api.py", "requirements.txt", "README.md",
        ],
        "web": [
            "app.py", "templates/index.html", "static/style.css",
            "tests/test_app.py", "requirements.txt", "README.md",
        ],
        "cli": [
            "cli.py", "commands/__init__.py", "commands/main.py",
            "tests/test_cli.py", "requirements.txt", "README.md",
        ],
        "script": [
            "main.py", "utils.py", "tests/test_main.py", "README.md",
        ],
    }
    return structures.get(app_type, structures["script"])


score2 = 0
checks_2 = []

r1 = generate_file_structure("api")
r2 = generate_file_structure("cli")

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
# TODO 3 Solution: Generate a class skeleton
# ============================================================

print("\n\n--- TODO 3: Generate a Class Skeleton ---\n")

def generate_class_skeleton(class_name, methods, description=""):
    """Generate Python source code for a class skeleton."""
    lines = []
    lines.append(f"class {class_name}:")
    if description:
        lines.append(f'    """{description}"""')
    lines.append("")
    lines.append("    def __init__(self):")
    lines.append("        pass")
    lines.append("")
    for method in methods:
        lines.append(f"    def {method}(self):")
        lines.append("        pass")
        lines.append("")
    return "\n".join(lines)


score3 = 0
checks_3 = []

r1 = generate_class_skeleton("UserService", ["create_user", "get_user", "delete_user"],
                              "Manages user CRUD operations")

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

try:
    compile(r1, "<string>", "exec")
    checks_3.append(("Valid Python syntax", "PASS"))
    score3 += 1
except SyntaxError as e:
    checks_3.append((f"Valid Python syntax (error: {e})", "FAIL"))

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
print(f"  Lab 05 Summary (Solution)")
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
