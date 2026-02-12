"""
Lab 04: Reflection Pattern — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# Step 1: Generate first draft
print("=" * 60)
print("Step 1: GENERATE")
print("=" * 60)

task = "Write a Python function that checks if a string is a palindrome."

first_draft = llm.invoke([
    SystemMessage(content="You are a Python developer. Write clean, working code. Include a brief docstring."),
    HumanMessage(content=task),
])
print(f"First Draft:\n{first_draft.content}\n")

# Step 2: Critique
print("=" * 60)
print("Step 2: CRITIQUE")
print("=" * 60)

critique = llm.invoke([
    SystemMessage(content="""You are a senior code reviewer. Review the code and list specific issues.
Check for: bugs, edge cases (empty string, None, mixed case, spaces), style, error handling, performance.
Be specific and constructive."""),
    HumanMessage(content=f"Review this code:\n\n{first_draft.content}"),
])
print(f"Critique:\n{critique.content}\n")

# Step 3: Improve
print("=" * 60)
print("Step 3: IMPROVE")
print("=" * 60)

improved = llm.invoke([
    SystemMessage(content="You are a Python developer. Rewrite the code to address ALL the issues. Show the complete improved function."),
    HumanMessage(content=f"Original code:\n{first_draft.content}\n\nReview feedback:\n{critique.content}\n\nRewrite to fix all issues."),
])
print(f"Improved:\n{improved.content}\n")

# Step 4: Automated reflection loop
print("=" * 60)
print("Automated Reflection Loop")
print("=" * 60)

writing_task = "Write a professional email explaining a 2-week project delay."

current_draft = llm.invoke([
    SystemMessage(content="Write a professional, empathetic email. Keep it to one short paragraph."),
    HumanMessage(content=writing_task),
]).content
print(f"[Draft 1]\n{current_draft}\n")

for iteration in range(1, 3):
    critique = llm.invoke([
        SystemMessage(content="""Critique this email. Check: tone, clarity, action items, revised timeline.
List 2-3 specific improvements."""),
        HumanMessage(content=f"Email draft:\n{current_draft}"),
    ]).content
    print(f"Critique {iteration}: {critique}\n")

    current_draft = llm.invoke([
        SystemMessage(content="Rewrite incorporating ALL feedback. Professional, concise, one short paragraph."),
        HumanMessage(content=f"Current draft:\n{current_draft}\n\nFeedback:\n{critique}"),
    ]).content
    print(f"[Draft {iteration + 1}]\n{current_draft}\n")

# TODO 1: Technical explanation with reflection
print("=" * 60)
print("TODO 1: Explain Docker to a Non-Tech Manager")
print("=" * 60)

current = llm.invoke([
    SystemMessage(content="Explain to a non-technical manager in exactly 3 sentences. No jargon."),
    HumanMessage(content="Explain Docker"),
]).content
print(f"[Draft 1]\n{current}\n")

critique = llm.invoke([
    SystemMessage(content="""Review this explanation for a non-technical audience. Check:
- Any jargon or technical terms they wouldn't understand?
- Is the analogy clear and relatable?
- Is it exactly 3 sentences?
List specific issues."""),
    HumanMessage(content=f"Explanation:\n{current}"),
]).content
print(f"Critique: {critique}\n")

current = llm.invoke([
    SystemMessage(content="Rewrite fixing all issues. Exactly 3 sentences. Zero jargon. Use everyday analogies."),
    HumanMessage(content=f"Current:\n{current}\n\nFeedback:\n{critique}"),
]).content
print(f"[Final]\n{current}\n")

# TODO 2: Reflection with early stopping
print("=" * 60)
print("TODO 2: Reflection with Early Stopping")
print("=" * 60)

current = llm.invoke([
    SystemMessage(content="Write a clear, one-sentence definition."),
    HumanMessage(content="Define 'machine learning'"),
]).content
print(f"[Draft 1] {current}")

for i in range(1, 6):
    critique = llm.invoke([
        SystemMessage(content="Critique this definition for accuracy, clarity, and simplicity. If it's good, say 'No major issues.' Otherwise list improvements."),
        HumanMessage(content=f"Definition: {current}"),
    ]).content
    print(f"Critique {i}: {critique}")

    if any(phrase in critique.lower() for phrase in ["no major issues", "looks good", "no issues", "well-written", "accurate"]):
        print(f"\n[Stopped after {i} rounds — critique found no major issues]")
        break

    current = llm.invoke([
        SystemMessage(content="Rewrite fixing all issues. One sentence only."),
        HumanMessage(content=f"Current: {current}\nFeedback: {critique}"),
    ]).content
    print(f"[Draft {i + 1}] {current}")

# TODO 3: Fix buggy code with reflection
print("\n" + "=" * 60)
print("TODO 3: Fix Buggy Fibonacci")
print("=" * 60)

buggy_code = """def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)"""

critique = llm.invoke([
    SystemMessage(content="Review this code for bugs, performance issues, and edge cases. List all problems."),
    HumanMessage(content=f"```python\n{buggy_code}\n```"),
]).content
print(f"Critique:\n{critique}\n")

fixed = llm.invoke([
    SystemMessage(content="Fix all issues found. Show the complete corrected function with memoization."),
    HumanMessage(content=f"Original:\n{buggy_code}\n\nIssues:\n{critique}"),
]).content
print(f"Fixed:\n{fixed}")
