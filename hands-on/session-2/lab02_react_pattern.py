"""
Lab 02: ReAct Pattern (Reasoning + Acting)
============================================
Goal: Simulate the Thought → Action → Observation loop that agents use.

What you'll learn:
- The ReAct loop: Think → Act → Observe → Repeat
- How an agent decides which tool to use
- Why ReAct is the most common agent pattern
"""

import json
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Define some "tools" (plain Python functions)
# ============================================================
# These simulate real tools an agent might use.
# In real life, these would call APIs, databases, etc.

def search(query: str) -> str:
    """Simulate a web search."""
    fake_results = {
        "capital of france": "Paris is the capital of France.",
        "population of paris": "Paris has approximately 2.1 million residents (city proper).",
        "weather in paris": "Paris: 18°C, partly cloudy.",
        "capital of japan": "Tokyo is the capital of Japan.",
        "population of tokyo": "Tokyo has approximately 13.96 million residents.",
    }
    for key, value in fake_results.items():
        if key in query.lower():
            return value
    return f"No results found for: {query}"


def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    try:
        return str(eval(expression))
    except Exception:
        return "Error: could not evaluate expression"


TOOLS = {
    "search": {"fn": search, "desc": "Search the web for information"},
    "calculator": {"fn": calculator, "desc": "Calculate a math expression"},
}

# ============================================================
# Step 2: Manual ReAct loop — YOU play the agent
# ============================================================
# Let's walk through a ReAct loop manually to understand the pattern.

print("=" * 60)
print("Manual ReAct: 'What is the population of the capital of France?'")
print("=" * 60)

# Turn 1: Think
print("\n[Thought 1] I need to find the capital of France first.")
# Turn 1: Act
result = search("capital of France")
print(f"[Action 1]  search('capital of France')")
print(f"[Observe 1] {result}")

# Turn 2: Think
print("\n[Thought 2] The capital is Paris. Now I need its population.")
# Turn 2: Act
result = search("population of Paris")
print(f"[Action 2]  search('population of Paris')")
print(f"[Observe 2] {result}")

# Turn 3: Think
print("\n[Thought 3] I have the answer!")
print("[Answer]    The capital of France is Paris, with approximately 2.1 million residents.")

# ============================================================
# Step 3: LLM-driven ReAct — the LLM decides what to do
# ============================================================
# Now let's have the LLM decide the thoughts and actions.

print("\n" + "=" * 60)
print("LLM-Driven ReAct Loop")
print("=" * 60)

REACT_SYSTEM = """You are a helpful assistant that uses tools to answer questions.

Available tools:
- search(query): Search the web for information
- calculator(expression): Calculate a math expression

For each step, respond in EXACTLY this format:
Thought: <your reasoning about what to do next>
Action: <tool_name>(<argument>)

If you have enough information to answer, respond with:
Thought: I have enough information to answer.
Answer: <your final answer>

Important: Only ONE thought and ONE action (or answer) per response."""

question = "What is the population of the capital of Japan?"
conversation = [
    SystemMessage(content=REACT_SYSTEM),
    HumanMessage(content=question),
]

# Run the ReAct loop (max 5 iterations to prevent infinite loops)
for step in range(1, 6):
    print(f"\n--- Step {step} ---")

    response = llm.invoke(conversation)
    print(f"LLM: {response.content}")

    # Check if the LLM gave a final answer
    if "Answer:" in response.content:
        print(f"\n[Agent finished in {step} steps]")
        break

    # Extract and execute the action
    conversation.append(AIMessage(content=response.content))

    if "Action:" in response.content:
        action_line = [l for l in response.content.split("\n") if "Action:" in l]
        if action_line:
            action_text = action_line[0].split("Action:")[-1].strip()
            # Parse tool name and argument
            if "(" in action_text and ")" in action_text:
                tool_name = action_text.split("(")[0].strip()
                tool_arg = action_text.split("(")[1].rstrip(")")
                # Remove quotes from argument
                tool_arg = tool_arg.strip("'\"")

                if tool_name in TOOLS:
                    result = TOOLS[tool_name]["fn"](tool_arg)
                    observation = f"Observation: {result}"
                    print(f"[Executing] {tool_name}('{tool_arg}') → {result}")
                    conversation.append(HumanMessage(content=observation))
                else:
                    conversation.append(HumanMessage(content=f"Observation: Unknown tool '{tool_name}'"))
            else:
                conversation.append(HumanMessage(content="Observation: Could not parse action. Use format: tool_name('argument')"))
    else:
        conversation.append(HumanMessage(content="Observation: Please use the format - Thought: ... then Action: tool_name('argument') or Answer: ..."))

# ============================================================
# Step 4: See the full conversation trace
# ============================================================

print("\n" + "=" * 60)
print("Full Conversation Trace")
print("=" * 60)
for msg in conversation:
    role = type(msg).__name__.replace("Message", "")
    # Truncate long messages for readability
    content = msg.content[:120] + "..." if len(msg.content) > 120 else msg.content
    print(f"[{role:6s}] {content}")

# ============================================================
# TODO 1: Ask a multi-step question
# ============================================================
# Try running the ReAct loop with these questions:
#   a) "What is the weather in the capital of France?"
#   b) "What is 15% of the population of Paris?"
#        (This needs search THEN calculator!)
#
# Hint: Copy the loop above but change the question.

# TODO: Build and run a new ReAct loop

# ============================================================
# TODO 2: Add a new tool
# ============================================================
# Add a "translate" tool to the TOOLS dictionary:
#   def translate(text_and_lang):
#       """Fake translator."""
#       return f"[Translated: {text_and_lang}]"
#
# Update the system message to include the new tool.
# Then ask: "How do you say 'hello' in the language spoken
#            in the capital of France?"

# TODO: Add translate tool and test

print("\n" + "=" * 60)
print("Lab 02 complete! Key takeaways:")
print("- ReAct = Thought → Action → Observation, repeated")
print("- The LLM DECIDES which tool to use and what to pass")
print("- The framework EXECUTES the tool and returns the result")
print("- Multi-step questions need multiple ReAct iterations")
print("- This is exactly how LangChain agents work under the hood!")
