"""
Lab 05: Conversation Memory Basics — SOLUTION
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

print("=" * 50)
print("  Conversation Memory Basics — SOLUTION")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile")

# Step 1: LLMs are stateless
print("\n--- Step 1: LLMs Are Stateless ---")
response1 = llm.invoke([HumanMessage(content="My name is Priya and I work in the Bangalore office.")])
print(f"Turn 1: {response1.content[:150]}")

response2 = llm.invoke([HumanMessage(content="What is my name and where do I work?")])
print(f"Turn 2: {response2.content[:150]}")
print("\n→ The LLM has NO memory of the previous message!")

# Step 2: Add memory with a message list
print("\n--- Step 2: Memory via Message List ---")
conversation = [
    SystemMessage(content="You are a helpful UniGPS HR assistant. Be concise."),
    HumanMessage(content="My name is Priya and I work in the Bangalore office."),
]

response1 = llm.invoke(conversation)
print(f"Turn 1: {response1.content[:150]}")

conversation.append(AIMessage(content=response1.content))
conversation.append(HumanMessage(content="What is my name and where do I work?"))
response2 = llm.invoke(conversation)
print(f"Turn 2: {response2.content[:150]}")
print("\n→ With the full message list, the LLM remembers!")

# Step 3: Multi-turn conversation
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

# Step 4: Inspect the history
print("--- Step 4: Message History ---")
print(f"Total messages in history: {len(history)}")
for i, msg in enumerate(history):
    role = msg.type.upper()
    preview = msg.content[:50].replace('\n', ' ')
    print(f"  [{i}] {role:8s}: {preview}...")

# Step 5: The problem with unlimited history
print("\n--- Step 5: History Grows! ---")
total_chars = sum(len(m.content) for m in history)
print(f"Total characters in history: {total_chars}")
print(f"Total messages: {len(history)}")

# TODO 1: Persona-driven conversation
print("\n--- TODO 1: Chef Raju Persona ---")
chef_history = [
    SystemMessage(content="You are Chef Raju, a friendly Indian cooking assistant. "
                  "You love South Indian cuisine and always suggest dosa variations. "
                  "Keep answers short and enthusiastic."),
]
for q in ["What should I make for breakfast?", "Any dosa suggestions?", "What about lunch?"]:
    chef_history.append(HumanMessage(content=q))
    response = llm.invoke(chef_history)
    chef_history.append(AIMessage(content=response.content))
    print(f"User: {q}")
    print(f"Chef Raju: {response.content[:150]}")
    print()

# TODO 2: Simple chat loop (non-interactive for solution)
print("--- TODO 2: Chat Loop (demo) ---")
chat_history = [
    SystemMessage(content="You are a helpful UniGPS assistant. Be concise."),
]
demo_questions = ["Hi, I'm new here!", "What's the WFH policy?", "Thanks!"]
for q in demo_questions:
    chat_history.append(HumanMessage(content=q))
    response = llm.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    print(f"You: {q}")
    print(f"AI:  {response.content[:150]}")
    print()

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- LLMs are stateless — they don't remember between calls")
print("- A message list (conversation history) adds memory")
print("- Each call sends the FULL history to the LLM")
print("- SystemMessage sets the assistant's persona and rules")
print("- History grows with every turn — needs management (Lab 06)")
