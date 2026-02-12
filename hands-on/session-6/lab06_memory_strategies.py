"""
Lab 06: Memory Strategies
===========================
Goal: Learn different strategies for managing conversation memory
      when history gets too long.

What you'll learn:
- Buffer memory: keep everything (simple but grows)
- Window memory: keep only the last N exchanges
- Summary memory: compress old messages with an LLM
- How to choose the right strategy for your use case
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

print("=" * 50)
print("  Memory Strategies")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile")

# ============================================================
# A sample long conversation for testing
# ============================================================
# Imagine a user has been chatting with the HR assistant for a while.

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

# ============================================================
# Strategy 1: Buffer Memory (keep everything)
# ============================================================

print("\n--- Strategy 1: Buffer Memory ---")

def buffer_memory(messages):
    """Keep all messages — simplest approach but grows without limit."""
    return list(messages)

buffered = buffer_memory(SAMPLE_CONVERSATION)
print(f"Messages kept: {len(buffered)}")
print(f"Characters:    {sum(len(m.content) for m in buffered)}")
print("Pros: Complete context preserved")
print("Cons: Token cost grows linearly with conversation length")

# ============================================================
# Strategy 2: Window Memory (keep last N exchanges)
# ============================================================

print("\n--- Strategy 2: Window Memory ---")

def window_memory(messages, window_size=3):
    """Keep the system message and the last N human-AI exchange pairs."""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]
    # Each exchange = 2 messages (human + ai), keep last N exchanges
    keep = non_system[-(window_size * 2):]
    return system_msgs + keep

for window in [2, 3, 5]:
    windowed = window_memory(SAMPLE_CONVERSATION, window)
    chars = sum(len(m.content) for m in windowed)
    print(f"  Window={window}: {len(windowed)} messages, {chars} chars")

# Test that window memory still works
print("\nTesting window=2 with follow-up question:")
windowed = window_memory(SAMPLE_CONVERSATION, window_size=2)
follow_up = windowed + [HumanMessage(content="Remind me, how much is the internet reimbursement?")]
response = llm.invoke(follow_up)
print(f"  Q: Remind me, how much is the internet reimbursement?")
print(f"  A: {response.content[:150]}")

# ============================================================
# Strategy 3: Summary Memory (compress with LLM)
# ============================================================

print("\n--- Strategy 3: Summary Memory ---")

def summary_memory(messages, llm):
    """Use the LLM to summarize older messages, keeping recent ones intact."""
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    non_system = [m for m in messages if not isinstance(m, SystemMessage)]

    if len(non_system) <= 4:
        return messages  # Too short to bother summarizing

    # Split: older messages to summarize, recent ones to keep verbatim
    old_messages = non_system[:-4]
    recent_messages = non_system[-4:]

    # Ask the LLM to summarize the older conversation
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

# Show the generated summary
for m in summarized:
    if isinstance(m, SystemMessage) and "summary" in m.content.lower():
        print(f"\nGenerated summary: {m.content[:200]}")

# Test it
follow_up = summarized + [HumanMessage(content="Based on what we discussed, can I carry forward my sick leave?")]
response = llm.invoke(follow_up)
print(f"\nQ: Can I carry forward my sick leave?")
print(f"A: {response.content[:200]}")

# ============================================================
# Compare all strategies
# ============================================================

print("\n--- Strategy Comparison ---")
buf = buffer_memory(SAMPLE_CONVERSATION)
win = window_memory(SAMPLE_CONVERSATION, 3)
summ = summarized

print(f"{'Strategy':<15} {'Messages':<10} {'Characters':<12} {'Best For'}")
print("-" * 70)
print(f"{'Buffer':<15} {len(buf):<10} {sum(len(m.content) for m in buf):<12} {'Short conversations'}")
print(f"{'Window(3)':<15} {len(win):<10} {sum(len(m.content) for m in win):<12} {'Task-focused chats'}")
print(f"{'Summary':<15} {len(summ):<10} {sum(len(m.content) for m in summ):<12} {'Long conversations'}")

# ============================================================
# TODO 1: Window size experiment
# ============================================================
# Try window_memory with window_size=1 and ask a follow-up
# question about annual leave (which was discussed early on).
# Does the LLM still remember? Then try window_size=5.
# What's the trade-off?

# win1 = window_memory(SAMPLE_CONVERSATION, window_size=1)
# follow_up = win1 + [HumanMessage(content="How many annual leave days do I get?")]
# response = llm.invoke(follow_up)
# print(f"\nWindow=1: {response.content[:150]}")
#
# win5 = window_memory(SAMPLE_CONVERSATION, window_size=5)
# follow_up = win5 + [HumanMessage(content="How many annual leave days do I get?")]
# response = llm.invoke(follow_up)
# print(f"Window=5: {response.content[:150]}")

# ============================================================
# TODO 2: Adjust summary memory
# ============================================================
# Modify the summary_memory function to keep the last 6 messages
# (instead of 4) and summarize the rest. Does the response quality
# improve? Print the character counts to compare.

# def summary_memory_v2(messages, llm):
#     """Keep last 6 recent messages, summarize the rest."""
#     system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
#     non_system = [m for m in messages if not isinstance(m, SystemMessage)]
#     if len(non_system) <= 6:
#         return messages
#     old_messages = non_system[:-6]
#     recent_messages = non_system[-6:]
#     conversation_text = "\n".join(
#         f"{'User' if isinstance(m, HumanMessage) else 'Assistant'}: {m.content}"
#         for m in old_messages
#     )
#     summary = llm.invoke([HumanMessage(
#         content=f"Summarize in 2-3 sentences:\n\n{conversation_text}"
#     )]).content
#     return system_msgs + [
#         SystemMessage(content=f"Previous conversation summary: {summary}"),
#     ] + recent_messages
#
# summ_v2 = summary_memory_v2(SAMPLE_CONVERSATION, llm)
# print(f"\nSummary v2: {len(summ_v2)} messages, {sum(len(m.content) for m in summ_v2)} chars")

print("\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- Buffer: simple, complete — good for short conversations")
print("- Window: fixed cost, loses old context — good for task chats")
print("- Summary: balanced, adds LLM call — good for long conversations")
print("- Choose based on: conversation length, context needs, token budget")
