"""
Lab 03: LLM Limitations — SOLUTION
"""

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

# Limitation 1: No Memory
print("=" * 50)
print("LIMITATION 1: No Memory")
print("=" * 50)
llm.invoke("My name is Raj and I live in Bangalore.")
r = llm.invoke("What is my name and where do I live?")
print(f"Without memory: {r.content}\n")

# Limitation 2: No Real-Time Info
print("=" * 50)
print("LIMITATION 2: No Real-Time Info")
print("=" * 50)
r = llm.invoke("What is the weather in Mumbai right now?")
print(f"Weather: {r.content}\n")
r = llm.invoke("What is the current price of Bitcoin?")
print(f"Bitcoin: {r.content}\n")

# Limitation 3: Unreliable Math
print("=" * 50)
print("LIMITATION 3: Unreliable Math")
print("=" * 50)
for q, correct in [("17 x 28", 476), ("1234 + 5678", 6912), ("15% of 847", 127.05)]:
    r = llm.invoke(f"What is {q}? Reply with ONLY the number.")
    print(f"  {q}: AI={r.content.strip()}, Correct={correct}")
print()

# Limitation 4: Can't Take Actions
print("=" * 50)
print("LIMITATION 4: Can't Take Actions")
print("=" * 50)
r = llm.invoke("Send an email to raj@example.com saying 'Meeting at 3 PM'")
print(f"Email: {r.content}\n")

# Limitation 5: Hallucination
print("=" * 50)
print("LIMITATION 5: Hallucination")
print("=" * 50)
r = llm.invoke("Tell me about the Python library called 'superfast_ml' and who created it.")
print(f"Fake library: {r.content}\n")

# TODO 1: More limitations
print("=" * 50)
print("TODO 1: More Limitations")
print("=" * 50)

r = llm.invoke("What time is it?")
print(f"Time: {r.content}\n")

r = llm.invoke("Count the words in: The quick brown fox jumps over the lazy dog")
print(f"Word count: {r.content}")
print(f"Correct: 9 words\n")

# TODO 2: Recent vs old knowledge
print("=" * 50)
print("TODO 2: Recent vs Old")
print("=" * 50)

r = llm.invoke("Who won the 2024 Olympics 100m sprint?")
print(f"2024 Olympics: {r.content}\n")

r = llm.invoke("Who was the US President in 2020?")
print(f"2020 President: {r.content}")

print("\nLab 03 complete!")
