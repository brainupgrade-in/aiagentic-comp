"""
Lab 01: Hello Groq!
====================
Goal: Switch from Ollama (Day 1) to Groq API (Day 2) and verify the connection.

What you'll learn:
- How to connect to Groq's cloud LLM using ChatGroq
- The difference between a 1B local model and a 70B cloud model
- That LangChain's model-agnostic design means only the import changes
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables from .env file (if it exists)
load_dotenv()

# ============================================================
# Step 1: Connect to Groq
# ============================================================
# Groq provides free API access to powerful LLMs.
# Your GROQ_API_KEY should be set as an environment variable.
# ChatGroq works exactly like ChatOllama — same .invoke() method!

print("Connecting to Groq API...")
llm = ChatGroq(model="llama-3.3-70b-versatile")
print("Connected!")
print("=" * 50)

# ============================================================
# Step 2: Send your first message via Groq
# ============================================================
# This is the same .invoke() call you used with Ollama,
# but now it runs a 70B parameter model on Groq's cloud.

response = llm.invoke("What is RAG in AI? Answer in 2 sentences.")

print("\n--- Response from Groq (70B model) ---")
print(f"Content: {response.content}")
print(f"\nModel used: {response.response_metadata.get('model_name', 'unknown')}")

# ============================================================
# Step 3: Test with structured messages
# ============================================================
# SystemMessage + HumanMessage work identically to Day 1.

response = llm.invoke([
    SystemMessage(content="You are a helpful AI assistant. Be concise."),
    HumanMessage(content="Explain embeddings in AI in one sentence."),
])

print("\n--- Structured message response ---")
print(response.content)

# ============================================================
# Step 4: Notice the quality difference
# ============================================================
# The 70B model gives much better responses than the 1B model.
# Same code, much smarter model — that's the power of Groq + LangChain.

response = llm.invoke([
    SystemMessage(content="You are a Python expert. Be concise but accurate."),
    HumanMessage(content="What are the top 3 differences between a list and a tuple in Python?"),
])

print("\n--- Quality test (complex question) ---")
print(response.content)

# ============================================================
# TODO 1: Ask your own question
# ============================================================
# Try asking the 70B model something that the 1B model struggled with.
# Suggestions: a math problem, a reasoning puzzle, or a code question.

# TODO: Uncomment and modify
# my_response = llm.invoke("YOUR QUESTION HERE")
# print(f"\nMy question: {my_response.content}")

# ============================================================
# TODO 2: Test with a different Groq model
# ============================================================
# Groq offers multiple models. Try switching to a smaller one:
#   - "llama-3.1-8b-instant" (faster, less capable)
#   - "mixtral-8x7b-32768" (different architecture)
# Compare the response quality and speed.

# TODO: Uncomment and try a different model
# llm_fast = ChatGroq(model="llama-3.1-8b-instant")
# fast_response = llm_fast.invoke("Explain Docker containers in 2 sentences.")
# print(f"\n8B model: {fast_response.content}")
#
# smart_response = llm.invoke("Explain Docker containers in 2 sentences.")
# print(f"\n70B model: {smart_response.content}")

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- ChatGroq connects to Groq's cloud API (free, fast)")
print("- Same .invoke() API as ChatOllama — only import changes")
print("- 70B model is significantly better than 1B for complex tasks")
print("- GROQ_API_KEY must be set as an environment variable")
