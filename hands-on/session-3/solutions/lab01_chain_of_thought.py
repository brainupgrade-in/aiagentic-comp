"""
Lab 01: Chain-of-Thought — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# Step 1: Without CoT
print("=" * 60)
print("WITHOUT Chain-of-Thought")
print("=" * 60)

question = """A store has 15 apples. They sell 8 in the morning.
At noon they receive a shipment of 20 apples.
In the afternoon they sell 12 more.
How many apples do they have now?"""

response = llm.invoke([
    SystemMessage(content="Answer the question. Give just the number."),
    HumanMessage(content=question),
])
print(f"LLM Answer: {response.content}")
print(f"Correct Answer: 15\n")

# Step 2: With CoT
print("=" * 60)
print("WITH Chain-of-Thought")
print("=" * 60)

response = llm.invoke([
    SystemMessage(content="Solve the problem step by step. Show each calculation."),
    HumanMessage(content=question + "\n\nLet's think step by step."),
])
print(f"LLM Reasoning:\n{response.content}\n")

# Step 3: Logic puzzle
print("=" * 60)
print("Logic Puzzle: Without vs With CoT")
print("=" * 60)

puzzle = """If all roses are flowers, and some flowers fade quickly,
can we conclude that some roses fade quickly?"""

response_no_cot = llm.invoke([
    SystemMessage(content="Answer yes or no and explain briefly."),
    HumanMessage(content=puzzle),
])
print(f"Without CoT:\n{response_no_cot.content}\n")

response_cot = llm.invoke([
    SystemMessage(content="Think through this carefully using formal logic. Show each step of your reasoning."),
    HumanMessage(content=puzzle + "\n\nLet's reason through this step by step."),
])
print(f"With CoT:\n{response_cot.content}\n")

# Step 4: Word problem
print("=" * 60)
print("Word Problem")
print("=" * 60)

word_problem = """Ravi is taller than Priya. Priya is taller than Amit.
Amit is taller than Sneha. Who is the shortest?"""

response = llm.invoke([
    SystemMessage(content="Think through this step by step, then give the answer."),
    HumanMessage(content=word_problem + "\n\nLet's work through the ordering step by step."),
])
print(f"With CoT:\n{response.content}\n")

# TODO 1: Train problem
print("=" * 60)
print("TODO 1: Train Problem")
print("=" * 60)

train_problem = """A train leaves Mumbai at 9 AM going 60 km/h.
Another train leaves Pune (150 km away) at 10 AM going 90 km/h toward Mumbai.
At what time do they meet?"""

# Without CoT
response = llm.invoke([
    SystemMessage(content="Answer the question directly."),
    HumanMessage(content=train_problem),
])
print(f"Without CoT: {response.content}\n")

# With CoT
response = llm.invoke([
    SystemMessage(content="Solve step by step. Show all calculations clearly."),
    HumanMessage(content=train_problem + "\n\nLet's think step by step."),
])
print(f"With CoT:\n{response.content}\n")
print("Expected: At 10 AM, Train 1 has traveled 60 km. Gap = 90 km.")
print("Combined speed = 150 km/h. Time = 90/150 = 0.6 hours = 36 min.")
print("They meet at 10:36 AM.\n")

# TODO 2: Compare different CoT prompts
print("=" * 60)
print("TODO 2: Different CoT Phrasings")
print("=" * 60)

test_q = "If a shirt costs Rs 400 and is on 25% discount, and you have a 10% coupon on top of that, what do you pay?"

phrasings = [
    "Think step by step.",
    "Break this into sub-problems and solve each.",
    "Before answering, list your assumptions and work through each calculation.",
]

for phrase in phrasings:
    response = llm.invoke([
        SystemMessage(content="Solve the problem carefully."),
        HumanMessage(content=f"{test_q}\n\n{phrase}"),
    ])
    print(f"Phrasing: '{phrase}'")
    print(f"Response: {response.content}\n")

print("Expected: 400 * 0.75 = 300 (after discount), 300 * 0.90 = Rs 270 (after coupon)")
