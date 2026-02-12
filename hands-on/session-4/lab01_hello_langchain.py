"""
Lab 01: Hello LangChain
========================
Goal: Connect to a local LLM (Ollama) using LangChain and send your first message.

What you'll learn:
- How to import and create a ChatOllama model
- How to use .invoke() to send a message
- What the response object looks like (AIMessage)
"""

from langchain_ollama import ChatOllama

# ============================================================
# Step 1: Create a connection to the local Ollama LLM
# ============================================================
# ChatOllama connects to the Ollama server running on your machine.
# We use "llama3.2:1b" — a small but capable model.

llm = ChatOllama(model="llama3.2:1b")

print("Connected to Ollama!")
print("=" * 50)

# ============================================================
# Step 2: Send a simple message using .invoke()
# ============================================================
# .invoke() sends a message and waits for the complete response.

response = llm.invoke("What is Python in one sentence?")

# Let's look at what we get back
print("\n--- Full Response Object ---")
print(f"Type: {type(response)}")
print(f"Content: {response.content}")
print(f"Metadata: {response.response_metadata}")

# ============================================================
# Step 3: The response is an AIMessage object
# ============================================================
# The key property is .content — that's the text the LLM generated.

print("\n--- Just the text ---")
print(response.content)

# ============================================================
# TODO 1: Ask the LLM a different question
# ============================================================
# Replace the question below with anything you're curious about.
# Try: "Explain Docker in one sentence" or "What is Kubernetes?"

# TODO: Uncomment and modify the line below
# my_response = llm.invoke("YOUR QUESTION HERE")
# print(f"\nMy question's answer: {my_response.content}")

# ============================================================
# TODO 2: Ask two different questions and compare responses
# ============================================================
# Notice how each .invoke() call is independent — the LLM doesn't
# remember the previous question. (We'll fix this with "memory" later!)

# TODO: Send two related questions and observe that the LLM has no memory
# response1 = llm.invoke("My name is Raj")
# print(f"\nResponse 1: {response1.content}")
#
# response2 = llm.invoke("What is my name?")
# print(f"\nResponse 2: {response2.content}")
# ^ The LLM won't know your name! Each call is independent.

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- ChatOllama connects LangChain to your local Ollama")
print("- .invoke() sends a message and returns an AIMessage")
print("- .content gives you the text response")
print("- Each .invoke() call is independent (no memory yet)")
