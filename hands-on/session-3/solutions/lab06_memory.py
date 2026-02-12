"""
Lab 06: Memory — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# Step 1: Without memory
print("=" * 60)
print("WITHOUT Memory")
print("=" * 60)

r1 = llm.invoke([HumanMessage(content="My name is Priya and I work at Oracle.")])
print(f"Turn 1 → {r1.content}\n")

r2 = llm.invoke([HumanMessage(content="What is my name and where do I work?")])
print(f"Turn 2 → {r2.content}\n")

# Step 2: With memory
print("=" * 60)
print("WITH Memory")
print("=" * 60)

conversation = [SystemMessage(content="You are a helpful assistant. Be concise.")]

for user_msg in [
    "My name is Priya and I work at Oracle.",
    "What is my name and where do I work?",
    "Suggest a good lunch place near my office.",
]:
    conversation.append(HumanMessage(content=user_msg))
    response = llm.invoke(conversation)
    conversation.append(AIMessage(content=response.content))
    print(f"User: {user_msg}")
    print(f"AI:   {response.content}\n")

# Step 3: ChatBot class
print("=" * 60)
print("ChatBot with Memory")
print("=" * 60)


class SimpleChatBot:
    def __init__(self, system_prompt: str, model: str = "llama3.2:1b"):
        self.llm = ChatOllama(model=model)
        self.history = [SystemMessage(content=system_prompt)]

    def chat(self, user_message: str) -> str:
        self.history.append(HumanMessage(content=user_message))
        response = self.llm.invoke(self.history)
        self.history.append(AIMessage(content=response.content))
        return response.content

    def get_history_length(self) -> int:
        return len(self.history)

    def clear_memory(self):
        self.history = [self.history[0]]


bot = SimpleChatBot("You are a friendly travel assistant. Be concise — 1-2 sentences.")
for msg in [
    "I want to visit Japan in March.",
    "What should I pack?",
    "Any must-see places?",
    "How much budget should I plan for a week?",
]:
    reply = bot.chat(msg)
    print(f"You: {msg}")
    print(f"Bot: {reply}")
    print(f"     [{bot.get_history_length()} messages]\n")

# Step 5: Sliding window
print("=" * 60)
print("Sliding Window Memory")
print("=" * 60)


class WindowedChatBot:
    def __init__(self, system_prompt: str, max_exchanges: int = 3):
        self.llm = ChatOllama(model="llama3.2:1b")
        self.system_msg = SystemMessage(content=system_prompt)
        self.history = []
        self.max_messages = max_exchanges * 2

    def chat(self, user_message: str) -> str:
        self.history.append(HumanMessage(content=user_message))
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
        messages = [self.system_msg] + self.history
        response = self.llm.invoke(messages)
        self.history.append(AIMessage(content=response.content))
        return response.content


wbot = WindowedChatBot("You are a helpful assistant. Be concise.", max_exchanges=2)
for msg in [
    "My name is Raj.",
    "I love Python programming.",
    "I work at Google.",
    "What is my name?",
]:
    reply = wbot.chat(msg)
    print(f"You: {msg}")
    print(f"Bot: {reply}\n")

# TODO 1: Persona chatbot
print("=" * 60)
print("TODO 1: Sherlock Holmes Chatbot")
print("=" * 60)

sherlock = SimpleChatBot(
    "You are Sherlock Holmes. Respond in character. Reference your adventures, "
    "use deductive reasoning, and speak in a Victorian manner. Be concise."
)

for msg in [
    "Good evening, Mr. Holmes. I need your help.",
    "Someone has been stealing files from our office at night.",
    "We found a muddy footprint near the window.",
    "The security guard says he saw nothing unusual.",
    "What do you deduce?",
]:
    reply = sherlock.chat(msg)
    print(f"You:      {msg}")
    print(f"Sherlock: {reply}\n")

# TODO 2: Summary memory
print("=" * 60)
print("TODO 2: Summary Memory ChatBot")
print("=" * 60)


class SummaryChatBot:
    def __init__(self, system_prompt: str, summarize_after: int = 6):
        self.llm = ChatOllama(model="llama3.2:1b")
        self.system_msg = SystemMessage(content=system_prompt)
        self.history = []
        self.summarize_after = summarize_after

    def chat(self, user_message: str) -> str:
        self.history.append(HumanMessage(content=user_message))

        # Summarize old messages if history is too long
        if len(self.history) > self.summarize_after:
            old_messages = self.history[:4]
            old_text = "\n".join(
                f"{'User' if isinstance(m, HumanMessage) else 'AI'}: {m.content}"
                for m in old_messages
            )
            summary = self.llm.invoke([
                SystemMessage(content="Summarize this conversation in 2 sentences. Preserve key facts."),
                HumanMessage(content=old_text),
            ]).content
            self.history = [HumanMessage(content=f"[Earlier conversation summary: {summary}]")] + self.history[4:]
            print(f"  [Summarized! History compressed to {len(self.history)} messages]")

        messages = [self.system_msg] + self.history
        response = self.llm.invoke(messages)
        self.history.append(AIMessage(content=response.content))
        return response.content


sbot = SummaryChatBot("You are a helpful assistant. Be concise.", summarize_after=6)
for msg in [
    "My favorite number is 42.",
    "I'm learning Python for data science.",
    "I work at Oracle in Bangalore.",
    "What's a good Python library for data analysis?",
    "Can you remind me of my favorite number?",
]:
    reply = sbot.chat(msg)
    print(f"You: {msg}")
    print(f"Bot: {reply}\n")

# TODO 3: Memory limit comparison
print("=" * 60)
print("TODO 3: Memory Limit Comparison")
print("=" * 60)

full_bot = SimpleChatBot("You are a helpful assistant. Be concise.")
win_bot = WindowedChatBot("You are a helpful assistant. Be concise.", max_exchanges=3)

full_bot.chat("My favorite number is 42.")
win_bot.chat("My favorite number is 42.")

for msg in [
    "Tell me about Python.",
    "What is Docker?",
    "Explain Kubernetes.",
    "What is REST API?",
]:
    full_bot.chat(msg)
    win_bot.chat(msg)

full_answer = full_bot.chat("What is my favorite number?")
win_answer = win_bot.chat("What is my favorite number?")

print(f"Full memory bot: {full_answer}")
print(f"Window (3) bot:  {win_answer}")
print(f"\nFull memory keeps everything — window forgets old messages!")
