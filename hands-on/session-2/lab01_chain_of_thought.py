"""
Lab 01: Chain-of-Thought (CoT) Reasoning
==========================================
Goal: See how asking the LLM to "think step by step" improves accuracy.

What you'll learn:
- Without CoT: LLMs often guess wrong on multi-step problems
- With CoT: Step-by-step reasoning dramatically improves accuracy
- The magic phrase: "Let's think step by step"
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: WITHOUT Chain-of-Thought
# ============================================================
# Ask the LLM a multi-step question directly.
# Notice: it often gets it wrong because it jumps to an answer.

print("=" * 60)
print("WITHOUT Chain-of-Thought")
print("=" * 60)

question = """A store has 15 apples. They sell 8 in the morning.
At noon they receive a shipment of 20 apples.
In the afternoon they sell 12 more.
How many apples do they have now?"""

# Expected answer: 15 - 8 + 20 - 12 = 15

response = llm.invoke([
    SystemMessage(content="Answer the question. Give just the number."),
    HumanMessage(content=question),
])
print(f"Question: {question}")
print(f"LLM Answer: {response.content}")
print(f"Correct Answer: 15")
print()

# ============================================================
# Step 2: WITH Chain-of-Thought
# ============================================================
# Same question, but now we ask the LLM to think step by step.
# This simple change forces it to show its work.

print("=" * 60)
print("WITH Chain-of-Thought")
print("=" * 60)

response = llm.invoke([
    SystemMessage(content="Solve the problem step by step. Show each calculation."),
    HumanMessage(content=question + "\n\nLet's think step by step."),
])
print(f"LLM Reasoning:\n{response.content}")
print()

# ============================================================
# Step 3: CoT on a logic puzzle
# ============================================================
# Logic puzzles really show the difference.

print("=" * 60)
print("Logic Puzzle: Without vs With CoT")
print("=" * 60)

puzzle = """If all roses are flowers, and some flowers fade quickly,
can we conclude that some roses fade quickly?"""

# Without CoT
response_no_cot = llm.invoke([
    SystemMessage(content="Answer yes or no and explain briefly."),
    HumanMessage(content=puzzle),
])
print(f"Without CoT:\n{response_no_cot.content}\n")

# With CoT
response_cot = llm.invoke([
    SystemMessage(content="Think through this carefully using formal logic. Show each step of your reasoning."),
    HumanMessage(content=puzzle + "\n\nLet's reason through this step by step."),
])
print(f"With CoT:\n{response_cot.content}\n")
print("Correct: No — 'some flowers fade quickly' doesn't mean the ones that do are roses.")

# ============================================================
# Step 4: CoT on a word problem
# ============================================================

print("\n" + "=" * 60)
print("Word Problem: CoT Comparison")
print("=" * 60)

word_problem = """Ravi is taller than Priya. Priya is taller than Amit.
Amit is taller than Sneha. Who is the shortest?"""

# Without CoT
response = llm.invoke([
    SystemMessage(content="Answer in one word."),
    HumanMessage(content=word_problem),
])
print(f"Without CoT: {response.content}")

# With CoT
response = llm.invoke([
    SystemMessage(content="Think through this step by step, then give the answer."),
    HumanMessage(content=word_problem + "\n\nLet's work through the ordering step by step."),
])
print(f"With CoT:\n{response.content}")

# ============================================================
# TODO 1: Test CoT on a math problem
# ============================================================
# Try this: "A train leaves Mumbai at 9 AM going 60 km/h.
# Another train leaves Pune (150 km away) at 10 AM going 90 km/h
# toward Mumbai. At what time do they meet?"
#
# First ask without CoT, then with CoT. Compare the answers.

# TODO: Write your code here

# ============================================================
# TODO 2: Create your own CoT system message
# ============================================================
# Try different phrasings and see which produces the best reasoning:
#   a) "Think step by step"
#   b) "Break this into sub-problems and solve each"
#   c) "Before answering, list your assumptions and work through them"
#
# Test all three on the same question.

# TODO: Experiment with different CoT prompts

print("\n" + "=" * 60)
print("Lab 01 complete! Key takeaways:")
print('- "Let\'s think step by step" significantly improves accuracy')
print("- CoT forces the LLM to reason instead of guess")
print("- Works best on: math, logic, multi-step problems")
print("- Cost: more tokens (longer response), but much more accurate")
