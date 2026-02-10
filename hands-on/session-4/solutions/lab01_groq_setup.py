"""
Lab 01: Hello Groq! — SOLUTION
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")

print("Connected to Groq!")
print("=" * 50)

# Step 2: First message
response = llm.invoke("What is RAG in AI? Answer in 2 sentences.")
print("\n--- Response from Groq (70B model) ---")
print(f"Content: {response.content}")
print(f"\nModel used: {response.response_metadata.get('model_name', 'unknown')}")

# Step 3: Structured messages
response = llm.invoke([
    SystemMessage(content="You are a helpful AI assistant. Be concise."),
    HumanMessage(content="Explain embeddings in AI in one sentence."),
])
print("\n--- Structured message response ---")
print(response.content)

# Step 4: Quality test
response = llm.invoke([
    SystemMessage(content="You are a Python expert. Be concise but accurate."),
    HumanMessage(content="What are the top 3 differences between a list and a tuple in Python?"),
])
print("\n--- Quality test ---")
print(response.content)

# TODO 1: Custom question
my_response = llm.invoke("Solve this step by step: If a train travels 120 km in 2 hours, what is its speed in m/s?")
print(f"\nMy question: {my_response.content}")

# TODO 2: Compare models
llm_fast = ChatGroq(model="llama-3.1-8b-instant")
fast_response = llm_fast.invoke("Explain Docker containers in 2 sentences.")
print(f"\n8B model: {fast_response.content}")

smart_response = llm.invoke("Explain Docker containers in 2 sentences.")
print(f"\n70B model: {smart_response.content}")

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- ChatGroq connects to Groq's cloud API (free, fast)")
print("- Same .invoke() API as ChatOllama — only import changes")
print("- 70B model is significantly better than 1B for complex tasks")
print("- GROQ_API_KEY must be set as an environment variable")
