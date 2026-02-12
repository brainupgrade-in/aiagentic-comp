"""
Lab 03 Solution: Context Management
======================================
"""

import os
import shutil
import json
import math

WORKDIR = "/tmp/aidev-lab-02-03"

print("=" * 50)
print("  Lab 03: Context Management (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Token Budget Allocation
# ============================================================

print("\n--- Step 1: Token Budget Allocation ---\n")

budget_table = [
    ("System prompt",       "15%",  "Agent instructions, persona, tool definitions"),
    ("User request",        "10%",  "The current task description"),
    ("Project context",     "40%",  "CLAUDE.md, relevant source files, configs"),
    ("Conversation history","20%",  "Previous turns, tool results"),
    ("Reserved for output", "15%",  "Room for the LLM to generate its response"),
]

print(f"  {'Component':<25} {'Budget':<8} {'Contents'}")
print(f"  {'-'*80}")
for component, budget, contents in budget_table:
    print(f"  {component:<25} {budget:<8} {contents}")

print("""
  Key insight: Project context (40%) is the largest bucket.
  The agent must CHOOSE which files to include.
""")


# ============================================================
# Step 2: File Relevance Scoring
# ============================================================

print("\n--- Step 2: File Relevance Scoring ---\n")

example_files = [
    {"path": "src/auth/login.py",       "size_tokens": 450,  "score": 8},
    {"path": "src/auth/middleware.py",   "size_tokens": 320,  "score": 6},
    {"path": "tests/test_login.py",     "size_tokens": 280,  "score": 5},
    {"path": "src/models/user.py",      "size_tokens": 200,  "score": 4},
    {"path": "README.md",               "size_tokens": 150,  "score": 2},
    {"path": "setup.py",                "size_tokens": 80,   "score": 1},
]

print(f"  {'File':<30} {'Tokens':<10} {'Relevance Score'}")
print(f"  {'-'*55}")
for f in example_files:
    print(f"  {f['path']:<30} {f['size_tokens']:<10} {f['score']}")


# ============================================================
# TODO 1 Solution: Implement token_counter
# ============================================================

print("\n\n--- TODO 1: Implement token_counter ---\n")

def token_counter(text):
    """
    Estimate the number of tokens in a text string.
    Approximation: tokens = number_of_words * 1.3 (rounded up to int).
    """
    words = text.split()
    if len(words) == 0:
        return 0
    return math.ceil(len(words) * 1.3)


score1 = 0
checks_1 = []

r1 = token_counter("Hello world")
r2 = token_counter("The quick brown fox jumps over the lazy dog")
r3 = token_counter("")

if isinstance(r1, int) and r1 == 3:
    checks_1.append(("Two words -> 3 tokens", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Two words -> 3 tokens (got {r1})", "FAIL"))

if isinstance(r2, int) and r2 == 12:
    checks_1.append(("Nine words -> 12 tokens", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Nine words -> 12 tokens (got {r2})", "FAIL"))

if isinstance(r3, int) and r3 == 0:
    checks_1.append(("Empty string -> 0", "PASS"))
    score1 += 1
else:
    checks_1.append((f"Empty string -> 0 (got {r3})", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2 Solution: Implement priority_file_selector
# ============================================================

print("\n\n--- TODO 2: Implement priority_file_selector ---\n")

def priority_file_selector(files, token_budget):
    """Select most relevant files within a token budget."""
    sorted_files = sorted(files, key=lambda f: f["score"], reverse=True)
    selected = []
    used_tokens = 0
    for f in sorted_files:
        if used_tokens + f["size_tokens"] <= token_budget:
            selected.append(f)
            used_tokens += f["size_tokens"]
    return selected


score2 = 0
checks_2 = []

test_files = [
    {"path": "a.py", "size_tokens": 300, "score": 5},
    {"path": "b.py", "size_tokens": 200, "score": 8},
    {"path": "c.py", "size_tokens": 400, "score": 3},
    {"path": "d.py", "size_tokens": 100, "score": 7},
]

r1 = priority_file_selector(test_files, 500)

if isinstance(r1, list):
    checks_2.append(("Returns a list", "PASS"))
    score2 += 1
else:
    checks_2.append(("Returns a list", "FAIL"))

selected_paths = [f["path"] for f in r1] if isinstance(r1, list) else []
if len(selected_paths) >= 2 and selected_paths[0] == "b.py":
    checks_2.append(("Selects highest-score files first", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Selects highest-score files first (got {selected_paths})", "FAIL"))

total_tokens = sum(f["size_tokens"] for f in r1) if isinstance(r1, list) else 0
if total_tokens <= 500:
    checks_2.append(("Respects token budget", "PASS"))
    score2 += 1
else:
    checks_2.append((f"Respects token budget (total={total_tokens}, budget=500)", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3 Solution: Generate a CLAUDE.md file
# ============================================================

print("\n\n--- TODO 3: Generate a CLAUDE.md ---\n")

project_meta = {
    "name": "weather-api",
    "language": "Python",
    "framework": "FastAPI",
    "description": "A weather forecast API with caching and rate limiting",
    "commands": {
        "install": "pip install -r requirements.txt",
        "run": "uvicorn main:app --reload --port 8000",
        "test": "pytest tests/ -v",
        "lint": "ruff check .",
    },
    "structure": [
        "main.py          # FastAPI app entry point",
        "routes/           # API route handlers",
        "models/           # Pydantic models",
        "services/         # Business logic",
        "tests/            # Pytest test files",
    ],
}

claude_md_content = f"# {project_meta['name']}\n\n"
claude_md_content += f"{project_meta['description']}\n\n"
claude_md_content += f"**Language:** {project_meta['language']}  \n"
claude_md_content += f"**Framework:** {project_meta['framework']}\n\n"
claude_md_content += "## Commands\n\n"
claude_md_content += "```bash\n"
for cmd_name, cmd_value in project_meta["commands"].items():
    claude_md_content += f"# {cmd_name}\n{cmd_value}\n\n"
claude_md_content += "```\n\n"
claude_md_content += "## Project Structure\n\n"
claude_md_content += "```\n"
for item in project_meta["structure"]:
    claude_md_content += f"{item}\n"
claude_md_content += "```\n"

claude_path = os.path.join(WORKDIR, "CLAUDE.md")
with open(claude_path, "w") as f:
    f.write(claude_md_content)

score3 = 0
checks_3 = []

if "weather-api" in claude_md_content:
    checks_3.append(("Contains project name", "PASS"))
    score3 += 1
else:
    checks_3.append(("Contains project name", "FAIL"))

if "pip install" in claude_md_content and "pytest" in claude_md_content:
    checks_3.append(("Contains commands section", "PASS"))
    score3 += 1
else:
    checks_3.append(("Contains commands section", "FAIL"))

if os.path.exists(claude_path):
    checks_3.append(("Written to file", "PASS"))
    score3 += 1
else:
    checks_3.append(("Written to file", "FAIL"))

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 3 + 3 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 03 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Token budgets allocate context across system/user/project/history/output")
print(f"    2. Priority file selection ranks files by relevance, fits them in budget")
print(f"    3. CLAUDE.md gives the agent project-specific instructions and structure")
print(f"\n  TODO 1: {score1}/3 token_counter checks passed")
print(f"  TODO 2: {score2}/3 file_selector checks passed")
print(f"  TODO 3: {score3}/3 CLAUDE.md generation checks passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
