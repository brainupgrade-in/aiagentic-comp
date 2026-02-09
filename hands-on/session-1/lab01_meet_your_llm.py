"""
Lab 01: Meet Your LLM
=======================
Goal: Talk to a local AI model for the very first time.

What you'll learn:
- An LLM is a program that understands and generates human language
- You send it a message, it sends back a response
- The LLM runs locally on your machine (via Ollama)
"""

# This line connects Python to the LLM running on your machine.
# Don't worry about the details yet — Session 3 explains this fully.
from langchain_ollama import ChatOllama

# Create a connection to the local Llama model
llm = ChatOllama(model="llama3.2:1b")

print("=" * 50)
print("  Welcome! You're about to talk to an AI.")
print("=" * 50)

# ============================================================
# Step 1: Your first message to the AI
# ============================================================
# .invoke() sends a message and waits for the response.
# It's like sending a text message and waiting for a reply.

print("\n--- Your First Message ---")
response = llm.invoke("Hello! What are you?")
print(f"You: Hello! What are you?")
print(f"AI:  {response.content}")

# ============================================================
# Step 2: Ask it a knowledge question
# ============================================================

print("\n--- Knowledge Question ---")
response = llm.invoke("What is the capital of India?")
print(f"You: What is the capital of India?")
print(f"AI:  {response.content}")

# ============================================================
# Step 3: Ask it to do something creative
# ============================================================

print("\n--- Creative Task ---")
response = llm.invoke("Write a 4-line poem about coding.")
print(f"You: Write a 4-line poem about coding.")
print(f"AI:  {response.content}")

# ============================================================
# Step 4: Look under the hood
# ============================================================
# The response isn't just text — it's an object with metadata.

print("\n--- Under the Hood ---")
response = llm.invoke("What is Python?")
print(f"Response type: {type(response).__name__}")
print(f"Text content:  {response.content[:100]}...")
print(f"Model used:    {response.response_metadata.get('model', 'unknown')}")

# ============================================================
# TODO 1: Ask YOUR question
# ============================================================
# What would you like to ask an AI? Uncomment and try!

# response = llm.invoke("YOUR QUESTION HERE")
# print(f"\nYour question's answer: {response.content}")

# ============================================================
# TODO 2: Ask it in a different language
# ============================================================
# Try asking in Hindi, Tamil, or any language you know.
# Does the AI understand and respond?

# response = llm.invoke("Namaste! Aap kaise hain?")
# print(f"\nHindi: {response.content}")

# ============================================================
# TODO 3: Ask something it SHOULDN'T know
# ============================================================
# Try asking about today's weather, or something that happened
# yesterday. What happens? (We'll explore this in Lab 03!)

# response = llm.invoke("What is the weather in Mumbai right now?")
# print(f"\nWeather: {response.content}")

print("\n" + "=" * 50)
print("Lab 01 complete! You just talked to an AI!")
print()
print("Key takeaways:")
print("- An LLM takes text in and gives text out")
print("- It knows a lot from its training data")
print("- It runs completely on your machine (via Ollama)")
print("- Each call is independent — it doesn't remember previous messages")
