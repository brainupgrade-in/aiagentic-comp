"""
Lab 05: Tool Calling — SOLUTION
"""

import json
import math
import random
import string
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")


# Tools
def calculator(expression: str) -> str:
    try:
        allowed = {"__builtins__": {}, "math": math}
        return f"{expression} = {eval(expression, allowed)}"
    except Exception as e:
        return f"Error: {e}"


def get_current_time() -> str:
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


def word_count(text: str) -> str:
    return f"The text has {len(text.split())} words."


def reverse_text(text: str) -> str:
    return text[::-1]


def unit_converter(query: str) -> str:
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
    return f"Cannot convert: {query}"


def password_generator(length: str) -> str:
    """Generate a random password of given length."""
    n = int(length)
    chars = string.ascii_letters + string.digits + "!@#$%"
    return "".join(random.choice(chars) for _ in range(n))


TOOLS = {
    "calculator": {"fn": calculator, "desc": "Evaluate a math expression (e.g., '17 * 28', 'math.sqrt(144)')"},
    "get_current_time": {"fn": get_current_time, "desc": "Get the current date and time. Takes no arguments."},
    "word_count": {"fn": word_count, "desc": "Count the words in a text."},
    "reverse_text": {"fn": reverse_text, "desc": "Reverse the given text."},
    "unit_converter": {"fn": unit_converter, "desc": "Convert between units. Format: '100 km to miles' or '30 celsius to fahrenheit'."},
    "password_generator": {"fn": password_generator, "desc": "Generate a random password. Argument: the desired length (e.g., '16')."},
}


def build_system_prompt(tools: dict) -> str:
    tool_descriptions = "\n".join(f"- {name}: {info['desc']}" for name, info in tools.items())
    return f"""You are a helpful assistant with access to tools.

Available tools:
{tool_descriptions}

When you need to use a tool, respond with EXACTLY this JSON format:
{{"tool": "tool_name", "argument": "the argument"}}

If the tool needs no argument, use: {{"tool": "tool_name", "argument": ""}}

If you can answer WITHOUT a tool, just respond normally.
Only use ONE tool per response."""


def execute_tool_call(response_text: str) -> str | None:
    try:
        start = response_text.index("{")
        end = response_text.rindex("}") + 1
        call = json.loads(response_text[start:end])
        tool_name = call.get("tool", "")
        argument = call.get("argument", "")
        if tool_name in TOOLS:
            result = TOOLS[tool_name]["fn"](argument) if argument else TOOLS[tool_name]["fn"]()
            return f"[Tool: {tool_name}] Result: {result}"
        return f"[Error] Unknown tool: {tool_name}"
    except (json.JSONDecodeError, ValueError):
        return None


SYSTEM = build_system_prompt(TOOLS)

# Test all tools
print("=" * 60)
print("Tool Calling Tests")
print("=" * 60)

test_questions = [
    "What is 17 multiplied by 28?",
    "What time is it right now?",
    "How many words are in: The quick brown fox jumps over the lazy dog",
    "Convert 100 kilometers to miles",
    "Reverse the text 'hello world'",
    "Generate a 16-character password",
    "What is the capital of India?",
]

for question in test_questions:
    print(f"\nQ: {question}")
    response = llm.invoke([
        SystemMessage(content=SYSTEM),
        HumanMessage(content=question),
    ])
    print(f"LLM: {response.content}")
    result = execute_tool_call(response.content)
    if result:
        print(f"  → {result}")
    else:
        print(f"  → [No tool used]")

# TODO 2: Multi-tool question with loop
print("\n" + "=" * 60)
print("Multi-Tool: Fahrenheit to Celsius + Square Root")
print("=" * 60)

question = "What is 42 degrees Fahrenheit in Celsius, and what is the square root of that Celsius value?"
conversation = [
    SystemMessage(content=SYSTEM),
    HumanMessage(content=question),
]

for step in range(1, 5):
    print(f"\n--- Step {step} ---")
    response = llm.invoke(conversation)
    print(f"LLM: {response.content}")

    result = execute_tool_call(response.content)
    if result:
        print(f"  → {result}")
        conversation.append(AIMessage(content=response.content))
        conversation.append(HumanMessage(content=f"Tool result: {result}\n\nContinue answering the original question."))
    else:
        print("[Final answer reached]")
        break
