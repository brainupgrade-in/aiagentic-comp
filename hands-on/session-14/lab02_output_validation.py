#!/usr/bin/env python3
"""
Lab 02: Output Validation — PII Detection and Schema Enforcement

Learn why LLM outputs must be validated, build regex-based PII detectors
for email, phone, SSN, and credit card numbers, and enforce JSON schemas.

No external packages required — standard library only.
"""

import os
import json
import re
import shutil

WORKDIR = "/tmp/safety-lab-14-02"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Why Validate LLM Output?                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Why Validate LLM Output?")
print("=" * 70)
print()
print("  LLMs can generate harmful, incorrect, or sensitive content.")
print("  Output validation is the last line of defense before the user.")
print()
print("  ┌─────────────────────┬────────────────────────────────────────────┐")
print("  │ Risk Category       │ Example                                   │")
print("  ├─────────────────────┼────────────────────────────────────────────┤")
print("  │ PII Leakage         │ Output contains SSNs, credit card numbers │")
print("  │ Hallucinated Data   │ Fabricated statistics presented as facts  │")
print("  │ Toxic Content       │ Hate speech, harassment, or threats       │")
print("  │ Code Injection      │ SQL/XSS in generated code snippets       │")
print("  │ Format Violations   │ Invalid JSON when structured output      │")
print("  │                     │ is expected                              │")
print("  │ Confidential Data   │ Internal API keys, passwords in output   │")
print("  └─────────────────────┴────────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — PII Patterns                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: PII Patterns (Regex-Based Detection)")
print("=" * 70)
print()
print("  Common PII patterns and their regex signatures:")
print()
print("  ┌──────────────┬───────────────────────────┬──────────────────────┐")
print("  │ PII Type     │ Pattern                   │ Example              │")
print("  ├──────────────┼───────────────────────────┼──────────────────────┤")
print("  │ Email        │ [\\w.+-]+@[\\w-]+\\.[\\w.]+   │ user@example.com     │")
print("  ├──────────────┼───────────────────────────┼──────────────────────┤")
print("  │ Phone (US)   │ \\b\\d{3}[-.\\s]?\\d{3}[-.   │ 555-123-4567         │")
print("  │              │ \\s]?\\d{4}\\b               │                      │")
print("  ├──────────────┼───────────────────────────┼──────────────────────┤")
print("  │ SSN          │ \\b\\d{3}-\\d{2}-\\d{4}\\b     │ 123-45-6789          │")
print("  ├──────────────┼───────────────────────────┼──────────────────────┤")
print("  │ Credit Card  │ \\b\\d{4}[- ]?\\d{4}[- ]?   │ 4111-1111-1111-1111  │")
print("  │              │ \\d{4}[- ]?\\d{4}\\b         │                      │")
print("  └──────────────┴───────────────────────────┴──────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Write Regex Patterns for PII Detection                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Write regex patterns for PII detection")
print("=" * 70)
print()

# TODO: Define regex patterns for each PII type.
#   Each pattern should match the examples shown in STEP 2.
#   Use raw strings (r"...") for the patterns.
#
# Hints:
#   email:       [\w.+-]+@[\w-]+\.[\w.]+
#   phone:       \b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b
#   ssn:         \b\d{3}-\d{2}-\d{4}\b
#   credit_card: \b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b

PII_PATTERNS = {
    "email":       "___",
    "phone":       "___",
    "ssn":         "___",
    "credit_card": "___",
}

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
test_cases = {
    "email":       ("Contact us at admin@oracle.com for help", True),
    "phone":       ("Call 555-123-4567 for support", True),
    "ssn":         ("SSN on file: 123-45-6789", True),
    "credit_card": ("Card: 4111 1111 1111 1111", True),
}
passed_all = True
for pii_type, (sample, should_match) in test_cases.items():
    pattern = PII_PATTERNS.get(pii_type, "")
    found = bool(re.search(pattern, sample)) if pattern else False
    if found != should_match:
        passed_all = False
        print(f"  [FAIL] {pii_type}: expected match={should_match}, got {found}")

# Also check that patterns do NOT match clean text
clean_text = "The quarterly report is ready for review."
for pii_type, pattern in PII_PATTERNS.items():
    if re.search(pattern, clean_text):
        passed_all = False
        print(f"  [FAIL] {pii_type}: false positive on clean text")

if passed_all:
    score += 1
    print("[PASS] All PII patterns match expected inputs and reject clean text")
else:
    print("[FAIL] Some PII pattern checks failed")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build an Output Validator for PII Leakage                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Build an output validator that checks for PII leakage")
print("=" * 70)
print()

def validate_no_pii(text: str) -> dict:
    """Check text for PII leakage using regex patterns.

    Args:
        text: The LLM output text to validate

    Returns:
        Dict with keys:
            - is_safe (bool): True if no PII found
            - pii_found (list): List of dicts with 'type', 'match', 'position'
            - pii_count (int): Total number of PII matches
    """
    # TODO: Iterate over PII_PATTERNS, use re.finditer to find all matches.
    #   For each match, record {"type": pii_type, "match": match.group(),
    #   "position": match.start()}.
    #   Return the result dict.

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    dirty = "Contact john@example.com or call 555-867-5309. SSN: 078-05-1120."
    clean = "The project deadline is next Friday."

    r_dirty = validate_no_pii(dirty)
    r_clean = validate_no_pii(clean)

    checks = [
        r_dirty["is_safe"] is False,
        r_dirty["pii_count"] == 3,  # email + phone + ssn
        r_clean["is_safe"] is True,
        r_clean["pii_count"] == 0,
    ]
    if all(checks):
        score += 1
        print("[PASS] PII validator works correctly")
        for item in r_dirty["pii_found"]:
            print(f"       Found {item['type']}: {item['match']}")
    else:
        print(f"[FAIL] dirty: safe={r_dirty['is_safe']}, count={r_dirty['pii_count']}")
        print(f"       clean: safe={r_clean['is_safe']}, count={r_clean['pii_count']}")
except Exception as e:
    print(f"[FAIL] validate_no_pii exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Validate JSON Schema Compliance                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Validate that output matches an expected JSON schema")
print("=" * 70)
print()

def validate_schema(output_text: str, required_fields: dict) -> dict:
    """Validate that a JSON output matches the expected schema.

    Args:
        output_text: The LLM output (should be valid JSON)
        required_fields: Dict mapping field names to expected types
            e.g. {"name": str, "age": int, "tags": list}

    Returns:
        Dict with keys:
            - is_valid (bool): True if JSON is valid and all fields match
            - errors (list): List of error message strings
    """
    # TODO: Implement schema validation:
    #   1. Try to parse output_text as JSON. If it fails, return error.
    #   2. For each field in required_fields, check:
    #      a. The field exists in the parsed JSON
    #      b. The field's value is an instance of the expected type
    #   3. Return the result dict.
    #
    # Hint:
    #   try:
    #       data = json.loads(output_text)
    #   except (json.JSONDecodeError, TypeError) as e:
    #       return {"is_valid": False, "errors": [f"Invalid JSON: {e}"]}

    return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    schema = {"name": str, "age": int, "tags": list}

    good_output = '{"name": "Alice", "age": 30, "tags": ["engineer", "lead"]}'
    bad_output_1 = '{"name": "Bob", "age": "thirty", "tags": []}'
    bad_output_2 = '{"name": "Charlie"}'
    bad_output_3 = 'not json at all'

    r_good = validate_schema(good_output, schema)
    r_bad1 = validate_schema(bad_output_1, schema)
    r_bad2 = validate_schema(bad_output_2, schema)
    r_bad3 = validate_schema(bad_output_3, schema)

    checks = [
        r_good["is_valid"] is True,
        len(r_good["errors"]) == 0,
        r_bad1["is_valid"] is False,
        any("age" in e for e in r_bad1["errors"]),
        r_bad2["is_valid"] is False,
        len(r_bad2["errors"]) == 2,  # missing age and tags
        r_bad3["is_valid"] is False,
        any("JSON" in e for e in r_bad3["errors"]),
    ]
    if all(checks):
        score += 1
        print("[PASS] Schema validator works correctly")
        print(f"       Good output: valid={r_good['is_valid']}")
        print(f"       Bad type:    errors={r_bad1['errors']}")
        print(f"       Missing:     errors={r_bad2['errors']}")
        print(f"       Not JSON:    errors={r_bad3['errors']}")
        # Save report
        report = {
            "good": r_good, "bad_type": r_bad1,
            "missing_fields": r_bad2, "invalid_json": r_bad3,
        }
        out_path = os.path.join(WORKDIR, "validation_report.json")
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        print("[FAIL] Schema validation checks failed")
        print(f"       good={r_good}, bad1={r_bad1}, bad2={r_bad2}, bad3={r_bad3}")
except Exception as e:
    print(f"[FAIL] validate_schema exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 02 Score: {score}/{total}")
print("=" * 70)
