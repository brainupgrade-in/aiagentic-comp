"""
Lab 06: Agent Comparison
==========================
Compare AI coding agents across key features — build a scoring
matrix, calculate weighted rankings, and make recommendations.

What you'll learn:
- Feature matrices for comparing AI coding tools
- Weighted scoring and ranking methodology
- Writing actionable recommendations

No API key needed — pure Python standard library.
"""

import os
import shutil
import json

WORKDIR = "/tmp/aidev-lab-02-06"

print("=" * 50)
print("  Lab 06: Agent Comparison")
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

# Reference scores (public knowledge)
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
# Step 2: Scoring Rubric
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
print(f"\n  Total: {sum(weights.values()):.0%}")


# ============================================================
# TODO 1: Fill in feature scores for each agent
# ============================================================

print("\n\n--- TODO 1: Score Each Agent ---\n")

print("  Rate each agent on each feature (1-5 scale).")
print("  Use your knowledge or the reference matrix above.\n")

# YOUR CODE HERE: Fill in the scores (replace "___" lists with actual scores)
# Each list should have 8 integers (one per feature), values 1-5.
student_scores = {
    "Claude Code":     "___",
    "GitHub Copilot":  "___",
    "Cursor":          "___",
    "OpenCode":        "___",
}

score1 = 0
checks_1 = []

if student_scores["Claude Code"] == "___":
    checks_1.append(("All agents have scores", "TODO"))
    checks_1.append(("Scores are valid (1-5)", "TODO"))
    checks_1.append(("Each agent has 8 scores", "TODO"))
else:
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
# TODO 2: Calculate weighted scores and rank
# ============================================================

print("\n\n--- TODO 2: Calculate Weighted Scores ---\n")

print("  Using the weights from Step 2 and your scores from TODO 1,")
print("  calculate a weighted total for each agent and rank them.\n")

# YOUR CODE HERE: Replace the body with a real implementation
def calculate_rankings(scores_dict, weights_dict, feature_list):
    """
    Calculate weighted scores and rank agents.

    Args:
        scores_dict: dict mapping agent name -> list of scores (int)
        weights_dict: dict mapping feature name -> weight (float)
        feature_list: list of feature names (in same order as scores)

    Returns:
        list of tuples [(agent_name, weighted_score), ...] sorted by score descending
    """
    # TODO: For each agent, compute: sum(score[i] * weight[feature_list[i]]) for all i
    # TODO: Sort by weighted_score descending
    # TODO: Return list of (agent_name, round(weighted_score, 2)) tuples
    return "___"


score2 = 0
checks_2 = []

# Use reference_matrix for validation regardless of student_scores
r1 = calculate_rankings(reference_matrix, weights, features)

if r1 == "___":
    checks_2.append(("Returns a list of tuples", "TODO"))
    checks_2.append(("Tuples have (name, score)", "TODO"))
    checks_2.append(("Sorted by score descending", "TODO"))
else:
    if isinstance(r1, list) and len(r1) == 4:
        checks_2.append(("Returns a list of tuples", "PASS"))
        score2 += 1
    else:
        checks_2.append((f"Returns a list of tuples (got {type(r1).__name__}, len={len(r1) if isinstance(r1, list) else '?'})", "FAIL"))

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
            checks_2.append((f"Sorted by score descending (got {scores_list})", "FAIL"))

for check, status in checks_2:
    print(f"    [{status}] {check}")

if isinstance(r1, list) and len(r1) > 0 and isinstance(r1[0], tuple):
    print(f"\n  Rankings:")
    for rank, (name, wscore) in enumerate(r1, 1):
        print(f"    {rank}. {name:<18} weighted score: {wscore}")

print(f"\n  Score: {score2}/3")


# ============================================================
# TODO 3: Write a recommendation
# ============================================================

print("\n\n--- TODO 3: Write a Recommendation ---\n")

print("  Given use case: 'A team of 5 developers building a FastAPI microservice'")
print("  with priorities: agentic capability, multi-file editing, cost.\n")
print("  Write a recommendation string (at least 30 characters) explaining")
print("  which agent you'd recommend and why.\n")

# YOUR CODE HERE: Replace "___" with your recommendation
recommendation = "___"

score3 = 0
checks_3 = []

if recommendation == "___":
    checks_3.append(("Recommendation provided", "TODO"))
    checks_3.append(("Mentions an agent by name", "TODO"))
    checks_3.append(("Gives a reason", "TODO"))
else:
    if len(recommendation) >= 30:
        checks_3.append(("Recommendation provided (30+ chars)", "PASS"))
        score3 += 1
    else:
        checks_3.append((f"Recommendation provided (got {len(recommendation)} chars, need 30+)", "FAIL"))

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
print(f"  Lab 06 Summary")
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
