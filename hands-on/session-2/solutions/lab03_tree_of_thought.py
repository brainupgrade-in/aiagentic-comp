"""
Lab 03: Tree-of-Thought — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# Step 1: Single path
print("=" * 60)
print("CoT: ONE Solution Path")
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

# Step 2: Generate 3 paths
print("=" * 60)
print("ToT: THREE Solution Paths")
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
approaches = response.content
print(f"Three Approaches:\n{approaches}\n")

# Step 3: Evaluate
print("=" * 60)
print("Evaluation")
print("=" * 60)

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

# TODO 1: Debugging ToT
print("=" * 60)
print("TODO 1: Debugging ToT")
print("=" * 60)

debug_problem = "A Python web app is running slow. Page load takes 8 seconds instead of the expected 1 second."

# Step 1: Generate hypotheses
print("--- Step 1: Generate root cause hypotheses ---")
hypotheses = llm.invoke([
    SystemMessage(content="""You are a senior backend developer debugging a performance issue.
Generate exactly 3 possible root causes. For each:
- Name the cause
- Explain why it could cause slow page loads
- Suggest how to verify this hypothesis
Keep each to 2-3 sentences."""),
    HumanMessage(content=debug_problem),
]).content
print(f"{hypotheses}\n")

# Step 2: Evaluate which is most likely
print("--- Step 2: Evaluate most likely cause ---")
evaluation = llm.invoke([
    SystemMessage(content="Based on common web app issues, which root cause is MOST likely? Explain your reasoning in 2-3 sentences."),
    HumanMessage(content=f"Problem: {debug_problem}\n\nPossible causes:\n{hypotheses}"),
]).content
print(f"{evaluation}\n")

# Step 3: Fix for most likely cause
print("--- Step 3: Suggest fix ---")
fix = llm.invoke([
    SystemMessage(content="Provide a specific, actionable fix for this issue. Include example code or commands if applicable. Keep it concise."),
    HumanMessage(content=f"Root cause analysis:\n{evaluation}"),
]).content
print(f"{fix}\n")

# TODO 2: Voting-based ToT
print("=" * 60)
print("TODO 2: Voting-Based Evaluation")
print("=" * 60)

design_question = """We need to add caching to our Python web API.
Options: A) Redis, B) In-memory (functools.lru_cache), C) Memcached.
We have a single server, 8GB RAM, and moderate traffic (1000 req/min)."""

votes = {"A": 0, "B": 0, "C": 0}

for round_num in range(1, 4):
    response = llm.invoke([
        SystemMessage(content="You are a senior engineer. Pick the BEST caching option (A, B, or C) for this scenario. Start your response with the letter of your choice."),
        HumanMessage(content=design_question),
    ])
    answer = response.content.strip()
    print(f"Round {round_num}: {answer[:80]}...")

    # Count the vote
    for letter in ["A", "B", "C"]:
        if answer.upper().startswith(letter) or f"option {letter}" in answer.upper() or f"({letter})" in answer.upper():
            votes[letter] += 1
            break

print(f"\nVotes: {votes}")
winner = max(votes, key=lambda k: votes[k])
print(f"Winner: Option {winner} with {votes[winner]} votes")
