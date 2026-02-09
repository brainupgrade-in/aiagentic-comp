"""
Lab 02: Exploring LLM Superpowers
===================================
Goal: See the impressive things LLMs can do.

What you'll learn:
- LLMs can write, translate, summarize, explain, and generate code
- They understand context and nuance in language
- These capabilities are what make agents possible
"""

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Superpower 1: Language Understanding
# ============================================================

print("=" * 50)
print("SUPERPOWER 1: Language Understanding")
print("=" * 50)

response = llm.invoke("Is the following review positive or negative? 'The food was amazing but the service was terrible and we waited 45 minutes.'")
print(f"Sentiment Analysis:\n{response.content}\n")

response = llm.invoke("Extract the person's name, city, and job from this text: 'Priya from Bangalore works as a data scientist at Oracle.'")
print(f"Information Extraction:\n{response.content}\n")

# ============================================================
# Superpower 2: Translation
# ============================================================

print("=" * 50)
print("SUPERPOWER 2: Translation")
print("=" * 50)

languages = ["French", "Japanese", "Hindi"]
for lang in languages:
    response = llm.invoke(f"Translate 'Good morning, how are you?' to {lang}. Reply with only the translation.")
    print(f"  {lang}: {response.content}")

# ============================================================
# Superpower 3: Summarization
# ============================================================

print(f"\n{'=' * 50}")
print("SUPERPOWER 3: Summarization")
print("=" * 50)

long_text = """Docker is a platform designed to help developers build, share, and run container
applications. It handles the tedious setup, so you can focus on the code. Containers
are lightweight and contain everything needed to run an application, so there's no
need to rely on what's installed on the host. Docker provides tools and a platform
to manage the lifecycle of your containers. You can develop your application and its
supporting components using containers, and the container becomes the unit for
distributing and testing your application."""

response = llm.invoke(f"Summarize this in exactly ONE sentence:\n\n{long_text}")
print(f"Summary: {response.content}\n")

# ============================================================
# Superpower 4: Code Generation
# ============================================================

print("=" * 50)
print("SUPERPOWER 4: Code Generation")
print("=" * 50)

response = llm.invoke("Write a Python function to check if a number is prime. Just the code, no explanation.")
print(f"Generated Code:\n{response.content}\n")

# ============================================================
# Superpower 5: Creative Writing
# ============================================================

print("=" * 50)
print("SUPERPOWER 5: Creative Writing")
print("=" * 50)

response = llm.invoke("Write a short story (4-5 sentences) about a robot learning to cook.")
print(f"Story:\n{response.content}\n")

# ============================================================
# Superpower 6: Reasoning (basic)
# ============================================================

print("=" * 50)
print("SUPERPOWER 6: Reasoning")
print("=" * 50)

response = llm.invoke("If I have 3 red balls and 2 blue balls in a bag, and I pick one without looking, what are the chances it's red? Explain briefly.")
print(f"Reasoning:\n{response.content}\n")

# ============================================================
# Superpower 7: Role Playing
# ============================================================

print("=" * 50)
print("SUPERPOWER 7: Role Playing")
print("=" * 50)

from langchain_core.messages import SystemMessage, HumanMessage

response = llm.invoke([
    SystemMessage(content="You are a friendly Indian grandmother. Respond with warmth and include one piece of life advice."),
    HumanMessage(content="I'm feeling stressed about my new job."),
])
print(f"AI Grandmother:\n{response.content}")

# ============================================================
# TODO 1: Test your own superpower
# ============================================================
# Try one of these:
#   a) "Explain quantum computing to a 5-year-old"
#   b) "Write a professional resignation letter"
#   c) "Convert this SQL to Python: SELECT name FROM users WHERE age > 25"
#   d) "Suggest 5 creative names for a coffee shop in Mumbai"

# response = llm.invoke("YOUR TASK HERE")
# print(f"\nResult: {response.content}")

# ============================================================
# TODO 2: Chain two superpowers
# ============================================================
# Ask the LLM to do two things in sequence:
#   1. Write a paragraph about any topic
#   2. Then pass that paragraph to summarize it
# This is a manual "chain" — in Session 3 you'll learn to do this automatically!

# paragraph = llm.invoke("Write a short paragraph about space exploration").content
# summary = llm.invoke(f"Summarize in one sentence: {paragraph}").content
# print(f"\nParagraph: {paragraph}")
# print(f"Summary: {summary}")

print("\n" + "=" * 50)
print("Lab 02 complete! LLMs are powerful text processors.")
print()
print("Key takeaways:")
print("- LLMs excel at: understanding, generating, translating, summarizing text")
print("- They can play roles, write code, and reason about simple problems")
print("- These superpowers are the BRAIN of an AI agent")
print("- But a brain alone has limits... (see Lab 03!)")
