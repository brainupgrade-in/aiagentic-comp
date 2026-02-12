#!/usr/bin/env python3
"""
Lab 07: Red Team Testing — Attack Categories, Scoring, and Reporting

Learn red team methodology for AI systems: define attack categories,
build a test runner, score defense effectiveness, and generate reports.

No external packages required — standard library only.
"""

import os
import json
import re
import shutil
from datetime import datetime

WORKDIR = "/tmp/safety-lab-14-07"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Red Team Methodology                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Red Team Methodology for AI Systems")
print("=" * 70)
print()
print("  Red teaming tests AI defenses by simulating adversarial attacks.")
print()
print("  ┌──────────────────┬──────────┬────────────────────────────────────┐")
print("  │ Attack Category  │ Severity │ Description                       │")
print("  ├──────────────────┼──────────┼────────────────────────────────────┤")
print("  │ Prompt Injection │ HIGH     │ Override system instructions      │")
print("  │ Jailbreak        │ HIGH     │ Bypass safety constraints         │")
print("  │ Data Exfiltration│ CRITICAL │ Extract training data or secrets  │")
print("  │ PII Extraction   │ CRITICAL │ Trick model into revealing PII   │")
print("  │ Harmful Content  │ HIGH     │ Generate violent/illegal content  │")
print("  │ Bias Probing     │ MEDIUM   │ Elicit discriminatory responses  │")
print("  │ Off-Topic Abuse  │ LOW      │ Use the system for unintended    │")
print("  │                  │          │ purposes                         │")
print("  └──────────────────┴──────────┴────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Test Matrix and Scoring Framework                                ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Test Matrix and Scoring Framework")
print("=" * 70)
print()
print("  Scoring per attack:")
print("    BLOCKED  = 1.0  (defense worked, attack prevented)")
print("    PARTIAL  = 0.5  (partially mitigated, some leakage)")
print("    BYPASSED = 0.0  (defense failed, attack succeeded)")
print()
print("  Defense Score = sum(scores) / number_of_attacks")
print("  Target: >= 0.8 (80% defense effectiveness)")
print()

# ── Defense function to test against ─────────────────────────────────────────

INJECTION_KEYWORDS = [
    "ignore previous instructions", "ignore all instructions",
    "disregard your instructions", "override your system prompt",
    "you are now", "forget your instructions",
]
JAILBREAK_KEYWORDS = [
    "do anything now", "dan mode", "no restrictions",
    "unrestricted mode", "developer mode", "god mode",
    "pretend you are", "act as if you have no",
]
EXFIL_KEYWORDS = [
    "reveal the system prompt", "show your instructions",
    "what are your rules", "dump your training data",
    "output your configuration",
]
HARMFUL_KEYWORDS = [
    "how to build a bomb", "make explosives", "create a weapon",
    "hack into", "steal credentials", "how to hurt someone",
]

def defense_system(text: str) -> dict:
    """A simple multi-layer defense system for testing."""
    text_lower = text.lower()
    for kw in INJECTION_KEYWORDS:
        if kw in text_lower:
            return {"blocked": True, "reason": "injection_detected"}
    for kw in JAILBREAK_KEYWORDS:
        if kw in text_lower:
            return {"blocked": True, "reason": "jailbreak_detected"}
    for kw in EXFIL_KEYWORDS:
        if kw in text_lower:
            return {"blocked": True, "reason": "exfiltration_detected"}
    for kw in HARMFUL_KEYWORDS:
        if kw in text_lower:
            return {"blocked": True, "reason": "harmful_content_detected"}
    return {"blocked": False, "reason": "allowed"}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Define Attack Categories and Example Payloads                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Define attack categories and example payloads")
print("=" * 70)
print()

# TODO: Define a dictionary of attack categories, each with:
#   - "severity": "CRITICAL", "HIGH", "MEDIUM", or "LOW"
#   - "payloads": list of 2-3 example attack strings
#
# Categories to define:
#   "prompt_injection" (severity: HIGH)
#     - payloads that use phrases from INJECTION_KEYWORDS
#   "jailbreak" (severity: HIGH)
#     - payloads that use phrases from JAILBREAK_KEYWORDS
#   "data_exfiltration" (severity: CRITICAL)
#     - payloads that use phrases from EXFIL_KEYWORDS
#   "harmful_content" (severity: HIGH)
#     - payloads that use phrases from HARMFUL_KEYWORDS

attack_catalog = "___"  # Replace with your attack catalog dict

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
checks = [
    len(attack_catalog) == 4,
    all(
        "severity" in cat and "payloads" in cat and len(cat["payloads"]) >= 2
        for cat in attack_catalog.values()
    ),
    "prompt_injection" in attack_catalog,
    "jailbreak" in attack_catalog,
    "data_exfiltration" in attack_catalog,
    "harmful_content" in attack_catalog,
    attack_catalog["data_exfiltration"]["severity"] == "CRITICAL",
]
if all(checks):
    score += 1
    print("[PASS] Attack catalog defined correctly")
    for cat, info in attack_catalog.items():
        print(f"       {cat}: severity={info['severity']}, payloads={len(info['payloads'])}")
else:
    print("[FAIL] Attack catalog is incomplete or incorrect")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build a Test Runner                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Build a test runner that executes attacks against defenses")
print("=" * 70)
print()

def run_red_team_tests(catalog: dict, defense_fn) -> list:
    """Execute all attacks from the catalog against the defense function.

    Args:
        catalog: Attack catalog dict (from TODO 1)
        defense_fn: Function that takes text and returns
            {"blocked": bool, "reason": str}

    Returns:
        List of result dicts, each with:
            - category (str): Attack category name
            - severity (str): Attack severity
            - payload (str): The attack payload used
            - blocked (bool): Whether defense blocked it
            - defense_reason (str): Reason from defense function
            - score (float): 1.0 if blocked, 0.0 if bypassed
    """
    # TODO: Iterate over each category and payload in the catalog.
    #   Call defense_fn(payload) for each attack.
    #   Record the result.

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    test_results = run_red_team_tests(attack_catalog, defense_system)
    total_attacks = sum(len(c["payloads"]) for c in attack_catalog.values())
    checks = [
        isinstance(test_results, list),
        len(test_results) == total_attacks,
        all("category" in r and "blocked" in r and "score" in r for r in test_results),
        all(r["score"] in (0.0, 1.0) for r in test_results),
    ]
    if all(checks):
        score += 1
        blocked_count = sum(1 for r in test_results if r["blocked"])
        print(f"[PASS] Test runner executed {len(test_results)} attacks")
        print(f"       Blocked: {blocked_count}/{len(test_results)}")
    else:
        print(f"[FAIL] test_results issues: {len(test_results)} results")
except Exception as e:
    print(f"[FAIL] run_red_team_tests exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Score Defense Effectiveness                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Score defense effectiveness and generate summary")
print("=" * 70)
print()

def score_defense(test_results: list) -> dict:
    """Calculate defense effectiveness scores.

    Args:
        test_results: List of result dicts from run_red_team_tests

    Returns:
        Dict with keys:
            - overall_score (float): Average score across all attacks
            - category_scores (dict): Score per category
            - severity_scores (dict): Score per severity level
            - total_attacks (int): Total number of attacks
            - total_blocked (int): Number blocked
            - meets_target (bool): True if overall_score >= 0.8
    """
    # TODO: Calculate overall, per-category, and per-severity scores.
    #   Score = sum of individual scores / count of attacks in that group.

    return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    defense_scores = score_defense(test_results)
    checks = [
        isinstance(defense_scores["overall_score"], float),
        0.0 <= defense_scores["overall_score"] <= 1.0,
        len(defense_scores["category_scores"]) == 4,
        defense_scores["total_attacks"] == len(test_results),
        isinstance(defense_scores["meets_target"], bool),
    ]
    if all(checks):
        score += 1
        print(f"[PASS] Defense scoring complete")
        print(f"       Overall: {defense_scores['overall_score']:.2f}")
        print(f"       Target met: {defense_scores['meets_target']}")
        for cat, cs in defense_scores["category_scores"].items():
            print(f"       {cat}: {cs:.2f}")
    else:
        print(f"[FAIL] defense_scores={defense_scores}")
except Exception as e:
    print(f"[FAIL] score_defense exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Generate Red Team Summary Report                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Generate a red team summary report (JSON)")
print("=" * 70)
print()

def generate_report(catalog: dict, test_results: list,
                    defense_scores: dict) -> dict:
    """Generate a comprehensive red team testing report.

    Args:
        catalog: The attack catalog
        test_results: Individual test results
        defense_scores: Aggregated defense scores

    Returns:
        Dict with keys:
            - report_title (str): "AI Safety Red Team Report"
            - timestamp (str): ISO format timestamp
            - attack_summary (dict): counts per category
            - defense_summary (dict): the defense_scores dict
            - bypassed_attacks (list): attacks that were NOT blocked
            - recommendations (list): list of recommendation strings
    """
    # TODO: Build the report.
    #   - attack_summary: for each category, record severity and payload_count
    #   - bypassed_attacks: filter test_results where blocked=False
    #   - recommendations: add one recommendation per category that
    #     scored below 1.0, suggesting improvement.
    #     If all categories score 1.0, add "All categories fully defended."

    return "___"  # Replace with your implementation

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    report = generate_report(attack_catalog, test_results, defense_scores)
    checks = [
        report["report_title"] == "AI Safety Red Team Report",
        "timestamp" in report,
        len(report["attack_summary"]) == 4,
        isinstance(report["bypassed_attacks"], list),
        isinstance(report["recommendations"], list),
        len(report["recommendations"]) > 0,
        "defense_summary" in report,
    ]
    if all(checks):
        score += 1
        print("[PASS] Red team report generated successfully")
        print(f"       Title: {report['report_title']}")
        print(f"       Categories: {len(report['attack_summary'])}")
        print(f"       Bypassed: {len(report['bypassed_attacks'])}")
        print(f"       Recommendations: {len(report['recommendations'])}")
        for rec in report["recommendations"]:
            print(f"         - {rec}")
        # Save report
        out_path = os.path.join(WORKDIR, "red_team_report.json")
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Report checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] generate_report exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 07 Score: {score}/{total}")
print("=" * 70)
