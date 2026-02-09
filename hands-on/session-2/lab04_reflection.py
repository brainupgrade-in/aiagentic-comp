"""
Lab 04: Reflection Pattern
============================
Goal: Build a Generate → Critique → Improve loop.

What you'll learn:
- First drafts from LLMs are often "good enough" but not great
- Self-critique makes the output significantly better
- The reflection loop: Generate → Critique → Improve → (Repeat)
- How this pattern is used in real code generation and writing
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Generate a first draft (no reflection)
# ============================================================

print("=" * 60)
print("Step 1: GENERATE — First Draft")
print("=" * 60)

task = "Write a Python function that checks if a string is a palindrome."

first_draft = llm.invoke([
    SystemMessage(content="You are a Python developer. Write clean, working code. Include a brief docstring."),
    HumanMessage(content=task),
])
print(f"First Draft:\n{first_draft.content}\n")

# ============================================================
# Step 2: Critique the first draft
# ============================================================
# Now ask a different "persona" to review the code critically.

print("=" * 60)
print("Step 2: CRITIQUE — Find Issues")
print("=" * 60)

critique = llm.invoke([
    SystemMessage(content="""You are a senior code reviewer. Review the code below and list specific issues.
Check for:
- Bugs or edge cases not handled (empty string, None, mixed case, spaces)
- Code style and readability
- Missing error handling
- Performance concerns
Be specific and constructive. List each issue as a bullet point."""),
    HumanMessage(content=f"Review this code:\n\n{first_draft.content}"),
])
print(f"Critique:\n{critique.content}\n")

# ============================================================
# Step 3: Improve based on critique
# ============================================================
# Feed both the original code AND the critique back to the generator.

print("=" * 60)
print("Step 3: IMPROVE — Revised Version")
print("=" * 60)

improved = llm.invoke([
    SystemMessage(content="You are a Python developer. Rewrite the code to address ALL the issues found in the review. Show the complete improved function."),
    HumanMessage(content=f"Original code:\n{first_draft.content}\n\nReview feedback:\n{critique.content}\n\nRewrite the code to fix all issues."),
])
print(f"Improved Version:\n{improved.content}\n")

# ============================================================
# Step 4: Automated reflection loop
# ============================================================
# Let's automate the generate → critique → improve cycle.

print("=" * 60)
print("Automated Reflection Loop (2 iterations)")
print("=" * 60)

writing_task = "Write a professional email to a client explaining that the project will be delayed by 2 weeks due to unexpected technical issues."

# Generate first draft
current_draft = llm.invoke([
    SystemMessage(content="You are a business communication expert. Write a professional, empathetic email. Keep it to one short paragraph."),
    HumanMessage(content=writing_task),
]).content

print(f"[Draft 1]\n{current_draft}\n")

# Reflection loop
for iteration in range(1, 3):
    print(f"--- Reflection round {iteration} ---")

    # Critique
    critique = llm.invoke([
        SystemMessage(content="""Critique this email. Be specific about:
- Tone: Is it professional but empathetic?
- Clarity: Is the delay reason clear?
- Action items: Does it offer a revised timeline?
- Missing: What should be added or removed?
List 2-3 specific improvements."""),
        HumanMessage(content=f"Email draft:\n{current_draft}"),
    ]).content
    print(f"Critique: {critique}\n")

    # Improve
    current_draft = llm.invoke([
        SystemMessage(content="Rewrite the email incorporating ALL the feedback. Keep it professional and concise. One short paragraph."),
        HumanMessage(content=f"Current draft:\n{current_draft}\n\nFeedback:\n{critique}"),
    ]).content
    print(f"[Draft {iteration + 1}]\n{current_draft}\n")

print("[Final email is above — notice how each iteration improves it]")

# ============================================================
# TODO 1: Reflection for a technical explanation
# ============================================================
# Task: "Explain Docker to a non-technical manager in 3 sentences."
#
# Run the Generate → Critique → Improve loop.
# For the critique, check:
#   - Are there any jargon words a non-tech person wouldn't understand?
#   - Is the analogy clear and relatable?
#   - Is it exactly 3 sentences?

# TODO: Implement the reflection loop

# ============================================================
# TODO 2: Multi-round reflection with a stopping condition
# ============================================================
# Run the reflection loop up to 5 times, but STOP EARLY if the
# critique says "no major issues found" or similar.
#
# Hint: Check if the critique contains phrases like "no issues",
# "looks good", "no major" and break out of the loop.

# TODO: Implement reflection with early stopping

# ============================================================
# TODO 3: Reflection for code — fix a buggy function
# ============================================================
# Give the LLM this buggy code and use reflection to fix it:
#
#   def fibonacci(n):
#       if n <= 0:
#           return 0
#       if n == 1:
#           return 1
#       return fibonacci(n-1) + fibonacci(n-2)
#
# Issues: no memoization (exponential time), no negative handling.
# Use critique to find issues, then improve to fix them.

# TODO: Implement

print("\n" + "=" * 60)
print("Lab 04 complete! Key takeaways:")
print("- First drafts are rarely optimal — reflection improves them")
print("- The loop: Generate → Critique → Improve → (repeat)")
print("- Different 'personas' for generation vs critique work best")
print("- 2-3 iterations usually enough; diminishing returns after")
print("- Great for: code, writing, explanations, design decisions")
