"""
Lab 01: Meet Your LLM — SOLUTION
"""

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

print("=" * 50)
print("  Welcome! You're about to talk to an AI.")
print("=" * 50)

# Step 1: First message
print("\n--- Your First Message ---")
response = llm.invoke("Hello! What are you?")
print(f"You: Hello! What are you?")
print(f"AI:  {response.content}")

# Step 2: Knowledge question
print("\n--- Knowledge Question ---")
response = llm.invoke("What is the capital of India?")
print(f"You: What is the capital of India?")
print(f"AI:  {response.content}")

# Step 3: Creative task
print("\n--- Creative Task ---")
response = llm.invoke("Write a 4-line poem about coding.")
print(f"You: Write a 4-line poem about coding.")
print(f"AI:  {response.content}")

# Step 4: Under the hood
print("\n--- Under the Hood ---")
response = llm.invoke("What is Python?")
print(f"Response type: {type(response).__name__}")
print(f"Text content:  {response.content[:100]}...")
print(f"Model used:    {response.response_metadata.get('model', 'unknown')}")

# TODO 1: Custom question
print("\n--- Custom Question ---")
response = llm.invoke("Explain Docker in one sentence")
print(f"Q: Explain Docker in one sentence")
print(f"A: {response.content}")

# TODO 2: Different language
print("\n--- Hindi ---")
response = llm.invoke("Namaste! Aap kaise hain?")
print(f"Q: Namaste! Aap kaise hain?")
print(f"A: {response.content}")

# TODO 3: Something it shouldn't know
print("\n--- Weather (can't know!) ---")
response = llm.invoke("What is the weather in Mumbai right now?")
print(f"Q: What is the weather in Mumbai right now?")
print(f"A: {response.content}")
print("(Notice: it either makes something up or says it can't access live data)")

print("\nLab 01 complete!")
