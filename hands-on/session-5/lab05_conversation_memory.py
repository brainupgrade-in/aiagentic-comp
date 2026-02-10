"""
Lab 05: Conversation Memory Basics
=====================================
Goal: Understand why LLMs are stateless and how to add memory
      by maintaining a message history.

What you'll learn:
- Why LLMs forget everything between calls
- How to maintain a message list for conversation memory
- How message history enables multi-turn conversations
- The role of SystemMessage in setting assistant persona
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

print("=" * 50)
print("  Conversation Memory Basics")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile")

# ============================================================
# Step 1: LLMs are stateless — they forget!
# ============================================================
# Each LLM call is independent. The model has NO memory of
# previous calls. Watch what happens:

print("\n--- Step 1: LLMs Are Stateless ---")
response1 = llm.invoke([HumanMessage(content="My name is Priya and I work in the Bangalore office.")])
print(f"Turn 1: {response1.content[:150]}")

response2 = llm.invoke([HumanMessage(content="What is my name and where do I work?")])
print(f"Turn 2: {response2.content[:150]}")
print("\n→ The LLM has NO memory of the previous message!")

# ============================================================
# Step 2: Add memory with a message list
# ============================================================
# The fix: send the FULL conversation history with each call.
# We maintain a Python list of messages.

print("\n--- Step 2: Memory via Message List ---")
conversation = [
    SystemMessage(content="You are a helpful UniGPS HR assistant. Be concise."),
    HumanMessage(content="My name is Priya and I work in the Bangalore office."),
]

response1 = llm.invoke(conversation)
print(f"Turn 1: {response1.content[:150]}")

# Add the AI's response to history
conversation.append(AIMessage(content=response1.content))

# Now ask a follow-up — this time including ALL previous messages
conversation.append(HumanMessage(content="What is my name and where do I work?"))
response2 = llm.invoke(conversation)
print(f"Turn 2: {response2.content[:150]}")
print("\n→ With the full message list, the LLM remembers!")

# ============================================================
# Step 3: Multi-turn conversation
# ============================================================
# Let's have a longer conversation and see memory in action.

print("\n--- Step 3: Multi-Turn Conversation ---")
history = [
    SystemMessage(content="You are a UniGPS IT support assistant. Be helpful and concise."),
]

questions = [
    "I need a new monitor for my desk.",
    "What's the budget limit for it?",
    "How do I submit the request?",
    "Thanks! One more thing — can I also get a keyboard?",
]

for q in questions:
    history.append(HumanMessage(content=q))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))
    print(f"User: {q}")
    print(f"AI:   {response.content[:150]}")
    print()

# ============================================================
# Step 4: Inspect the history
# ============================================================
# Let's see what the message list looks like.

print("--- Step 4: Message History ---")
print(f"Total messages in history: {len(history)}")
for i, msg in enumerate(history):
    role = msg.type.upper()
    preview = msg.content[:50].replace('\n', ' ')
    print(f"  [{i}] {role:8s}: {preview}...")

# ============================================================
# Step 5: The problem with unlimited history
# ============================================================

print("\n--- Step 5: History Grows! ---")
total_chars = sum(len(m.content) for m in history)
print(f"Total characters in history: {total_chars}")
print(f"Total messages: {len(history)}")
print("As conversations get longer, this grows without limit!")
print("→ More tokens = more cost = slower responses")
print("We'll fix this in Lab 06 with memory strategies.")

# ============================================================
# TODO 1: Persona-driven conversation
# ============================================================
# Create a conversation where the assistant has a specific persona.
# Use a SystemMessage like:
#   "You are Chef Raju, a friendly Indian cooking assistant. You love
#    South Indian cuisine and always suggest dosa variations."
# Have a 3-turn conversation and verify the persona is maintained.

# chef_history = [
#     SystemMessage(content="You are Chef Raju, a friendly Indian cooking assistant..."),
# ]
# for q in ["What should I make for breakfast?", "Any dosa suggestions?", "What about lunch?"]:
#     chef_history.append(HumanMessage(content=q))
#     response = llm.invoke(chef_history)
#     chef_history.append(AIMessage(content=response.content))
#     print(f"User: {q}")
#     print(f"Chef Raju: {response.content[:150]}")

# ============================================================
# TODO 2: Simple chat loop
# ============================================================
# Build a simple interactive chat loop that maintains history.

# chat_history = [
#     SystemMessage(content="You are a helpful UniGPS assistant. Be concise."),
# ]
# print("\nChat with UniGPS assistant (type 'quit' to exit):")
# while True:
#     user_input = input("You: ").strip()
#     if user_input.lower() in ("quit", "exit", "q"):
#         break
#     if not user_input:
#         continue
#     chat_history.append(HumanMessage(content=user_input))
#     response = llm.invoke(chat_history)
#     chat_history.append(AIMessage(content=response.content))
#     print(f"AI: {response.content}")

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- LLMs are stateless — they don't remember between calls")
print("- A message list (conversation history) adds memory")
print("- Each call sends the FULL history to the LLM")
print("- SystemMessage sets the assistant's persona and rules")
print("- History grows with every turn — needs management (Lab 06)")
