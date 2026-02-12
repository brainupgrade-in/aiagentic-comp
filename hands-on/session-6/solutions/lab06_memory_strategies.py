"""
Lab 06: Memory Strategies — SOLUTION
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

print("=" * 50)
print("  Memory Strategies — SOLUTION")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile")

# Sample long conversation
SAMPLE_CONVERSATION = [
    SystemMessage(content="You are a UniGPS HR assistant. Be concise."),
    HumanMessage(content="How many annual leave days do I get?"),
    AIMessage(content="Full-time employees get 24 days of annual leave per year."),
    HumanMessage(content="Can I carry forward unused leave?"),
    AIMessage(content="No, unused annual leave cannot be carried forward to the next financial year."),
    HumanMessage(content="What about sick leave?"),
    AIMessage(content="You get 12 sick days per year. Unused sick leave can be carried forward up to 30 days."),
    HumanMessage(content="Do I need a doctor's note for sick leave?"),
    AIMessage(content="Yes, for absences exceeding 2 consecutive days, a medical certificate is required."),
    HumanMessage(content="What's the WFH policy?"),
    AIMessage(content="Up to 3 days/week with team lead approval. Core hours 10 AM-4 PM. Friday is mandatory in-office."),
    HumanMessage(content="What about internet reimbursement?"),
    AIMessage(content="Rs 1,500/month for WFH employees. Submit your broadband bill by the 5th of each month."),
]

total_chars = sum(len(m.content) for m in SAMPLE_CONVERSATION)
print(f"Sample conversation: {len(SAMPLE_CONVERSATION)} messages, {total_chars} chars")

# Strategy 1: Buffer Memory
print("\n--- Strategy 1: Buffer Memory ---")

def buffer_memory(messages):
    """Keep all messages."""
    return list(messages)

buffered = buffer_memory(SAMPLE_CONVERSATION)
print(f"Messages kept: {len(buffered)}")
print(f"Characters:    {sum(len(m.content) for m in buffered)}")

# Strategy 2: Window Memory
print("\n--- Strategy 2: Window Memory ---")

def window_memory(messages, window_size=3):
    """Keep the system message and the last N human-AI exchange pairs."""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    keep = non_system[-(window_size * 2):]
    return system_msgs + keep

for window in [2, 3, 5]:
    windowed = window_memory(SAMPLE_CONVERSATION, window)
    chars = sum(len(m.content) for m in windowed)
    print(f"  Window={window}: {len(windowed)} messages, {chars} chars")

print("\nTesting window=2 with follow-up question:")
windowed = window_memory(SAMPLE_CONVERSATION, window_size=2)
follow_up = windowed + [HumanMessage(content="Remind me, how much is the internet reimbursement?")]
response = llm.invoke(follow_up)
print(f"  Q: Remind me, how much is the internet reimbursement?")
print(f"  A: {response.content[:150]}")

# Strategy 3: Summary Memory
print("\n--- Strategy 3: Summary Memory ---")

def summary_memory(messages, llm):
    """Summarize older messages, keep recent ones."""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]

    if len(non_system) <= 4:
        return messages

    old_messages = non_system[:-4]
    recent_messages = non_system[-4:]

    conversation_text = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in old_messages
    )
    summary_prompt = (
        f"Summarize this conversation in 2-3 sentences, "
        f"capturing key facts discussed:\n\n{conversation_text}"
    )
    summary = llm.invoke([HumanMessage(content=summary_prompt)]).content

    return system_msgs + [
        SystemMessage(content=f"Previous conversation summary: {summary}"),
    ] + recent_messages

summarized = summary_memory(SAMPLE_CONVERSATION, llm)
summary_chars = sum(len(m.content) for m in summarized)
print(f"Original:      {len(SAMPLE_CONVERSATION)} messages, {total_chars} chars")
print(f"After summary: {len(summarized)} messages, {summary_chars} chars")
print(f"Compression:   {(1 - summary_chars/total_chars)*100:.0f}% reduction")

for m in summarized:
    if isinstance(m, SystemMessage) and "summary" in m.content.lower():
        print(f"\nGenerated summary: {m.content[:200]}")

follow_up = summarized + [HumanMessage(content="Based on what we discussed, can I carry forward my sick leave?")]
response = llm.invoke(follow_up)
print(f"\nQ: Can I carry forward my sick leave?")
print(f"A: {response.content[:200]}")

# Comparison
print("\n--- Strategy Comparison ---")
buf = buffer_memory(SAMPLE_CONVERSATION)
win = window_memory(SAMPLE_CONVERSATION, 3)
summ = summarized

print(f"{'Strategy':<15} {'Messages':<10} {'Characters':<12} {'Best For'}")
print("-" * 70)
print(f"{'Buffer':<15} {len(buf):<10} {sum(len(m.content) for m in buf):<12} {'Short conversations'}")
print(f"{'Window(3)':<15} {len(win):<10} {sum(len(m.content) for m in win):<12} {'Task-focused chats'}")
print(f"{'Summary':<15} {len(summ):<10} {sum(len(m.content) for m in summ):<12} {'Long conversations'}")

# TODO 1: Window size experiment
print("\n--- TODO 1: Window Size Experiment ---")
win1 = window_memory(SAMPLE_CONVERSATION, window_size=1)
follow_up = win1 + [HumanMessage(content="How many annual leave days do I get?")]
response = llm.invoke(follow_up)
print(f"Window=1 (annual leave question): {response.content[:150]}")
print(f"  → Window=1 only has the last exchange, so it may not remember annual leave details")

win5 = window_memory(SAMPLE_CONVERSATION, window_size=5)
follow_up = win5 + [HumanMessage(content="How many annual leave days do I get?")]
response = llm.invoke(follow_up)
print(f"Window=5 (annual leave question): {response.content[:150]}")
print(f"  → Window=5 keeps more history, so it likely remembers annual leave")

# TODO 2: Summary memory v2 with 6 recent messages
print("\n--- TODO 2: Summary Memory v2 ---")

def summary_memory_v2(messages, llm):
    """Keep last 6 recent messages, summarize the rest."""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    if len(non_system) <= 6:
        return messages
    old_messages = non_system[:-6]
    recent_messages = non_system[-6:]
    conversation_text = "\n".join(
        f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
        for m in old_messages
    )
    summary = llm.invoke([HumanMessage(
        content=f"Summarize in 2-3 sentences:\n\n{conversation_text}"
    )]).content
    return system_msgs + [
        SystemMessage(content=f"Previous conversation summary: {summary}"),
    ] + recent_messages

summ_v2 = summary_memory_v2(SAMPLE_CONVERSATION, llm)
v2_chars = sum(len(m.content) for m in summ_v2)
print(f"Summary v1 (keep 4): {len(summarized)} messages, {summary_chars} chars")
print(f"Summary v2 (keep 6): {len(summ_v2)} messages, {v2_chars} chars")
print(f"v2 keeps more recent context but summarizes less")

print("\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- Buffer: simple, complete — good for short conversations")
print("- Window: fixed cost, loses old context — good for task chats")
print("- Summary: balanced, adds LLM call — good for long conversations")
print("- Choose based on: conversation length, context needs, token budget")
