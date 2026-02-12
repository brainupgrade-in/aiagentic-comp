"""
Lab 02: ReAct Pattern — SOLUTION
"""

import json
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")


# Tools
def search(query: str) -> str:
    """Simulate a web search."""
    fake_results = {
        "capital of france": "Paris is the capital of France.",
        "population of paris": "Paris has approximately 2.1 million residents (city proper).",
        "weather in paris": "Paris: 18°C, partly cloudy.",
        "capital of japan": "Tokyo is the capital of Japan.",
        "population of tokyo": "Tokyo has approximately 13.96 million residents.",
        "language spoken in france": "The official language of France is French.",
        "hello in french": "'Hello' in French is 'Bonjour'.",
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


def translate(text_and_lang: str) -> str:
    """Fake translator."""
    translations = {
        "hello french": "Bonjour",
        "hello spanish": "Hola",
        "hello hindi": "Namaste",
        "hello japanese": "Konnichiwa",
    }
    for key, value in translations.items():
        if key in text_and_lang.lower():
            return f"Translation: {value}"
    return f"[Translated: {text_and_lang}]"


TOOLS = {
    "search": {"fn": search, "desc": "Search the web for information"},
    "calculator": {"fn": calculator, "desc": "Calculate a math expression"},
    "translate": {"fn": translate, "desc": "Translate text. Format: 'hello to French'"},
}

REACT_SYSTEM = """You are a helpful assistant that uses tools to answer questions.

Available tools:
- search(query): Search the web for information
- calculator(expression): Calculate a math expression
- translate(text_and_language): Translate text. Format: 'hello French'

For each step, respond in EXACTLY this format:
Thought: <your reasoning about what to do next>
Action: <tool_name>(<argument>)

If you have enough information to answer, respond with:
Thought: I have enough information to answer.
Answer: <your final answer>

Important: Only ONE thought and ONE action (or answer) per response."""


def run_react(question: str, max_steps: int = 5) -> str:
    """Run a ReAct loop and return the final answer."""
    conversation = [
        SystemMessage(content=REACT_SYSTEM),
        HumanMessage(content=question),
    ]

    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step} ---")
        response = llm.invoke(conversation)
        print(f"LLM: {response.content}")

        if "Answer:" in response.content:
            answer_line = response.content.split("Answer:")[-1].strip()
            print(f"\n[Agent finished in {step} steps]")
            return answer_line

        conversation.append(AIMessage(content=response.content))

        if "Action:" in response.content:
            action_line = [l for l in response.content.split("\n") if "Action:" in l]
            if action_line:
                action_text = action_line[0].split("Action:")[-1].strip()
                if "(" in action_text and ")" in action_text:
                    tool_name = action_text.split("(")[0].strip()
                    tool_arg = action_text.split("(")[1].rstrip(")").strip("'\"")

                    if tool_name in TOOLS:
                        result = TOOLS[tool_name]["fn"](tool_arg)
                        print(f"[Executing] {tool_name}('{tool_arg}') → {result}")
                        conversation.append(HumanMessage(content=f"Observation: {result}"))
                    else:
                        conversation.append(HumanMessage(content=f"Observation: Unknown tool '{tool_name}'. Available: {', '.join(TOOLS.keys())}"))
                else:
                    conversation.append(HumanMessage(content="Observation: Could not parse action. Use format: tool_name('argument')"))
        else:
            conversation.append(HumanMessage(content="Observation: Please respond with either an Action or an Answer."))

    return "[Max steps reached]"


# Test 1: Simple multi-step
print("=" * 60)
print("Test 1: Population of the capital of Japan")
print("=" * 60)
run_react("What is the population of the capital of Japan?")

# Test 2: Weather question
print("\n" + "=" * 60)
print("Test 2: Weather in the capital of France")
print("=" * 60)
run_react("What is the weather in the capital of France?")

# TODO 1: Multi-tool question
print("\n" + "=" * 60)
print("TODO 1: Multi-tool — 15% of Paris population")
print("=" * 60)
run_react("What is 15% of the population of Paris?")

# TODO 2: Question with translate tool
print("\n" + "=" * 60)
print("TODO 2: Translate hello to French")
print("=" * 60)
run_react("How do you say 'hello' in the language spoken in the capital of France?")
