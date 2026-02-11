"""
Lab 02 Solution: Test Runner Server

Learn to build a test execution simulation tool that runs simple test
functions and parses pytest-style output.

Key concepts:
- Test discovery and execution patterns
- Pytest output format parsing
- Test report generation with pass rates

Uses only Python standard library (json, os, re, traceback, textwrap).
"""

import json
import os
import re
import shutil
import textwrap
import traceback

WORKDIR = "/tmp/aidev-lab-12-02"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: Pytest Output Format ──────────────────────────────────
print("=" * 70)
print("STEP 1: Understanding Pytest Output Format")
print("=" * 70)

print("""
Pytest produces a structured text output. A typical summary looks like:

  ========================= test session starts ==========================
  collected 8 items

  tests/test_api.py::test_health_check PASSED
  tests/test_api.py::test_create_item PASSED
  tests/test_api.py::test_get_item PASSED
  tests/test_api.py::test_delete_item FAILED
  tests/test_api.py::test_update_item PASSED
  tests/test_api.py::test_invalid_input ERROR
  tests/test_api.py::test_list_items PASSED
  tests/test_api.py::test_auth PASSED

  ===================== 6 passed, 1 failed, 1 error ======================

  Key fields to extract:
  ┌──────────────────┬─────────────────────────────────────────────┐
  │ Field            │ How to Find It                              │
  ├──────────────────┼─────────────────────────────────────────────┤
  │ total            │ "collected N items" line                    │
  │ passed           │ Count of lines ending with PASSED           │
  │ failed           │ Count of lines ending with FAILED           │
  │ errors           │ Count of lines ending with ERROR            │
  │ summary line     │ Last line: "N passed, N failed, ..."        │
  └──────────────────┴─────────────────────────────────────────────┘
""")

# ── Step 2: Parsing Strategy ──────────────────────────────────────
print("=" * 70)
print("STEP 2: Parsing Test Results")
print("=" * 70)

print("""
Strategy for parsing pytest-like output:

  1. Use regex to find "collected (\\d+) items" for total count
  2. Count lines matching "PASSED", "FAILED", "ERROR"
  3. Extract failing test names for the report
  4. Calculate pass rate as passed / total * 100

  Example regex patterns:
    collected_pattern = r"collected (\\d+) items?"
    result_pattern    = r"(\\S+)\\s+(PASSED|FAILED|ERROR)"
""")

# ── Sample pytest output ──────────────────────────────────────────

SAMPLE_PYTEST_OUTPUT = textwrap.dedent("""\
    ========================= test session starts ==========================
    platform linux -- Python 3.13.0, pytest-8.0.0
    collected 8 items

    tests/test_api.py::test_health_check PASSED
    tests/test_api.py::test_create_item PASSED
    tests/test_api.py::test_get_item PASSED
    tests/test_api.py::test_delete_item FAILED
    tests/test_api.py::test_update_item PASSED
    tests/test_api.py::test_invalid_input ERROR
    tests/test_api.py::test_list_items PASSED
    tests/test_api.py::test_auth PASSED

    ===================== 6 passed, 1 failed, 1 error ======================
""")

SAMPLE_ALL_PASS_OUTPUT = textwrap.dedent("""\
    ========================= test session starts ==========================
    collected 3 items

    tests/test_math.py::test_add PASSED
    tests/test_math.py::test_subtract PASSED
    tests/test_math.py::test_multiply PASSED

    ========================= 3 passed =========================
""")


# ── Sample test functions ─────────────────────────────────────────

def test_addition():
    assert 2 + 2 == 4

def test_string_upper():
    assert "hello".upper() == "HELLO"

def test_list_append():
    lst = [1, 2]
    lst.append(3)
    assert lst == [1, 2, 3]

def test_division_by_zero():
    # This will fail
    result = 10 / 0

def test_type_check():
    assert isinstance(42, str)  # This will fail


# ── TODO 1: Simple Test Runner ─────────────────────────────────────
print("=" * 70)
print("TODO 1: Implement run_tests(test_functions)")
print("=" * 70)

print("""
Given a list of callables (test functions), execute each one.
- If the function runs without exception -> mark as "passed"
- If it raises AssertionError -> mark as "failed"
- If it raises any other exception -> mark as "error"

Return a list of dicts:
  [{"name": <func.__name__>, "status": "passed"|"failed"|"error",
    "detail": None or str(exception)}]
""")


def run_tests(test_functions: list) -> list:
    """Execute test functions and return results."""
    results = []

    for func in test_functions:
        try:
            func()
            results.append({"name": func.__name__, "status": "passed", "detail": None})
        except AssertionError as e:
            results.append({"name": func.__name__, "status": "failed", "detail": str(e) if str(e) else "Assertion failed"})
        except Exception as e:
            results.append({"name": func.__name__, "status": "error", "detail": str(e)})

    return results


# Validate TODO 1
total += 1
try:
    funcs = [test_addition, test_string_upper, test_list_append, test_division_by_zero, test_type_check]
    result = run_tests(funcs)
    if isinstance(result, list) and len(result) == 5:
        statuses = [r["status"] for r in result]
        if statuses[:3] == ["passed", "passed", "passed"]:
            print(f"  [PASS] run_tests correctly identified 3 passing tests")
            score += 1
        else:
            print(f"  [FAIL] First 3 tests should pass: {statuses[:3]}")
    else:
        print(f"  [FAIL] run_tests returned: {result}")
except Exception as e:
    print(f"  [FAIL] run_tests raised: {e}")

total += 1
try:
    funcs = [test_addition, test_division_by_zero, test_type_check]
    result = run_tests(funcs)
    if isinstance(result, list):
        statuses = [r["status"] for r in result]
        # division_by_zero is "error" (ZeroDivisionError), type_check is "failed" (AssertionError)
        if "error" in statuses and "failed" in statuses:
            print(f"  [PASS] run_tests correctly distinguishes 'failed' from 'error'")
            score += 1
        else:
            print(f"  [FAIL] Expected both 'error' and 'failed' in: {statuses}")
    else:
        print(f"  [FAIL] run_tests returned: {result}")
except Exception as e:
    print(f"  [FAIL] run_tests raised: {e}")


# ── TODO 2: Parse Pytest Output ────────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement parse_test_results(output_text)")
print("=" * 70)

print("""
Parse a pytest-style output string and extract:
  - total:   from "collected N items" line
  - passed:  count of lines containing "PASSED"
  - failed:  count of lines containing "FAILED"
  - errors:  count of lines containing "ERROR" (in result lines, not header)
  - failing_tests: list of test names (the part before FAILED or ERROR)

Return a dict with keys: total, passed, failed, errors, failing_tests
""")


def parse_test_results(output_text: str) -> dict:
    """Parse pytest-style output into a structured dict."""
    # Find total from "collected N items"
    collected_match = re.search(r"collected (\d+) items?", output_text)
    total_tests = int(collected_match.group(1)) if collected_match else 0

    # Find individual test results
    result_pattern = re.compile(r"(\S+)\s+(PASSED|FAILED|ERROR)")
    matches = result_pattern.findall(output_text)

    passed = sum(1 for _, status in matches if status == "PASSED")
    failed = sum(1 for _, status in matches if status == "FAILED")
    errors = sum(1 for _, status in matches if status == "ERROR")

    failing_tests = [name for name, status in matches if status in ("FAILED", "ERROR")]

    return {
        "total": total_tests,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "failing_tests": failing_tests,
    }


# Validate TODO 2
total += 1
try:
    result = parse_test_results(SAMPLE_PYTEST_OUTPUT)
    if isinstance(result, dict) and result.get("total") == 8:
        print(f"  [PASS] parse_test_results found total=8")
        score += 1
    else:
        print(f"  [FAIL] Expected total=8, got: {result}")
except Exception as e:
    print(f"  [FAIL] parse_test_results raised: {e}")

total += 1
try:
    result = parse_test_results(SAMPLE_PYTEST_OUTPUT)
    if isinstance(result, dict) and result.get("passed") == 6 and result.get("failed") == 1:
        print(f"  [PASS] parse_test_results found passed=6, failed=1")
        score += 1
    else:
        print(f"  [FAIL] Expected passed=6, failed=1, got: {result}")
except Exception as e:
    print(f"  [FAIL] parse_test_results raised: {e}")

total += 1
try:
    result = parse_test_results(SAMPLE_PYTEST_OUTPUT)
    failing = result.get("failing_tests", []) if isinstance(result, dict) else []
    if len(failing) == 2:
        print(f"  [PASS] parse_test_results found 2 failing/error tests")
        score += 1
    else:
        print(f"  [FAIL] Expected 2 failing tests, got {len(failing)}: {failing}")
except Exception as e:
    print(f"  [FAIL] parse_test_results raised: {e}")

total += 1
try:
    result = parse_test_results(SAMPLE_ALL_PASS_OUTPUT)
    if isinstance(result, dict) and result.get("passed") == 3 and result.get("failed") == 0:
        print(f"  [PASS] parse_test_results handles all-pass output")
        score += 1
    else:
        print(f"  [FAIL] All-pass output: {result}")
except Exception as e:
    print(f"  [FAIL] parse_test_results raised: {e}")


# ── TODO 3: Generate Test Report ───────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement generate_test_report(results)")
print("=" * 70)

print("""
Given a list of test result dicts (from run_tests), generate a summary report.

Return a dict with:
  - summary: str like "5 tests: 3 passed, 1 failed, 1 error"
  - pass_rate: float (0.0 to 100.0), e.g., 60.0
  - failing_tests: list of dicts with "name" and "detail" for failed/error tests
  - status: "all_passed" if pass_rate == 100.0, else "has_failures"
""")


def generate_test_report(results: list) -> dict:
    """Generate a test report from run_tests results."""
    total_count = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    error = sum(1 for r in results if r["status"] == "error")

    pass_rate = (passed / total_count) * 100 if total_count > 0 else 0.0

    failing_tests = [
        {"name": r["name"], "detail": r["detail"]}
        for r in results if r["status"] != "passed"
    ]

    summary = f"{total_count} tests: {passed} passed, {failed} failed, {error} error"
    status = "all_passed" if pass_rate == 100.0 else "has_failures"

    return {
        "summary": summary,
        "pass_rate": pass_rate,
        "failing_tests": failing_tests,
        "status": status,
    }


# Validate TODO 3
total += 1
try:
    test_results = [
        {"name": "test_a", "status": "passed", "detail": None},
        {"name": "test_b", "status": "failed", "detail": "assertion error"},
        {"name": "test_c", "status": "passed", "detail": None},
        {"name": "test_d", "status": "error", "detail": "zero division"},
    ]
    report = generate_test_report(test_results)
    if isinstance(report, dict) and report.get("pass_rate") == 50.0:
        print(f"  [PASS] generate_test_report pass_rate=50.0")
        score += 1
    else:
        print(f"  [FAIL] Expected pass_rate=50.0, got: {report}")
except Exception as e:
    print(f"  [FAIL] generate_test_report raised: {e}")

total += 1
try:
    report = generate_test_report(test_results)
    if isinstance(report, dict) and len(report.get("failing_tests", [])) == 2:
        print(f"  [PASS] generate_test_report found 2 failing tests")
        score += 1
    else:
        print(f"  [FAIL] Expected 2 failing tests: {report}")
except Exception as e:
    print(f"  [FAIL] generate_test_report raised: {e}")

total += 1
try:
    all_pass = [
        {"name": "test_x", "status": "passed", "detail": None},
        {"name": "test_y", "status": "passed", "detail": None},
    ]
    report = generate_test_report(all_pass)
    if isinstance(report, dict) and report.get("status") == "all_passed":
        print(f"  [PASS] generate_test_report returns 'all_passed' for 100%")
        score += 1
    else:
        print(f"  [FAIL] Expected status='all_passed': {report}")
except Exception as e:
    print(f"  [FAIL] generate_test_report raised: {e}")


# ── Write Report ──────────────────────────────────────────────────
print()
print("=" * 70)
print("Writing Test Report")
print("=" * 70)

try:
    funcs = [test_addition, test_string_upper, test_list_append, test_division_by_zero, test_type_check]
    raw_results = run_tests(funcs) if callable(run_tests) else []
    final_report = generate_test_report(raw_results) if callable(generate_test_report) and isinstance(raw_results, list) else {}
except Exception:
    final_report = {}

report_path = os.path.join(WORKDIR, "test_report.json")
with open(report_path, "w") as f:
    json.dump(final_report, f, indent=2, default=str)
print(f"  Report written to: {report_path}")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 02 Score: {score}/{total}")
print("=" * 70)
