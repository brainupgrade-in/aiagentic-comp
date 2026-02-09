"""
Lab 07: Challenge — Smart Study Buddy — SOLUTION
"""

import json
import math
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

print("=" * 60)
print("  Smart Study Buddy — Mini Agent (Solution)")
print("=" * 60)


# Tools
def calculator(expression: str) -> str:
    try:
        allowed = {"__builtins__": {}, "math": math}
        return str(eval(expression, allowed))
    except Exception as e:
        return f"Error: {e}"


def define_word(word: str) -> str:
    definitions = {
        "algorithm": "A step-by-step procedure for solving a problem or accomplishing a task.",
        "api": "Application Programming Interface — a way for software programs to communicate with each other.",
        "variable": "A named storage location in a program that holds a value which can change.",
        "function": "A reusable block of code that performs a specific task.",
        "loop": "A programming construct that repeats a block of code multiple times.",
        "recursion": "When a function calls itself to solve smaller instances of the same problem.",
        "docker": "A platform that packages applications into lightweight, portable containers.",
        "kubernetes": "An orchestration system for automating deployment and management of containers.",
        "class": "A blueprint for creating objects that bundles data and methods together.",
        "inheritance": "A mechanism where a new class inherits properties and methods from an existing class.",
    }
    return definitions.get(word.lower().strip(), f"Definition not found for: {word}")


def generate_quiz(topic: str) -> str:
    quizzes = {
        "python": "Q: What keyword is used to define a function in Python?\nA) func  B) def  C) function  D) define\nCorrect: B) def",
        "git": "Q: What command creates a new Git branch?\nA) git new  B) git create  C) git branch  D) git fork\nCorrect: C) git branch",
        "docker": "Q: What file defines a Docker image?\nA) docker.yml  B) Dockerfile  C) docker.conf  D) image.json\nCorrect: B) Dockerfile",
        "linux": "Q: What command lists files in a directory?\nA) dir  B) show  C) ls  D) list\nCorrect: C) ls",
        "java": "Q: Which keyword is used for inheritance in Java?\nA) inherits  B) extends  C) implements  D) derives\nCorrect: B) extends",
    }
    for key, quiz in quizzes.items():
        if key in topic.lower():
            return quiz
    return f"No quiz available for: {topic}. Try: python, git, docker, linux, java."


def explain_code(code: str) -> str:
    """Provide a simple explanation of a code snippet."""
    explanations = {
        "for": "This is a loop that iterates over a sequence of items.",
        "def": "This defines a function — a reusable block of code.",
        "class": "This defines a class — a blueprint for creating objects.",
        "if": "This is a conditional statement that runs code only if a condition is true.",
        "import": "This loads a module or library to use its features.",
    }
    for keyword, explanation in explanations.items():
        if keyword in code.lower():
            return explanation
    return "This code performs a programming operation. Ask me about specific parts!"


TOOLS = {
    "calculator": {"fn": calculator, "desc": "Calculate a math expression (e.g., '17 * 28', 'math.sqrt(144)')"},
    "define_word": {"fn": define_word, "desc": "Look up the definition of a programming/tech term"},
    "generate_quiz": {"fn": generate_quiz, "desc": "Generate a quiz question about a topic (python, git, docker, linux, java)"},
    "explain_code": {"fn": explain_code, "desc": "Get a simple explanation of a code snippet or keyword"},
}


SYSTEM_PROMPT = """You are a Smart Study Buddy that helps students learn programming concepts.
You are friendly, encouraging, and patient.

Available tools:
- calculator(expression): Calculate a math expression (e.g., '17 * 28', 'math.sqrt(144)')
- define_word(word): Look up the definition of a programming/tech term
- generate_quiz(topic): Generate a quiz question about a topic (python, git, docker, linux, java)
- explain_code(code): Get a simple explanation of a code snippet or keyword

When you need a tool, respond with EXACTLY this JSON:
{"tool": "tool_name", "argument": "the argument"}

If you can answer without a tool, respond directly.
For complex questions, think step by step before answering.
Remember what the student has asked before and build on it.
Be encouraging — celebrate when they get things right!"""


def run_agent(user_message: str, history: list) -> tuple[str, list]:
    """Run one turn of the agent with ReAct loop."""
    history.append(HumanMessage(content=user_message))

    response_text = ""
    for _ in range(3):
        response = llm.invoke(history)
        response_text = response.content

        try:
            start = response_text.index("{")
            end = response_text.rindex("}") + 1
            call = json.loads(response_text[start:end])
            tool_name = call.get("tool", "")
            argument = call.get("argument", "")

            if tool_name in TOOLS:
                result = TOOLS[tool_name]["fn"](argument) if argument else TOOLS[tool_name]["fn"]()
                print(f"  [Tool: {tool_name}('{argument}') → {result}]")
                history.append(AIMessage(content=response_text))
                history.append(HumanMessage(content=f"Tool result: {result}\nNow respond to the student based on this result. Be friendly and helpful."))
                continue
            else:
                break
        except (json.JSONDecodeError, ValueError):
            break

    history.append(AIMessage(content=response_text))
    return response_text, history


# Run test conversation
history = [SystemMessage(content=SYSTEM_PROMPT)]

test_messages = [
    "Hi! I'm Raj and I'm learning programming. Can you help me?",
    "What does 'algorithm' mean?",
    "What is 2 to the power of 10?",
    "Give me a quiz about Python!",
    "The answer is B, def! Did I get it right?",
    "What was the first definition I asked you about?",
    "Can you explain what 'class' means?",
    "Now give me a quiz about Docker!",
]

for msg in test_messages:
    print(f"\nYou: {msg}")
    reply, history = run_agent(msg, history)
    print(f"Bot: {reply}")
    print(f"     [Memory: {len(history)} messages]")

# Interactive mode
print("\n" + "=" * 60)
print("Interactive Mode (type 'quit' to exit)")
print("=" * 60)

history = [SystemMessage(content=SYSTEM_PROMPT)]
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == "quit":
        print("Goodbye! Keep learning — you're doing great!")
        break
    reply, history = run_agent(user_input, history)
    print(f"Bot: {reply}")
