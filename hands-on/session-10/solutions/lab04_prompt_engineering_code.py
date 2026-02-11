"""
Lab 04 Solution: Prompt Engineering for Code
===============================================
"""

import os
import shutil
import json

WORKDIR = "/tmp/aidev-lab-10-04"

print("=" * 50)
print("  Lab 04: Prompt Engineering for Code (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Three Levels of Prompt Quality
# ============================================================

print("\n--- Step 1: Three Levels of Prompt Quality ---\n")

levels = [
    ("BAD",   "make a login",
     "Vague, no language, no framework, no requirements"),
    ("GOOD",  "Create a Python Flask login endpoint with email/password validation",
     "Has language, framework, and basic requirements"),
    ("GREAT", "Create a POST /api/auth/login endpoint using Python FastAPI with: "
              "Pydantic model for email (valid format) and password (min 8 chars), "
              "bcrypt password comparison, JWT token response with 1h expiry, "
              "401 for invalid credentials, return type LoginResponse(token, expires_at)",
     "Specific endpoint, framework, validation rules, auth mechanism, error handling, return type"),
]

for level, prompt, why in levels:
    print(f"  [{level}]")
    print(f"    Prompt: \"{prompt}\"")
    print(f"    Why:    {why}\n")


# ============================================================
# Step 2: Structured Prompt Template
# ============================================================

print("\n--- Step 2: Structured Prompt Template ---\n")

template = """
  TASK:        [What to build / what to change]
  LANGUAGE:    [Programming language]
  FRAMEWORK:   [Library or framework to use]
  INPUT:       [What the function/endpoint receives]
  OUTPUT:      [What it returns, including types]
  CONSTRAINTS: [Validation rules, limits, error cases]
  STYLE:       [Naming conventions, patterns to follow]
  EXAMPLE:     [Sample input -> expected output]
"""
print(template)


# ============================================================
# TODO 1 Solution: Rate 3 prompts
# ============================================================

print("\n--- TODO 1: Rate These Prompts ---\n")

prompts_to_rate = [
    {
        "prompt": "write a function to sort data",
        "rating": "bad",
        "correct": "bad",
        "reason": "No language, no data type, no sort criteria, no function name",
    },
    {
        "prompt": "Write a Python function sort_users(users: list[dict]) that sorts by 'created_at' descending",
        "rating": "good",
        "correct": "good",
        "reason": "Has language, function name, types, sort field and order",
    },
    {
        "prompt": ("Write a Python function sort_users(users: list[dict], key: str = 'created_at', "
                   "reverse: bool = True) -> list[dict] that: sorts by the given key, "
                   "raises ValueError if key not in dicts, handles empty list by returning [], "
                   "preserves original list (returns new copy). "
                   "Example: sort_users([{'name': 'A', 'created_at': 2}], 'name') -> [{'name': 'A', 'created_at': 2}]"),
        "rating": "great",
        "correct": "great",
        "reason": "Full signature, edge cases, error handling, immutability, example",
    },
]

score1 = 0
for i, p in enumerate(prompts_to_rate, 1):
    if p["rating"].strip().lower() == p["correct"]:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Prompt {i}: \"{p['prompt'][:60]}...\"")
    print(f"             Your rating: {p['rating']}")

print(f"\n  Score: {score1}/{len(prompts_to_rate)}")


# ============================================================
# TODO 2 Solution: Rewrite a bad prompt
# ============================================================

print("\n\n--- TODO 2: Rewrite a Bad Prompt ---\n")

bad_prompt = "make a function to validate emails"
print(f"  Bad prompt: \"{bad_prompt}\"\n")

great_prompt = (
    "Write a Python function validate_email(email: str) -> bool that: "
    "checks the email contains exactly one @ symbol with a non-empty local part "
    "and a domain containing at least one dot, "
    "returns False for empty strings or None input, "
    "raises TypeError if input is not a string. "
    "Example: validate_email('user@example.com') -> True, "
    "validate_email('invalid') -> False"
)

score2 = 0
checks_2 = []

prompt_lower = great_prompt.lower()

has_func_name = any(kw in prompt_lower for kw in ["validate_email", "is_valid_email", "check_email", "email_validator"])
if has_func_name:
    checks_2.append(("Has function name", "PASS"))
    score2 += 1
else:
    checks_2.append(("Has function name", "FAIL"))

has_types = any(kw in prompt_lower for kw in ["str", "bool", "string", "-> bool", "-> str", "returns"])
if has_types:
    checks_2.append(("Has type information", "PASS"))
    score2 += 1
else:
    checks_2.append(("Has type information", "FAIL"))

has_rule = any(kw in prompt_lower for kw in ["@", "format", "regex", "pattern", "contains", "domain", "valid"])
if has_rule:
    checks_2.append(("Has validation rule", "PASS"))
    score2 += 1
else:
    checks_2.append(("Has validation rule", "FAIL"))

has_error = any(kw in prompt_lower for kw in ["error", "invalid", "raise", "empty", "none", "false", "exception"])
if has_error:
    checks_2.append(("Has error case", "PASS"))
    score2 += 1
else:
    checks_2.append(("Has error case", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/4")


# ============================================================
# TODO 3 Solution: Generate a structured prompt
# ============================================================

print("\n\n--- TODO 3: Generate a Structured Prompt ---\n")

task_meta = {
    "task": "Create a REST endpoint to search products",
    "language": "Python",
    "framework": "FastAPI",
    "input": "query string, optional category filter, page number",
    "output": "list of product dicts with name, price, category",
    "constraints": "max 50 results per page, category must be valid enum, empty query returns 400",
    "example_input": "GET /api/products?q=laptop&category=electronics&page=1",
    "example_output": '{"products": [{"name": "Laptop X", "price": 999.99, "category": "electronics"}], "total": 42}',
}

structured_prompt = f"""TASK:        {task_meta['task']}
LANGUAGE:    {task_meta['language']}
FRAMEWORK:   {task_meta['framework']}
INPUT:       {task_meta['input']}
OUTPUT:      {task_meta['output']}
CONSTRAINTS: {task_meta['constraints']}
EXAMPLE:
  Input:  {task_meta['example_input']}
  Output: {task_meta['example_output']}"""

print(f"  Generated prompt:\n")
for line in structured_prompt.split("\n"):
    print(f"    {line}")

score3 = 0
checks_3 = []

sp_lower = structured_prompt.lower()

if "search products" in sp_lower or "rest endpoint" in sp_lower:
    checks_3.append(("Contains TASK", "PASS"))
    score3 += 1
else:
    checks_3.append(("Contains TASK", "FAIL"))

if "python" in sp_lower or "fastapi" in sp_lower:
    checks_3.append(("Contains LANGUAGE or FRAMEWORK", "PASS"))
    score3 += 1
else:
    checks_3.append(("Contains LANGUAGE or FRAMEWORK", "FAIL"))

if ("query" in sp_lower or "input" in sp_lower) and ("product" in sp_lower or "output" in sp_lower):
    checks_3.append(("Contains INPUT/OUTPUT", "PASS"))
    score3 += 1
else:
    checks_3.append(("Contains INPUT/OUTPUT", "FAIL"))

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Save reference
# ============================================================

ref = {
    "template_fields": ["TASK", "LANGUAGE", "FRAMEWORK", "INPUT", "OUTPUT",
                        "CONSTRAINTS", "STYLE", "EXAMPLE"],
    "quality_levels": {
        "bad": "Vague, missing key details",
        "good": "Has language, function name, basic requirements",
        "great": "Full spec with types, edge cases, examples",
    },
}

with open(os.path.join(WORKDIR, "prompt-engineering-reference.json"), "w") as f:
    json.dump(ref, f, indent=2)


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 3 + 4 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 04 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Bad prompts = vague; Good prompts = specific; Great prompts = complete spec")
print(f"    2. Structured templates force you to think about types, errors, examples")
print(f"    3. The more constraints you give, the better the generated code")
print(f"\n  TODO 1: {score1}/3 ratings correct")
print(f"  TODO 2: {score2}/4 rewrite checks passed")
print(f"  TODO 3: {score3}/3 structured prompt checks passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
