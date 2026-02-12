"""
Lab 02: Message Types — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# Without SystemMessage
print("--- Without SystemMessage ---")
response = llm.invoke("Explain what an API is")
print(response.content)
print()

# With SystemMessage: kindergarten teacher
print("--- With SystemMessage: 'Explain like I'm 5' ---")
messages = [
    SystemMessage(content="You are a kindergarten teacher. Explain everything using simple words and fun examples. Keep answers to 2 sentences."),
    HumanMessage(content="Explain what an API is"),
]
response = llm.invoke(messages)
print(response.content)
print()

# With SystemMessage: senior engineer
print("--- With SystemMessage: 'Senior Engineer' ---")
messages = [
    SystemMessage(content="You are a senior software engineer. Use technical terms. Be precise and concise. One sentence only."),
    HumanMessage(content="Explain what an API is"),
]
response = llm.invoke(messages)
print(response.content)
print()

# TODO 1: Custom persona — pirate
print("--- Custom Persona: Pirate ---")
messages = [
    SystemMessage(content="You are a pirate who explains technology. Use pirate language and sea metaphors. Keep it to 2 sentences."),
    HumanMessage(content="Explain what an API is"),
]
response = llm.invoke(messages)
print(response.content)
print()

# TODO 2: Format control — bullet points
print("--- Formatted Output: Bullet Points ---")
messages = [
    SystemMessage(content="Always respond in exactly 3 bullet points. Start each with a dash (-). No other format."),
    HumanMessage(content="What are the benefits of Python?"),
]
response = llm.invoke(messages)
print(response.content)
print()

# TODO 3: Multi-turn conversation
print("--- Multi-turn Conversation ---")
messages = [
    SystemMessage(content="You are a helpful assistant. Be concise."),
    HumanMessage(content="My favorite language is Python"),
    AIMessage(content="Great choice! Python is versatile and beginner-friendly."),
    HumanMessage(content="Why is it popular for AI?"),
]
response = llm.invoke(messages)
print(response.content)

print("\n" + "=" * 50)
print("Lab 02 complete!")
