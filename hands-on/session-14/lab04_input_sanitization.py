#!/usr/bin/env python3
"""
Lab 04: Input Sanitization — Length, Encoding, and Content Policy

Build a multi-stage sanitization pipeline that validates input length,
normalizes encoding, and enforces content policies before LLM processing.

No external packages required — standard library only.
"""

import os
import json
import re
import shutil
import unicodedata

WORKDIR = "/tmp/safety-lab-14-04"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Input Attack Vectors                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Input Attack Vectors")
print("=" * 70)
print()
print("  User input can be weaponized in many ways:")
print()
print("  ┌─────────────────────┬────────────────────────────────────────────┐")
print("  │ Attack Vector       │ Example                                   │")
print("  ├─────────────────────┼────────────────────────────────────────────┤")
print("  │ Excessive length    │ 100K-character input to exhaust tokens    │")
print("  │ Unicode tricks      │ Homoglyph substitution (Cyrillic 'a' for │")
print("  │                     │ Latin 'a') to bypass keyword filters      │")
print("  ├─────────────────────┼────────────────────────────────────────────┤")
print("  │ Control characters  │ Null bytes, escape sequences, ANSI codes  │")
print("  │ Invisible chars     │ Zero-width spaces, joiners to hide text   │")
print("  ├─────────────────────┼────────────────────────────────────────────┤")
print("  │ Prohibited topics   │ Requests about weapons, illegal activity  │")
print("  │ Off-topic requests  │ Asking a finance bot about cooking        │")
print("  └─────────────────────┴────────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Sanitization Pipeline Stages                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Sanitization Pipeline Stages")
print("=" * 70)
print()
print("  A robust sanitization pipeline applies multiple checks in order:")
print()
print("   User Input")
print("       │")
print("       ▼")
print("  ┌──────────────────┐")
print("  │ 1. Length Check   │──▶ Reject if too long or too short")
print("  └──────────────────┘")
print("       │")
print("       ▼")
print("  ┌──────────────────┐")
print("  │ 2. Encoding Norm │──▶ Normalize Unicode, strip control chars")
print("  └──────────────────┘")
print("       │")
print("       ▼")
print("  ┌──────────────────┐")
print("  │ 3. Content Policy │──▶ Block prohibited topics")
print("  └──────────────────┘")
print("       │")
print("       ▼")
print("  Sanitized Input ──▶ LLM")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement Length Validation                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement length validation with configurable limits")
print("=" * 70)
print()

def validate_length(text: str, min_len: int = 1, max_len: int = 4096) -> dict:
    """Validate that input text length is within acceptable bounds.

    Args:
        text: Input text to validate
        min_len: Minimum allowed length (default: 1)
        max_len: Maximum allowed length (default: 4096)

    Returns:
        Dict with keys:
            - is_valid (bool): True if length is within bounds
            - length (int): Actual text length
            - error (str or None): Error message if invalid, None if valid
    """
    # TODO: Implement length validation.
    #   Check if len(text) is between min_len and max_len (inclusive).
    #   If too short: error = "Input too short: {length} < {min_len}"
    #   If too long:  error = "Input too long: {length} > {max_len}"
    #   If valid:     error = None

    return "___"  # Replace with your implementation

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    r1 = validate_length("Hello world", min_len=1, max_len=100)
    r2 = validate_length("", min_len=1, max_len=100)
    r3 = validate_length("x" * 5000, min_len=1, max_len=4096)

    checks = [
        r1["is_valid"] is True and r1["length"] == 11,
        r2["is_valid"] is False and "short" in r2["error"],
        r3["is_valid"] is False and "long" in r3["error"],
    ]
    if all(checks):
        score += 1
        print("[PASS] Length validation works correctly")
        print(f"       Normal: valid={r1['is_valid']}, len={r1['length']}")
        print(f"       Empty:  valid={r2['is_valid']}, error={r2['error']}")
        print(f"       Long:   valid={r3['is_valid']}, error={r3['error']}")
    else:
        print(f"[FAIL] r1={r1}, r2={r2}, r3={r3}")
except Exception as e:
    print(f"[FAIL] validate_length exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build Encoding Normalization                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Build encoding normalization (Unicode, whitespace, control chars)")
print("=" * 70)
print()

def normalize_encoding(text: str) -> dict:
    """Normalize text encoding for safe processing.

    Steps:
        1. Apply NFKC Unicode normalization (converts homoglyphs)
        2. Remove control characters (category 'Cc') except newline/tab
        3. Remove zero-width characters (U+200B, U+200C, U+200D, U+FEFF)
        4. Collapse multiple whitespace into single spaces
        5. Strip leading/trailing whitespace

    Args:
        text: Raw input text

    Returns:
        Dict with keys:
            - normalized (str): The cleaned text
            - changes_made (list): List of change descriptions
    """
    # TODO: Implement encoding normalization following the steps above.
    #   Track what changes were made in the changes_made list.
    #
    # Hints:
    #   unicodedata.normalize("NFKC", text)
    #   unicodedata.category(ch) == "Cc"  # control character
    #   re.sub(r"[ \t]+", " ", text)      # collapse whitespace

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    # Test with dirty input containing control chars and zero-width spaces
    dirty = "Hello\x00 \u200bworld\x01  test\u200d  input"
    r = normalize_encoding(dirty)
    checks = [
        "\x00" not in r["normalized"],
        "\x01" not in r["normalized"],
        "\u200b" not in r["normalized"],
        "\u200d" not in r["normalized"],
        "Hello" in r["normalized"],
        "world" in r["normalized"],
        len(r["changes_made"]) > 0,
    ]
    if all(checks):
        score += 1
        print("[PASS] Encoding normalization works correctly")
        print(f"       Input:   {repr(dirty)}")
        print(f"       Output:  {repr(r['normalized'])}")
        print(f"       Changes: {r['changes_made']}")
    else:
        print(f"[FAIL] normalized={repr(r['normalized'])}, changes={r['changes_made']}")
except Exception as e:
    print(f"[FAIL] normalize_encoding exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Create a Content Policy Checker                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Create a content policy checker (blocked topics)")
print("=" * 70)
print()

BLOCKED_TOPICS = {
    "weapons":      ["how to build a bomb", "make explosives", "create a weapon",
                     "assemble a firearm"],
    "illegal":      ["hack into", "break into a system", "steal credentials",
                     "bypass security", "crack a password"],
    "harmful":      ["how to hurt someone", "cause harm to", "self-harm",
                     "instructions for poison"],
    "private_data": ["give me the password", "reveal the api key",
                     "show me the secret", "dump the database"],
}

def check_content_policy(text: str) -> dict:
    """Check text against content policy rules.

    Args:
        text: Input text to check

    Returns:
        Dict with keys:
            - is_allowed (bool): True if no policy violations
            - violations (list): List of dicts with 'category' and 'matched_phrase'
    """
    # TODO: For each category in BLOCKED_TOPICS, check if any phrase
    #   appears in text (case-insensitive). Collect all violations.

    return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    r1 = check_content_policy("How to build a bomb at home")
    r2 = check_content_policy("How to build a React application")
    r3 = check_content_policy("Can you hack into my neighbor's wifi and give me the password?")
    checks = [
        r1["is_allowed"] is False,
        any(v["category"] == "weapons" for v in r1["violations"]),
        r2["is_allowed"] is True,
        r3["is_allowed"] is False,
        len(r3["violations"]) >= 2,  # illegal + private_data
    ]
    if all(checks):
        score += 1
        print("[PASS] Content policy checker works correctly")
        print(f"       Weapons:  allowed={r1['is_allowed']}, violations={len(r1['violations'])}")
        print(f"       Safe:     allowed={r2['is_allowed']}")
        print(f"       Multi:    allowed={r3['is_allowed']}, violations={len(r3['violations'])}")
    else:
        print(f"[FAIL] r1={r1}, r2={r2}, r3={r3}")
except Exception as e:
    print(f"[FAIL] check_content_policy exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Assemble a Full Sanitization Pipeline                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Assemble a full sanitization pipeline")
print("=" * 70)
print()

def sanitize_input(text: str, max_len: int = 4096) -> dict:
    """Run the full sanitization pipeline on user input.

    Pipeline stages (in order):
        1. Length validation (min=1, max=max_len)
        2. Encoding normalization
        3. Content policy check

    Args:
        text: Raw user input
        max_len: Maximum allowed input length

    Returns:
        Dict with keys:
            - is_safe (bool): True only if ALL stages pass
            - sanitized_text (str): The normalized text (even if blocked)
            - stages (dict): Result from each pipeline stage
            - blocked_reason (str or None): Why input was blocked, if applicable
    """
    # TODO: Chain all three stages together. If any stage fails,
    #   set is_safe=False and record the blocked_reason.
    #
    # Hint:
    #   1. Run validate_length → if invalid, return immediately
    #   2. Run normalize_encoding → get sanitized text
    #   3. Run check_content_policy on sanitized text → if violated, block
    #   4. If all pass, return is_safe=True

    return "___"  # Replace with your implementation

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    r1 = sanitize_input("How do I configure a Kubernetes deployment?")
    r2 = sanitize_input("")
    r3 = sanitize_input("How to hack into a corporate network")
    r4 = sanitize_input("Hello\x00 \u200bworld")

    checks = [
        r1["is_safe"] is True and r1["blocked_reason"] is None,
        r2["is_safe"] is False and "short" in r2["blocked_reason"],
        r3["is_safe"] is False and "policy" in r3["blocked_reason"].lower(),
        r4["is_safe"] is True,
        "\x00" not in r4["sanitized_text"],
        "\u200b" not in r4["sanitized_text"],
    ]
    if all(checks):
        score += 1
        print("[PASS] Full sanitization pipeline works correctly")
        print(f"       Safe input:  safe={r1['is_safe']}")
        print(f"       Empty input: safe={r2['is_safe']}, reason={r2['blocked_reason']}")
        print(f"       Bad topic:   safe={r3['is_safe']}, reason={r3['blocked_reason']}")
        print(f"       Dirty text:  safe={r4['is_safe']}, text={repr(r4['sanitized_text'])}")
        # Save pipeline report
        report = {"safe": r1, "empty": r2, "blocked": r3, "normalized": r4}
        out_path = os.path.join(WORKDIR, "sanitization_report.json")
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Pipeline checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] sanitize_input exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 04 Score: {score}/{total}")
print("=" * 70)
