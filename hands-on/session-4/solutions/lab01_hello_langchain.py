"""
Lab 01: Hello LangChain — SOLUTION
"""

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

print("Connected to Ollama!")
print("=" * 50)

# Step 2: Send a simple message
response = llm.invoke("What is Python in one sentence?")

print("\n--- Full Response Object ---")
print(f"Type: {type(response)}")
print(f"Content: {response.content}")
print(f"Metadata: {response.response_metadata}")

print("\n--- Just the text ---")
print(response.content)

# TODO 1: Ask a different question
my_response = llm.invoke("Explain Docker in one sentence")
print(f"\nMy question's answer: {my_response.content}")

# TODO 2: Demonstrate no memory between calls
response1 = llm.invoke("My name is Raj")
print(f"\nResponse 1: {response1.content}")

response2 = llm.invoke("What is my name?")
print(f"\nResponse 2: {response2.content}")
# The LLM won't know the name — each call is independent!

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- ChatOllama connects LangChain to your local Ollama")
print("- .invoke() sends a message and returns an AIMessage")
print("- .content gives you the text response")
print("- Each .invoke() call is independent (no memory yet)")
