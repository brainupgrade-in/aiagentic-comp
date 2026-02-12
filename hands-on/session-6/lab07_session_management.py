"""
Lab 07: Session Management with MemorySaver
=============================================
Goal: Use LangGraph's MemorySaver to automatically manage conversation
      memory with support for multiple users and sessions.

What you'll learn:
- How MemorySaver handles memory automatically
- How thread_id isolates conversations for different users
- How to resume previous conversations
- The pattern for multi-user session management
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

print("=" * 50)
print("  Session Management with MemorySaver")
print("=" * 50)

# ============================================================
# Step 1: Create tools and agent with MemorySaver
# ============================================================
# MemorySaver automatically stores conversation history per thread.
# No manual message list management needed!

@tool
def get_leave_policy(leave_type: str) -> str:
    """Get UniGPS leave policy details for a specific type: annual, sick, maternity, or paternity."""
    policies = {
        "annual": "24 days/year. Apply 3 days in advance via HR portal. No carry-forward.",
        "sick": "12 days/year. Notify manager by 10 AM. Medical cert after 2 days. Carry-forward up to 30 days.",
        "maternity": "26 weeks paid. Can start 8 weeks before delivery. Requires 80 days of employment.",
        "paternity": "2 weeks paid. Take within 6 months of birth. Apply 15 days in advance.",
    }
    return policies.get(leave_type.lower(), f"Unknown type: {leave_type}. Available: annual, sick, maternity, paternity")

@tool
def get_expense_limit(expense_type: str) -> str:
    """Get UniGPS expense policy limits. Types: meal_domestic, meal_international, team_dinner, monitor, mobile, internet."""
    limits = {
        "meal_domestic": "Rs 500/day during client visits in India",
        "meal_international": "Rs 3,000/day for international travel",
        "team_dinner": "Rs 1,000/person with manager approval",
        "monitor": "Up to Rs 15,000 — request through IT",
        "mobile": "Rs 1,000/month for client-facing roles",
        "internet": "Rs 1,500/month for WFH employees",
    }
    return limits.get(expense_type.lower(), f"Unknown type: {expense_type}. Available: {', '.join(limits.keys())}")

llm = ChatGroq(model="llama-3.3-70b-versatile")
memory = MemorySaver()
agent = create_react_agent(llm, [get_leave_policy, get_expense_limit], checkpointer=memory)
print("Agent with MemorySaver ready!")

# ============================================================
# Step 2: Conversation with thread_id
# ============================================================
# Each thread_id creates an isolated conversation session.
# MemorySaver automatically tracks the full history.

print("\n--- Step 2: Session for User 'priya' ---")
config_priya = {"configurable": {"thread_id": "priya-session"}}

r1 = agent.invoke({"messages": [("user", "Hi, I'm Priya. How many sick days do I get?")]}, config_priya)
print(f"Turn 1: {r1['messages'][-1].content[:200]}")

r2 = agent.invoke({"messages": [("user", "Can I carry them forward?")]}, config_priya)
print(f"Turn 2: {r2['messages'][-1].content[:200]}")

r3 = agent.invoke({"messages": [("user", "What's my name again?")]}, config_priya)
print(f"Turn 3: {r3['messages'][-1].content[:200]}")
print("→ MemorySaver remembers the full conversation automatically!")

# ============================================================
# Step 3: Different user, different session
# ============================================================
# A different thread_id = a completely separate conversation.

print("\n--- Step 3: Session for User 'rahul' ---")
config_rahul = {"configurable": {"thread_id": "rahul-session"}}

r1 = agent.invoke(
    {"messages": [("user", "I'm Rahul. What's the meal allowance for international travel?")]},
    config_rahul
)
print(f"Turn 1: {r1['messages'][-1].content[:200]}")

r2 = agent.invoke({"messages": [("user", "And for domestic travel?")]}, config_rahul)
print(f"Turn 2: {r2['messages'][-1].content[:200]}")

# ============================================================
# Step 4: Switch back to Priya's session
# ============================================================
# Priya's conversation is preserved — we can pick up where we left off.

print("\n--- Step 4: Resume Priya's Session ---")
r4 = agent.invoke(
    {"messages": [("user", "Going back to sick leave — do I need a doctor's note?")]},
    config_priya
)
print(f"Priya Turn 4: {r4['messages'][-1].content[:200]}")
print("→ Priya's session is intact even after switching to Rahul!")

# ============================================================
# Step 5: Verify session isolation
# ============================================================

print("\n--- Step 5: Session Isolation ---")
rahul_check = agent.invoke({"messages": [("user", "What's my name?")]}, config_rahul)
priya_check = agent.invoke({"messages": [("user", "Summarize everything we discussed.")]}, config_priya)

print(f"Rahul's session: {rahul_check['messages'][-1].content[:150]}")
print(f"Priya's session: {priya_check['messages'][-1].content[:200]}")
print("→ Each thread_id maintains its own completely separate conversation!")

# ============================================================
# TODO 1: Third user session
# ============================================================
# Create a session for "anita" (thread_id: "anita-session").
# Have Anita ask about maternity leave policy, then ask a follow-up
# like "How early can I start the leave?"
# Verify Anita's session doesn't know about Priya or Rahul.

# config_anita = {"configurable": {"thread_id": "anita-session"}}
# r1 = agent.invoke({"messages": [("user", "I'm Anita. Tell me about maternity leave.")]}, config_anita)
# print(f"\nAnita Turn 1: {r1['messages'][-1].content[:200]}")
# r2 = agent.invoke({"messages": [("user", "How early can I start the leave?")]}, config_anita)
# print(f"Anita Turn 2: {r2['messages'][-1].content[:200]}")
# # Isolation check:
# r3 = agent.invoke({"messages": [("user", "Do you know anyone named Priya?")]}, config_anita)
# print(f"Anita isolation: {r3['messages'][-1].content[:150]}")

# ============================================================
# TODO 2: Interactive multi-user loop
# ============================================================
# Build an interactive loop that supports switching between users:

# print("\n--- Interactive Multi-User Chat ---")
# print("Commands: /switch <name> to switch user, /quit to exit")
# current_user = "default"
# while True:
#     user_input = input(f"\n[{current_user}] You: ").strip()
#     if not user_input:
#         continue
#     if user_input == "/quit":
#         break
#     if user_input.startswith("/switch "):
#         current_user = user_input.split(" ", 1)[1]
#         print(f"Switched to session: {current_user}")
#         continue
#     config = {"configurable": {"thread_id": f"{current_user}-session"}}
#     response = agent.invoke({"messages": [("user", user_input)]}, config)
#     print(f"[Bot] {response['messages'][-1].content}")

print("\n" + "=" * 50)
print("Lab 07 complete! Key takeaways:")
print("- MemorySaver automatically persists conversation history")
print("- thread_id isolates sessions — each user gets their own memory")
print("- Sessions can be paused and resumed with the same thread_id")
print("- In production, use SqliteSaver or PostgresSaver for persistence")
print("- This is the foundation for multi-user chatbot applications")
