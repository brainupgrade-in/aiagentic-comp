"""
Lab 06 Solution: Agent Comparison
====================================
"""

import os
import shutil
import json

WORKDIR = "/tmp/aidev-lab-10-06"

print("=" * 50)
print("  Lab 06: Agent Comparison (Solution)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Feature Matrix
# ============================================================

print("\n--- Step 1: AI Coding Agent Feature Matrix ---\n")

features = [
    "Context window",
    "Agentic (plan/code/test loop)",
    "Multi-file editing",
    "Terminal access",
    "IDE integration",
    "Cost (free tier)",
    "Privacy / local option",
    "Custom instructions (CLAUDE.md)",
]

agents = ["Claude Code", "GitHub Copilot", "Cursor", "OpenCode"]

reference_matrix = {
    "Claude Code":     [5, 5, 5, 5, 3, 3, 2, 5],
    "GitHub Copilot":  [4, 3, 4, 3, 5, 4, 2, 3],
    "Cursor":          [5, 4, 5, 4, 5, 3, 2, 4],
    "OpenCode":        [4, 4, 4, 5, 2, 5, 4, 3],
}

print(f"  {'Feature':<35}", end="")
for agent in agents:
    print(f" {agent:<16}", end="")
print()
print(f"  {'-'*100}")
for i, feature in enumerate(features):
    print(f"  {feature:<35}", end="")
    for agent in agents:
        print(f" {reference_matrix[agent][i]:<16}", end="")
    print()

print("\n  Scale: 1 = poor, 2 = basic, 3 = decent, 4 = good, 5 = excellent")


# ============================================================
# Step 2: Weighted Scoring Rubric
# ============================================================

print("\n\n--- Step 2: Weighted Scoring Rubric ---\n")

weights = {
    "Context window":                   0.15,
    "Agentic (plan/code/test loop)":    0.20,
    "Multi-file editing":               0.15,
    "Terminal access":                   0.10,
    "IDE integration":                  0.10,
    "Cost (free tier)":                 0.10,
    "Privacy / local option":           0.10,
    "Custom instructions (CLAUDE.md)":  0.10,
}

print(f"  {'Feature':<35} {'Weight'}")
print(f"  {'-'*50}")
for feature, weight in weights.items():
    print(f"  {feature:<35} {weight:.0%}")


# ============================================================
# TODO 1 Solution: Fill in feature scores
# ============================================================

print("\n\n--- TODO 1: Score Each Agent ---\n")

student_scores = {
    "Claude Code":     [5, 5, 5, 5, 3, 3, 2, 5],
    "GitHub Copilot":  [4, 3, 4, 3, 5, 4, 2, 3],
    "Cursor":          [5, 4, 5, 4, 5, 3, 2, 4],
    "OpenCode":        [4, 4, 4, 5, 2, 5, 4, 3],
}

score1 = 0
checks_1 = []

all_filled = all(isinstance(v, list) for v in student_scores.values())
if all_filled:
    checks_1.append(("All agents have scores", "PASS"))
    score1 += 1
else:
    checks_1.append(("All agents have scores", "FAIL"))

all_valid = all(
    isinstance(v, list) and all(isinstance(s, int) and 1 <= s <= 5 for s in v)
    for v in student_scores.values()
)
if all_valid:
    checks_1.append(("Scores are valid (1-5)", "PASS"))
    score1 += 1
else:
    checks_1.append(("Scores are valid (1-5)", "FAIL"))

all_8 = all(isinstance(v, list) and len(v) == 8 for v in student_scores.values())
if all_8:
    checks_1.append(("Each agent has 8 scores", "PASS"))
    score1 += 1
else:
    checks_1.append(("Each agent has 8 scores", "FAIL"))

for check, status in checks_1:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score1}/3")


# ============================================================
# TODO 2 Solution: Calculate weighted scores and rank
# ============================================================

print("\n\n--- TODO 2: Calculate Weighted Scores ---\n")

def calculate_rankings(scores_dict, weights_dict, feature_list):
    """Calculate weighted scores and rank agents."""
    rankings = []
    for agent_name, scores in scores_dict.items():
        weighted_score = 0.0
        for i, feature in enumerate(feature_list):
            weighted_score += scores[i] * weights_dict[feature]
        rankings.append((agent_name, round(weighted_score, 2)))
    rankings.sort(key=lambda x: x[1], reverse=True)
    return rankings


score2 = 0
checks_2 = []

r1 = calculate_rankings(reference_matrix, weights, features)

if isinstance(r1, list) and len(r1) == 4:
    checks_2.append(("Returns a list of tuples", "PASS"))
    score2 += 1
else:
    checks_2.append(("Returns a list of tuples", "FAIL"))

if isinstance(r1, list) and len(r1) > 0 and isinstance(r1[0], tuple) and len(r1[0]) == 2:
    checks_2.append(("Tuples have (name, score)", "PASS"))
    score2 += 1
else:
    checks_2.append(("Tuples have (name, score)", "FAIL"))

if isinstance(r1, list) and len(r1) >= 2:
    scores_list = [t[1] for t in r1 if isinstance(t, tuple) and len(t) == 2]
    if scores_list == sorted(scores_list, reverse=True):
        checks_2.append(("Sorted by score descending", "PASS"))
        score2 += 1
    else:
        checks_2.append(("Sorted by score descending", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

print(f"\n  Rankings:")
for rank, (name, wscore) in enumerate(r1, 1):
    print(f"    {rank}. {name:<18} weighted score: {wscore}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3 Solution: Write a recommendation
# ============================================================

print("\n\n--- TODO 3: Write a Recommendation ---\n")

recommendation = (
    "For a team of 5 developers building a FastAPI microservice, "
    "I recommend Claude Code because it excels at agentic workflows "
    "(plan/code/test loop), offers best-in-class multi-file editing, "
    "and supports custom CLAUDE.md instructions for project-specific conventions. "
    "While Cursor offers comparable IDE integration, Claude Code's stronger "
    "agentic capability provides more autonomy for complex refactoring tasks."
)

score3 = 0
checks_3 = []

if len(recommendation) >= 30:
    checks_3.append(("Recommendation provided (30+ chars)", "PASS"))
    score3 += 1
else:
    checks_3.append(("Recommendation provided", "FAIL"))

rec_lower = recommendation.lower()
mentions_agent = any(a.lower() in rec_lower for a in agents)
if mentions_agent:
    checks_3.append(("Mentions an agent by name", "PASS"))
    score3 += 1
else:
    checks_3.append(("Mentions an agent by name", "FAIL"))

has_reason = any(kw in rec_lower for kw in ["because", "since", "due to", "supports", "offers",
                                              "provides", "best", "strong", "excels", "for"])
if has_reason:
    checks_3.append(("Gives a reason", "PASS"))
    score3 += 1
else:
    checks_3.append(("Gives a reason", "FAIL"))

for check, status in checks_3:
    print(f"    [{status}] {check}")

print(f"\n  Score: {score3}/3")


# ============================================================
# Save reference
# ============================================================

ref = {
    "agents": agents,
    "features": features,
    "weights": weights,
    "reference_scores": reference_matrix,
}

with open(os.path.join(WORKDIR, "agent-comparison-reference.json"), "w") as f:
    json.dump(ref, f, indent=2)


# ============================================================
# Summary
# ============================================================

total = score1 + score2 + score3
max_total = 3 + 3 + 3

print(f"\n\n{'='*50}")
print(f"  Lab 06 Summary (Solution)")
print(f"{'='*50}")
print(f"  Key concepts:")
print(f"    1. Feature matrices help compare tools objectively")
print(f"    2. Weighted scoring accounts for what matters to YOUR team")
print(f"    3. Recommendations should match the specific use case and priorities")
print(f"\n  TODO 1: {score1}/3 scoring checks passed")
print(f"  TODO 2: {score2}/3 ranking checks passed")
print(f"  TODO 3: {score3}/3 recommendation checks passed")
print(f"\n  Total: {total}/{max_total}")
print(f"\n  Files generated in {WORKDIR}/")
