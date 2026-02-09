"""
Lab 06: Memory — Stateless vs Stateful
========================================
Goal: Understand why memory matters and build a simple conversation memory.

What you'll learn:
- Without memory: every message is a fresh conversation
- With memory: the LLM can reference previous messages
- How short-term memory works (conversation buffer)
- The cost: more tokens per message as conversation grows
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: WITHOUT memory — the LLM forgets everything
# ============================================================

print("=" * 60)
print("WITHOUT Memory (Stateless)")
print("=" * 60)

# Each invoke() is independent — no connection between them.
r1 = llm.invoke([HumanMessage(content="My name is Priya and I work at Oracle.")])
print(f"Turn 1 → {r1.content}\n")

r2 = llm.invoke([HumanMessage(content="What is my name and where do I work?")])
print(f"Turn 2 → {r2.content}\n")

print("^ The LLM doesn't know! Each call is completely independent.\n")

# ============================================================
# Step 2: WITH memory — manually pass conversation history
# ============================================================

print("=" * 60)
print("WITH Memory (Stateful — manual)")
print("=" * 60)

# We keep a list of all messages and send the FULL list every time.
conversation = [
    SystemMessage(content="You are a helpful assistant. Be concise."),
]

# Turn 1
user_msg = "My name is Priya and I work at Oracle."
conversation.append(HumanMessage(content=user_msg))
response = llm.invoke(conversation)
conversation.append(AIMessage(content=response.content))
print(f"User: {user_msg}")
print(f"AI:   {response.content}\n")

# Turn 2
user_msg = "What is my name and where do I work?"
conversation.append(HumanMessage(content=user_msg))
response = llm.invoke(conversation)
conversation.append(AIMessage(content=response.content))
print(f"User: {user_msg}")
print(f"AI:   {response.content}\n")

# Turn 3
user_msg = "Suggest a good lunch place near my office."
conversation.append(HumanMessage(content=user_msg))
response = llm.invoke(conversation)
conversation.append(AIMessage(content=response.content))
print(f"User: {user_msg}")
print(f"AI:   {response.content}\n")

print(f"[Conversation has {len(conversation)} messages in memory]")

# ============================================================
# Step 3: Build a ChatBot class with memory
# ============================================================

print("\n" + "=" * 60)
print("ChatBot with Built-in Memory")
print("=" * 60)


class SimpleChatBot:
    """A chatbot with short-term memory (conversation buffer)."""

    def __init__(self, system_prompt: str, model: str = "llama3.2:1b"):
        self.llm = ChatOllama(model=model)
        self.history = [SystemMessage(content=system_prompt)]

    def chat(self, user_message: str) -> str:
        """Send a message and get a response. Remembers the conversation."""
        self.history.append(HumanMessage(content=user_message))
        response = self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content

    def get_history_length(self) -> int:
        """How many messages are in memory."""
        return len(self.history)

    def clear_memory(self):
        """Reset conversation (keep system prompt)."""
        self.history = [self.history[0]]


# Use the chatbot
bot = SimpleChatBot("You are a friendly travel assistant who helps plan trips. Be concise — 1-2 sentences.")

exchanges = [
    "I want to visit Japan in March.",
    "What should I pack?",
    "Any must-see places?",
    "How much budget should I plan for a week?",
]

for msg in exchanges:
    reply = bot.chat(msg)
    print(f"You: {msg}")
    print(f"Bot: {reply}")
    print(f"     [{bot.get_history_length()} messages in memory]\n")

# ============================================================
# Step 4: The memory problem — token growth
# ============================================================

print("=" * 60)
print("The Memory Problem: Token Growth")
print("=" * 60)

print(f"After 4 exchanges, memory has {bot.get_history_length()} messages.")
print("Each new message sends ALL previous messages to the LLM.")
print()
print("Imagine 100 exchanges:")
print("  - Message 1:   sends 2 messages   (system + user)")
print("  - Message 50:  sends 101 messages  (system + 50 user + 50 AI)")
print("  - Message 100: sends 201 messages  (system + 100 user + 100 AI)")
print()
print("Solutions (covered in later sessions):")
print("  1. Sliding window: keep only last N messages")
print("  2. Summarization: summarize old messages into a short context")
print("  3. Vector store: store messages in a DB, retrieve relevant ones")

# ============================================================
# Step 5: Sliding window memory (simple approach)
# ============================================================

print("\n" + "=" * 60)
print("Sliding Window Memory (keep last N exchanges)")
print("=" * 60)


class WindowedChatBot:
    """ChatBot that keeps only the last N exchanges in memory."""

    def __init__(self, system_prompt: str, max_exchanges: int = 3):
        self.llm = ChatOllama(model="llama3.2:1b")
        self.system_msg = SystemMessage(content=system_prompt)
        self.history = []
        self.max_messages = max_exchanges * 2  # Each exchange = user + AI

    def chat(self, user_message: str) -> str:
        self.history.append(HumanMessage(content=user_message))
        # Trim old messages (keep last N)
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
        messages = [self.system_msg] + self.history
        response = self.llm.invoke(messages)
        self.history.append(AIMessage(content=response.content))
        return response.content


wbot = WindowedChatBot("You are a helpful assistant. Be concise.", max_exchanges=2)

exchanges = [
    "My name is Raj.",
    "I love Python programming.",
    "I work at Google.",
    "What is my name?",  # Will it still remember?
]

for msg in exchanges:
    reply = wbot.chat(msg)
    print(f"You: {msg}")
    print(f"Bot: {reply}\n")

print("^ With window=2, the bot forgets messages older than 2 exchanges.")
print("  'What is my name?' may fail because that info was pushed out of the window.")

# ============================================================
# TODO 1: Build a persona chatbot
# ============================================================
# Use SimpleChatBot with a fun system prompt:
#   "You are Sherlock Holmes. Respond in character.
#    Reference your adventures and use deductive reasoning."
#
# Have a 5-message conversation and see if the bot stays in character.

# TODO: Create and test a persona chatbot

# ============================================================
# TODO 2: Implement summary memory
# ============================================================
# Instead of dropping old messages, summarize them:
#   1. When history > 6 messages, take the oldest 4
#   2. Ask the LLM to summarize them into 1 message
#   3. Replace the 4 messages with the 1 summary
#
# This preserves context while reducing token count.

# TODO: Implement SummaryChatBot

# ============================================================
# TODO 3: Compare — how many turns until memory fails?
# ============================================================
# Create a SimpleChatBot and a WindowedChatBot (window=3).
# Tell both: "My favorite number is 42" in turn 1.
# Then chat about random topics for several turns.
# Finally ask: "What is my favorite number?"
# At what point does the windowed bot forget?

# TODO: Test memory limits

print("\n" + "=" * 60)
print("Lab 06 complete! Key takeaways:")
print("- Without memory, every LLM call is independent")
print("- Short-term memory = send full conversation history")
print("- Memory grows linearly — need strategies to manage it")
print("- Sliding window: simple but lossy")
print("- Summary memory: preserves context, reduces tokens")
print("- LangChain/LangGraph handle this for you (Session 3+)")
