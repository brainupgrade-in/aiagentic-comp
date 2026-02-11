"""
Lab 01 Solution: Coding Agent Anatomy
=======================================
"""

import os
import shutil
import json

WORKDIR = "/tmp/aidev-lab-10-01"

print("=" * 50)
print("  Lab 01: Coding Agent Anatomy (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: The 5 Phases of a Coding Agent
# ============================================================

print("\n--- Step 1: The 5 Phases of a Coding Agent ---\n")

phases = [
    ("1. Plan",     "Analyse the request, break into sub-tasks",
     "Read the codebase, identify files to change"),
    ("2. Code",     "Generate or modify source code",
     "Write new functions, edit existing files"),
    ("3. Test",     "Run tests or linters to verify correctness",
     "Execute unit tests, type-check, lint"),
    ("4. Reflect",  "Evaluate test results, diagnose failures",
     "Parse error messages, compare expected vs actual"),
    ("5. Iterate",  "Loop back to Plan or Code if issues remain",
     "Retry with improved approach, max N iterations"),
]

print(f"  {'Phase':<14} {'Purpose':<45} {'Examples'}")
print(f"  {'-'*100}")
for phase, purpose, examples in phases:
    print(f"  {phase:<14} {purpose:<45} {examples}")

print("""
  The agent keeps looping through phases 1-5 until:
    a) All tests pass  (success)
    b) Max iterations reached  (give up gracefully)
    c) User interrupts  (manual override)
""")


# ============================================================
# Step 2: Tool Registry
# ============================================================

print("\n--- Step 2: Tool Registry ---\n")

example_registry = {
    "read_file":    {"description": "Read file contents",          "params": ["path"]},
    "write_file":   {"description": "Write content to file",       "params": ["path", "content"]},
    "run_tests":    {"description": "Execute test suite",          "params": ["test_path"]},
    "search_code":  {"description": "Grep for a pattern in files", "params": ["pattern", "directory"]},
    "list_files":   {"description": "List files in a directory",   "params": ["directory"]},
}

print(f"  {'Tool':<14} {'Description':<35} {'Parameters'}")
print(f"  {'-'*70}")
for name, info in example_registry.items():
    print(f"  {name:<14} {info['description']:<35} {', '.join(info['params'])}")


# ============================================================
# Step 3: Agent Loop Pseudocode
# ============================================================

print("\n\n--- Step 3: Agent Loop Pseudocode ---\n")

pseudocode = """
  def agent_loop(request, max_iterations=5):
      context = gather_context(request)       # read relevant files
      plan = create_plan(request, context)     # break into steps

      for i in range(max_iterations):
          code_changes = generate_code(plan)   # LLM writes code
          apply_changes(code_changes)          # write to disk

          test_results = run_tests()           # execute tests
          if test_results.all_passed:
              return "success"                 # done!

          diagnosis = reflect(test_results)    # analyse failures
          plan = revise_plan(plan, diagnosis)  # update the plan

      return "max iterations reached"          # give up
"""
print(pseudocode)


# ============================================================
# TODO 1 Solution: Fill in the 5 phases in order
# ============================================================

print("\n--- TODO 1: Name the 5 Phases in Order ---\n")

agent_phases = [
    "plan",       # Phase 1
    "code",       # Phase 2
    "test",       # Phase 3
    "reflect",    # Phase 4
    "iterate",    # Phase 5
]

correct_phases = ["plan", "code", "test", "reflect", "iterate"]

score1 = 0
for i, (student, correct) in enumerate(zip(agent_phases, correct_phases), 1):
    if student == "___":
        status = "TODO"
    elif student.strip().lower() == correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Phase {i}: {student}")

print(f"\n  Score: {score1}/{len(correct_phases)}")


# ============================================================
# TODO 2 Solution: Build a tool registry
# ============================================================

print("\n\n--- TODO 2: Build a Tool Registry ---\n")

tool_registry = {
    "read_file":  "Read file contents",
    "write_file": "Write content to file",
    "run_tests":  "Execute test suite",
}

score2 = 0
checks_2 = []

if isinstance(tool_registry, dict):
    checks_2.append(("Registry is a dict", "PASS"))
    score2 += 1
else:
    checks_2.append(("Registry is a dict", "FAIL"))

for key in ["read_file", "write_file", "run_tests"]:
    if isinstance(tool_registry, dict) and key in tool_registry:
        checks_2.append((f"Has {key}", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Has {key}", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score2}/4")


# ============================================================
# TODO 3 Solution: What happens when tests fail?
# ============================================================

print("\n\n--- TODO 3: What Happens When Tests Fail? ---\n")

on_test_failure = "reflect"

correct_answer = "reflect"

if on_test_failure.strip().lower() == correct_answer:
    status3 = "PASS"
    score3 = 1
else:
    status3 = "FAIL"
    score3 = 0

print(f"    [{status3}] On test failure, go to: {on_test_failure}")
print(f"\n  Score: {score3}/1")


# ============================================================
# Save reference document
# ============================================================

ref = {
    "phases": correct_phases,
    "phase_details": {p[0].split(". ")[1]: p[1] for p in phases},
    "tool_registry_example": example_registry,
    "on_test_failure": "reflect",
}

with open(os.path.join(WORKDIR, "agent-anatomy-reference.json"), "w") as f:
    json.dump(ref, f, indent=2)


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = len(correct_phases) + 4 + 1

print(f"\n\n{'='*50}")
print(f"  Lab 01 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Coding agents loop: Plan -> Code -> Test -> Reflect -> Iterate")
print(f"    2. Tools are registered in a dict (name -> description + params)")
print(f"    3. On test failure the agent reflects before retrying")
print(f"\n  TODO 1: {score1}/{len(correct_phases)} phases correct")
print(f"  TODO 2: {score2}/4 registry checks passed")
print(f"  TODO 3: {score3}/1 failure handling correct")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
