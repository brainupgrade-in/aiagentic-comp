"""
Lab 07: Challenge — Build a Mini Agent
========================================
Goal: Combine reasoning + tools + memory into a working agent.

Your mission: Build a "Smart Study Buddy" agent that:
1. Uses Chain-of-Thought to reason about questions
2. Has access to tools (calculator, dictionary, quiz generator)
3. Remembers the conversation (short-term memory)
4. Uses the ReAct pattern to decide when to use tools

This exercise has minimal pre-written code — use what you learned
in Labs 01-06 to build it!
"""

import json
import math
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

print("=" * 60)
print("  Smart Study Buddy — Mini Agent Challenge")
print("=" * 60)

# ============================================================
# PART A: Define your tools
# ============================================================
# Here are some tools. You can add more!

def calculator(expression: str) -> str:
    """Calculate a math expression."""
    try:
        allowed = {"__builtins__": {}, "math": math}
        return str(eval(expression, allowed))
    except Exception as e:
        return f"Error: {e}"


def define_word(word: str) -> str:
    """Look up the definition of a word."""
    definitions = {
        "algorithm": "A step-by-step procedure for solving a problem or accomplishing a task.",
        "api": "Application Programming Interface — a way for software programs to communicate with each other.",
        "variable": "A named storage location in a program that holds a value which can change.",
        "function": "A reusable block of code that performs a specific task.",
        "loop": "A programming construct that repeats a block of code multiple times.",
        "recursion": "When a function calls itself to solve smaller instances of the same problem.",
        "docker": "A platform that packages applications into lightweight, portable containers.",
        "kubernetes": "An orchestration system for automating deployment and management of containers.",
    }
    return definitions.get(word.lower().strip(), f"Definition not found for: {word}")


def generate_quiz(topic: str) -> str:
    """Generate a quick quiz question about a topic."""
    quizzes = {
        "python": "Q: What keyword is used to define a function in Python?\nA) func  B) def  C) function  D) define\nCorrect: B) def",
        "git": "Q: What command creates a new Git branch?\nA) git new  B) git create  C) git branch  D) git fork\nCorrect: C) git branch",
        "docker": "Q: What file defines a Docker image?\nA) docker.yml  B) Dockerfile  C) docker.conf  D) image.json\nCorrect: B) Dockerfile",
        "linux": "Q: What command lists files in a directory?\nA) dir  B) show  C) ls  D) list\nCorrect: C) ls",
    }
    for key, quiz in quizzes.items():
        if key in topic.lower():
            return quiz
    return f"No quiz available for: {topic}. Try: python, git, docker, linux."


TOOLS = {
    "calculator": {"fn": calculator, "desc": "Calculate a math expression (e.g., '17 * 28', 'math.sqrt(144)')"},
    "define_word": {"fn": define_word, "desc": "Look up the definition of a programming/tech term"},
    "generate_quiz": {"fn": generate_quiz, "desc": "Generate a quiz question about a topic (python, git, docker, linux)"},
}


# ============================================================
# PART B: Build the system prompt
# ============================================================
# TODO: Create a system prompt that tells the LLM about:
#   1. Its role (study buddy)
#   2. Available tools and their descriptions
#   3. The ReAct format (Thought → Action or Answer)
#   4. Instruction to think step by step for complex questions

# Hint — here's a template to start with:
SYSTEM_PROMPT = """You are a Smart Study Buddy that helps students learn programming concepts.

Available tools:
- calculator(expression): Calculate a math expression (e.g., '17 * 28', 'math.sqrt(144)')
- define_word(word): Look up the definition of a programming/tech term
- generate_quiz(topic): Generate a quiz question about a topic (python, git, docker, linux)

When you need a tool, respond with EXACTLY this JSON:
{"tool": "tool_name", "argument": "the argument"}

If you can answer without a tool, respond directly.
For complex questions, think step by step before answering.
Be encouraging and friendly — this is a learning environment!"""


# ============================================================
# PART C: Build the agent loop
# ============================================================
# TODO: Implement the ReAct loop with memory.
# The agent should:
#   1. Keep conversation history (memory)
#   2. Parse tool calls from LLM responses
#   3. Execute tools and feed results back
#   4. Continue until the LLM gives a direct answer

def run_agent(user_message: str, history: list) -> tuple[str, list]:
    """
    Run one turn of the agent.

    Args:
        user_message: The user's input
        history: List of previous messages (memory)

    Returns:
        (agent_reply, updated_history)
    """
    history.append(HumanMessage(content=user_message))

    # ReAct loop (max 3 tool calls per turn)
    response_text = ""
    for _ in range(3):
        response = llm.invoke(history)
        response_text = response.content

        # Try to parse a tool call
        try:
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
                # Add tool interaction to history
                history.append(AIMessage(content=response_text))
                history.append(HumanMessage(content=f"Tool result: {result}"))
                continue  # Let the LLM process the result
            else:
                # Unknown tool — treat as direct answer
                break
        except (json.JSONDecodeError, ValueError):
            # No tool call — it's a direct answer
            break

    history.append(AIMessage(content=response_text))
    return response_text, history


# ============================================================
# PART D: Test the agent
# ============================================================

history = [SystemMessage(content=SYSTEM_PROMPT)]

test_messages = [
    "Hi! I'm learning programming. Can you help me?",
    "What does 'algorithm' mean?",
    "What is 2 to the power of 10?",
    "Give me a quiz about Python!",
    "I got it right! What was the first thing I asked you about?",  # Tests memory
]

for msg in test_messages:
    print(f"\nYou: {msg}")
    reply, history = run_agent(msg, history)
    print(f"Bot: {reply}")
    print(f"     [Memory: {len(history)} messages]")

# ============================================================
# PART E (Bonus): Make it interactive
# ============================================================
# TODO: Uncomment to run an interactive chat loop

# print("\n" + "=" * 60)
# print("Interactive Mode (type 'quit' to exit)")
# print("=" * 60)
#
# history = [SystemMessage(content=SYSTEM_PROMPT)]
# while True:
#     user_input = input("\nYou: ").strip()
#     if user_input.lower() == "quit":
#         print("Goodbye! Keep learning!")
#         break
#     reply, history = run_agent(user_input, history)
#     print(f"Bot: {reply}")

# ============================================================
# PART F (Bonus): Add more tools
# ============================================================
# Ideas:
#   - explain_code(code): Explain what a code snippet does
#   - compare(a_and_b): Compare two technologies
#   - acronym(letters): Expand a tech acronym (API, REST, SQL)
#
# Add them to TOOLS and update the SYSTEM_PROMPT.

print("\n" + "=" * 60)
print("Challenge tips:")
print("- The agent already works! Try the interactive mode (Part E)")
print("- Add your own tools to make it more capable")
print("- Notice how memory lets the bot reference earlier messages")
print("- Notice how the ReAct loop decides tool vs direct answer")
print("- Check solutions/lab07_challenge.py for the complete version")
