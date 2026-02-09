"""
Lab 05: Tool Calling
======================
Goal: Build Python tools and see how an LLM decides which tool to use.

What you'll learn:
- A tool = Python function + name + description
- The LLM reads descriptions to decide WHICH tool to call
- The LLM generates the correct arguments
- Multiple tools can be available simultaneously
"""

import json
import math
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Define tools as Python functions
# ============================================================
# Each tool has: a name, a description, and a function.

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression and return the result."""
    try:
        # Safe subset of math operations
        allowed = {"__builtins__": {}, "math": math}
        result = eval(expression, allowed)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"


def get_current_time() -> str:
    """Return the current date and time."""
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y at %I:%M %p")


def word_count(text: str) -> str:
    """Count the number of words in the given text."""
    words = text.split()
    return f"The text has {len(words)} words."


def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]


def unit_converter(query: str) -> str:
    """Convert between units. Format: '<value> <from_unit> to <to_unit>'."""
    conversions = {
        ("km", "miles"): 0.621371,
        ("miles", "km"): 1.60934,
        ("kg", "lbs"): 2.20462,
        ("lbs", "kg"): 0.453592,
        ("celsius", "fahrenheit"): lambda x: x * 9 / 5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5 / 9,
    }
    parts = query.lower().replace("to ", "").split()
    try:
        value = float(parts[0])
        from_unit = parts[1]
        to_unit = parts[2] if len(parts) > 2 else parts[-1]
        key = (from_unit, to_unit)
        if key in conversions:
            conv = conversions[key]
            result = conv(value) if callable(conv) else value * conv
            return f"{value} {from_unit} = {result:.2f} {to_unit}"
    except (ValueError, IndexError):
        pass
    return f"Cannot convert: {query}. Use format: '100 km to miles'"


# Registry of all tools
TOOLS = {
    "calculator": {
        "fn": calculator,
        "description": "Evaluate a math expression (e.g., '17 * 28', 'math.sqrt(144)').",
    },
    "get_current_time": {
        "fn": get_current_time,
        "description": "Get the current date and time. Takes no arguments.",
    },
    "word_count": {
        "fn": word_count,
        "description": "Count the words in a text.",
    },
    "reverse_text": {
        "fn": reverse_text,
        "description": "Reverse the given text.",
    },
    "unit_converter": {
        "fn": unit_converter,
        "description": "Convert between units. Format: '100 km to miles' or '30 celsius to fahrenheit'.",
    },
}


# ============================================================
# Step 2: Build the tool-calling system prompt
# ============================================================
# The LLM needs to know what tools are available.

def build_system_prompt(tools: dict) -> str:
    tool_descriptions = "\n".join(
        f"- {name}: {info['description']}"
        for name, info in tools.items()
    )
    return f"""You are a helpful assistant with access to tools.

Available tools:
{tool_descriptions}

When you need to use a tool, respond with EXACTLY this JSON format:
{{"tool": "tool_name", "argument": "the argument"}}

If the tool needs no argument, use: {{"tool": "tool_name", "argument": ""}}

If you can answer WITHOUT a tool, just respond normally.
Only use ONE tool per response."""


SYSTEM = build_system_prompt(TOOLS)


# ============================================================
# Step 3: Tool execution engine
# ============================================================

def execute_tool_call(response_text: str) -> str | None:
    """Parse and execute a tool call from the LLM response."""
    try:
        # Try to find JSON in the response
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        call = json.loads(response_text[start:end])

        tool_name = call.get("tool", "")
        argument = call.get("argument", "")

        if tool_name in TOOLS:
            if argument:
                result = TOOLS[tool_name]["fn"](argument)
            else:
                result = TOOLS[tool_name]["fn"]()
            return f"[Tool: {tool_name}] Result: {result}"
        else:
            return f"[Error] Unknown tool: {tool_name}"
    except (json.JSONDecodeError, ValueError):
        return None  # No tool call detected


# ============================================================
# Step 4: Test — LLM decides which tool to use
# ============================================================

print("=" * 60)
print("Tool Calling: LLM Chooses the Right Tool")
print("=" * 60)

test_questions = [
    "What is 17 multiplied by 28?",
    "What time is it right now?",
    "How many words are in this sentence: The quick brown fox jumps over the lazy dog",
    "Convert 100 kilometers to miles",
    "What is the reverse of 'hello world'?",
    "What is the capital of India?",  # Should NOT use a tool
]

for question in test_questions:
    print(f"\nQ: {question}")
    response = llm.invoke([
        SystemMessage(content=SYSTEM),
        HumanMessage(content=question),
    ])
    print(f"LLM: {response.content}")

    # Try to execute if it's a tool call
    result = execute_tool_call(response.content)
    if result:
        print(f"  → {result}")
    else:
        print(f"  → [No tool used — answered directly]")

# ============================================================
# Step 5: See what the LLM sees
# ============================================================

print("\n" + "=" * 60)
print("What the LLM Sees (System Prompt)")
print("=" * 60)
print(SYSTEM)

# ============================================================
# TODO 1: Add a new tool — password generator
# ============================================================
# Create a tool that generates a random password of a given length.
#
# import random, string
# def password_generator(length: str) -> str:
#     n = int(length)
#     chars = string.ascii_letters + string.digits + "!@#$%"
#     return "".join(random.choice(chars) for _ in range(n))
#
# Add it to TOOLS and test with: "Generate a 16-character password"

# TODO: Add the tool and test it

# ============================================================
# TODO 2: Multi-tool question
# ============================================================
# Ask: "What is 42 degrees Fahrenheit in Celsius, and what
# is the square root of that number?"
#
# This needs TWO tool calls (unit_converter then calculator).
# Implement a loop that runs until the LLM gives a final answer.

# TODO: Implement a multi-step tool calling loop

# ============================================================
# TODO 3: Improve tool descriptions
# ============================================================
# The LLM sometimes picks the wrong tool. Try improving the
# descriptions to be more specific. For example:
#   Bad:  "Do math"
#   Good: "Evaluate a mathematical expression like '17*28' or 'math.sqrt(144)'"
#
# Test if better descriptions lead to better tool selection.

# TODO: Experiment with description quality

print("\n" + "=" * 60)
print("Lab 05 complete! Key takeaways:")
print("- Tools = Python functions with name + description")
print("- The LLM reads descriptions to choose the right tool")
print("- Good descriptions → correct tool selection")
print("- The LLM generates arguments; the framework executes")
print("- Any Python function can be a tool!")
