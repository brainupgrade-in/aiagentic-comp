# Medium Priority Improvements

Enhance value and engagement. Consider for this delivery or future iterations.

## 1. Add Agent Evaluation/Testing Methodology

**Where:** Session 14 (AI Safety & Guardrails) — add 2-3 slides
**What:** Cover systematic agent quality measurement:
- Accuracy metrics: how to measure if agents give correct answers
- Regression testing: golden dataset of question/expected-answer pairs
- A/B testing agents: compare two prompt versions on same inputs
- Evaluation frameworks: brief mention of LangSmith, RAGAS, custom eval harnesses
**Why:** Enterprise teams need "how do we know this works?" not just "how do we build it?" Safety testing (already covered) is one dimension; quality evaluation is another.
**Effort:** ~1 hour

## 2. Add Internal Tooling Use Cases

**Where:** Session 1 (Introduction) or Session 2 (Coding Assistants) — add 1-2 slides
**What:** Enterprise-developer-specific agent use cases:
- "AI agent that helps onboard new developers by answering questions about your codebase"
- "Agent that monitors CI/CD pipeline failures and suggests fixes"
- "Code review assistant that checks for security vulnerabilities and style violations"
- "Documentation agent that generates API docs from code comments"
- "Incident response agent that correlates logs, metrics, and traces to suggest root cause"
**Why:** Participants will think "cool technology, but what do I build with it on Monday?" These use cases are directly actionable for enterprise developers.
**Effort:** ~30 minutes

## 3. Add Peer Collaboration Exercises

**Where:**
- Day 3 (after Session 8): 15-minute "Design Review" — pairs critique each other's LangGraph workflow designs
- Day 5 (Session 14): Group red-teaming exercise — teams try to break each other's safety layers
**What:** Structured group activities that break up the solo-coding pattern. Provide templates/rubrics for the reviews.
**Why:** 5 days of solo notebook work gets tiring. Peer exercises increase engagement, build team rapport, and expose participants to different thinking styles.
**Effort:** ~1 hour (create templates and instructions)

## 4. Add CI/CD Patterns for AI Services

**Where:** Session 11 (Production) or Session 15 (Capstone) — add 1-2 slides
**What:**
- How to version-control prompts (prompt registry, git-tracked templates)
- Prompt regression tests in CI pipeline (golden dataset + automated eval)
- Model versioning: pinning model versions in config, not code
- Blue/green deployment for AI services (gradual rollout)
**Why:** DevOps-background participants will ask "how do we CI/CD this?" Standard software CI/CD doesn't cover prompt versioning or model swaps.
**Effort:** ~45 minutes

## 5. Add Indian Regulatory Context to Safety Session

**Where:** Session 14 (AI Safety & Guardrails)
**What:** Beyond the DPDPA reference (must-do), add context on:
- RBI guidelines for AI in financial services (relevant if any participants work on fintech)
- CERT-In incident reporting requirements for AI-related breaches
- MEITY's responsible AI framework
- Brief comparison table: GDPR vs DPDPA vs CCPA key differences
**Why:** Shows the course understands participants' regulatory environment. Makes the safety content feel locally relevant, not just a Western compliance checklist.
**Effort:** ~45 minutes
