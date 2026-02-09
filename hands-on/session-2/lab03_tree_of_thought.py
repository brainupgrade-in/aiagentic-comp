"""
Lab 03: Tree-of-Thought (ToT)
===============================
Goal: Explore multiple solution paths, evaluate each, and pick the best.

What you'll learn:
- CoT follows ONE path; ToT explores MULTIPLE paths
- How to generate multiple approaches to a problem
- How to evaluate and score each approach
- When ToT is worth the extra cost
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Single path (Chain-of-Thought) — one attempt
# ============================================================

print("=" * 60)
print("Chain-of-Thought: ONE Solution Path")
print("=" * 60)

problem = """A small startup has 3 developers and needs to build:
1. A REST API backend
2. A mobile app
3. A landing page website

They have 8 weeks. How should they organize the work?"""

response = llm.invoke([
    SystemMessage(content="You are a project manager. Think step by step and propose a plan."),
    HumanMessage(content=problem),
])
print(f"Single Plan:\n{response.content}\n")

# ============================================================
# Step 2: Tree-of-Thought — generate multiple paths
# ============================================================
# Ask the LLM to brainstorm 3 different approaches.

print("=" * 60)
print("Tree-of-Thought: THREE Solution Paths")
print("=" * 60)

response = llm.invoke([
    SystemMessage(content="""You are a project manager. Generate exactly 3 DIFFERENT approaches to solve this problem.

For each approach:
- Label it (Approach A, B, C)
- Describe the strategy in 2-3 sentences
- List one key advantage and one key risk

Keep each approach concise."""),
    HumanMessage(content=problem),
])
print(f"Three Approaches:\n{response.content}\n")

# ============================================================
# Step 3: Evaluate and score each path
# ============================================================
# Now ask the LLM to be a critic and evaluate the approaches.

print("=" * 60)
print("Evaluation: Score Each Path")
print("=" * 60)

approaches = response.content  # The three approaches from above

response = llm.invoke([
    SystemMessage(content="""You are a senior engineering director evaluating project plans.

Score each approach on these criteria (1-10):
- Feasibility: Can 3 developers realistically do this in 8 weeks?
- Risk: How likely is it to fail?
- Speed to market: How fast do they get something usable?

Give a total score and pick the BEST approach. Be critical."""),
    HumanMessage(content=f"Here are 3 approaches to evaluate:\n\n{approaches}"),
])
print(f"Evaluation:\n{response.content}\n")

# ============================================================
# Step 4: Compare CoT vs ToT on a design decision
# ============================================================

print("=" * 60)
print("Design Decision: CoT vs ToT")
print("=" * 60)

design_question = """We need to add user authentication to our web app.
The app uses Python/FastAPI backend and React frontend.
We have 2 weeks and 1 developer.
What approach should we use?"""

# CoT: Single approach
print("--- CoT (single path) ---")
cot_response = llm.invoke([
    SystemMessage(content="You are a senior developer. Recommend one approach. Think step by step."),
    HumanMessage(content=design_question),
])
print(f"{cot_response.content}\n")

# ToT: Multiple approaches → evaluate → pick best
print("--- ToT Step 1: Generate options ---")
options = llm.invoke([
    SystemMessage(content="""Generate 3 different authentication approaches. For each:
- Name the approach (e.g., "JWT + Custom", "OAuth2 + Google", "Firebase Auth")
- One sentence on how it works
- Time estimate
- Difficulty: Easy/Medium/Hard"""),
    HumanMessage(content=design_question),
])
print(f"{options.content}\n")

print("--- ToT Step 2: Evaluate and pick ---")
best = llm.invoke([
    SystemMessage(content="""You are evaluating authentication approaches for a 2-week, 1-developer project.
Pick the BEST option considering: time constraint, developer experience (assume mid-level), and long-term maintainability.
Explain your choice in 2-3 sentences."""),
    HumanMessage(content=f"Options:\n{options.content}"),
])
print(f"Best choice:\n{best.content}")

# ============================================================
# TODO 1: ToT for a debugging scenario
# ============================================================
# Problem: "A Python web app is running slow. Page load takes 8 seconds."
#
# Step 1: Ask the LLM to generate 3 possible root causes
# Step 2: Ask the LLM to evaluate which is most likely
# Step 3: Ask for a fix for the most likely cause
#
# This mirrors how experienced developers debug — they consider
# multiple hypotheses before jumping to a solution.

# TODO: Implement the 3-step debugging ToT

# ============================================================
# TODO 2: ToT with self-voting
# ============================================================
# Instead of one evaluation pass, run the evaluation 3 times
# and count "votes" for each approach. This reduces bias.
#
# Hint: Call the evaluation prompt 3 times and count which
# approach wins each time. Majority wins.

# TODO: Implement voting-based ToT

print("\n" + "=" * 60)
print("Lab 03 complete! Key takeaways:")
print("- CoT = one path. ToT = multiple paths + evaluation")
print("- ToT: Generate options → Evaluate → Pick best")
print("- More expensive (3x+ LLM calls) but better for complex decisions")
print("- Best for: architecture choices, debugging, planning")
print("- Not needed for simple factual questions")
