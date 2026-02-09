"""
Lab 02: Exploring LLM Superpowers — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# Superpower 1: Language Understanding
print("=" * 50)
print("SUPERPOWER 1: Language Understanding")
print("=" * 50)

response = llm.invoke("Is this review positive or negative? 'The food was amazing but the service was terrible and we waited 45 minutes.'")
print(f"Sentiment: {response.content}\n")

response = llm.invoke("Extract name, city, job: 'Priya from Bangalore works as a data scientist at Oracle.'")
print(f"Extraction: {response.content}\n")

# Superpower 2: Translation
print("=" * 50)
print("SUPERPOWER 2: Translation")
print("=" * 50)
for lang in ["French", "Japanese", "Hindi"]:
    response = llm.invoke(f"Translate 'Good morning, how are you?' to {lang}. Only the translation.")
    print(f"  {lang}: {response.content}")

# Superpower 3: Summarization
print(f"\n{'=' * 50}")
print("SUPERPOWER 3: Summarization")
print("=" * 50)
long_text = """Docker is a platform designed to help developers build, share, and run container
applications. It handles the tedious setup, so you can focus on the code. Containers
are lightweight and contain everything needed to run an application, so there's no
need to rely on what's installed on the host."""
response = llm.invoke(f"Summarize in ONE sentence:\n\n{long_text}")
print(f"Summary: {response.content}\n")

# Superpower 4: Code Generation
print("=" * 50)
print("SUPERPOWER 4: Code Generation")
print("=" * 50)
response = llm.invoke("Write a Python function to check if a number is prime. Just code.")
print(f"Code:\n{response.content}\n")

# Superpower 5: Creative Writing
print("=" * 50)
print("SUPERPOWER 5: Creative Writing")
print("=" * 50)
response = llm.invoke("Write a 4-sentence story about a robot learning to cook.")
print(f"Story:\n{response.content}\n")

# Superpower 6: Reasoning
print("=" * 50)
print("SUPERPOWER 6: Reasoning")
print("=" * 50)
response = llm.invoke("3 red and 2 blue balls. What are the chances of picking red? Explain briefly.")
print(f"Reasoning:\n{response.content}\n")

# Superpower 7: Role Playing
print("=" * 50)
print("SUPERPOWER 7: Role Playing")
print("=" * 50)
response = llm.invoke([
    SystemMessage(content="You are a friendly Indian grandmother. Respond with warmth and advice."),
    HumanMessage(content="I'm stressed about my new job."),
])
print(f"AI Grandmother:\n{response.content}\n")

# TODO 1: Custom superpowers
print("=" * 50)
print("CUSTOM TESTS")
print("=" * 50)

response = llm.invoke("Explain quantum computing to a 5-year-old")
print(f"For a 5-year-old:\n{response.content}\n")

response = llm.invoke("Suggest 5 creative names for a coffee shop in Mumbai")
print(f"Coffee shop names:\n{response.content}\n")

# TODO 2: Chain two superpowers
print("=" * 50)
print("CHAINING: Write → Summarize")
print("=" * 50)

paragraph = llm.invoke("Write a short paragraph about space exploration").content
summary = llm.invoke(f"Summarize in one sentence: {paragraph}").content
print(f"Paragraph: {paragraph}\n")
print(f"Summary: {summary}")

print("\nLab 02 complete!")
