"""
Lab 02: Message Types
======================
Goal: Understand how SystemMessage and HumanMessage control LLM behavior.

What you'll learn:
- SystemMessage sets the LLM's personality and rules
- HumanMessage is the user's input
- How changing the system message dramatically changes the response
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Without a SystemMessage (basic call)
# ============================================================
# When you pass a plain string, LangChain wraps it in a HumanMessage.

print("--- Without SystemMessage ---")
response = llm.invoke("Explain what an API is")
print(response.content)
print()

# ============================================================
# Step 2: With a SystemMessage (controlled behavior)
# ============================================================
# A SystemMessage is like a job description for the LLM.
# It tells the LLM HOW to respond — tone, format, rules.

print("--- With SystemMessage: 'Explain like I'm 5' ---")
messages = [
    SystemMessage(content="You are a kindergarten teacher. Explain everything using simple words and fun examples. Keep answers to 2 sentences."),
    HumanMessage(content="Explain what an API is"),
]
response = llm.invoke(messages)
print(response.content)
print()

# ============================================================
# Step 3: Same question, different persona
# ============================================================

print("--- With SystemMessage: 'Senior Engineer' ---")
messages = [
    SystemMessage(content="You are a senior software engineer. Use technical terms. Be precise and concise. One sentence only."),
    HumanMessage(content="Explain what an API is"),
]
response = llm.invoke(messages)
print(response.content)
print()

# ============================================================
# TODO 1: Create your own persona
# ============================================================
# Try making the LLM respond as:
#   - A pirate ("Arr! An API be...")
#   - A poet (explain in a rhyme)
#   - A cricket commentator

# TODO: Create a messages list with your custom SystemMessage
# messages = [
#     SystemMessage(content="YOUR PERSONA HERE"),
#     HumanMessage(content="Explain what an API is"),
# ]
# response = llm.invoke(messages)
# print(f"--- Custom Persona ---")
# print(response.content)

# ============================================================
# TODO 2: Use SystemMessage to control output format
# ============================================================
# SystemMessage can also enforce format rules.
# Try: "Always respond in exactly 3 bullet points. No other format."

# TODO: Create a SystemMessage that forces bullet-point output
# messages = [
#     SystemMessage(content="YOUR FORMAT RULE HERE"),
#     HumanMessage(content="What are the benefits of Python?"),
# ]
# response = llm.invoke(messages)
# print(f"\n--- Formatted Output ---")
# print(response.content)

# ============================================================
# TODO 3: Multi-turn conversation (manual)
# ============================================================
# You can simulate a conversation by including previous messages.
# The LLM will use the full message history as context.

# from langchain_core.messages import AIMessage
# messages = [
#     SystemMessage(content="You are a helpful assistant. Be concise."),
#     HumanMessage(content="My favorite language is Python"),
#     AIMessage(content="Great choice! Python is versatile and beginner-friendly."),
#     HumanMessage(content="Why is it popular for AI?"),
# ]
# response = llm.invoke(messages)
# print(f"\n--- Multi-turn ---")
# print(response.content)

print("=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- SystemMessage controls HOW the LLM responds")
print("- Same question + different SystemMessage = different answer")
print("- You can enforce persona, tone, format, and rules")
print("- Message lists simulate conversation history")
