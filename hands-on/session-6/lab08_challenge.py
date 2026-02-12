"""
Lab 08: Challenge — Build a UniGPS Employee Support Agent
==========================================================
Goal: Combine everything from Session 5 into a complete AI-powered
      employee support agent with tools and memory.

Your mission: Build an agent that can answer questions about UniGPS
policies, remember conversation context, and handle multiple users.

This exercise has LESS pre-written code — use what you learned in Labs 01-07!
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

print("=" * 50)
print("  UniGPS Employee Support Agent — Challenge Lab")
print("=" * 50)

# ============================================================
# Company knowledge base (DO NOT modify)
# ============================================================

LEAVE_DATA = {
    "annual": {"days": 24, "notice": "3 working days", "carry_forward": False,
               "notes": "Prorated for <6 months tenure"},
    "sick": {"days": 12, "notice": "Same day by 10 AM", "carry_forward": True,
             "notes": "Medical cert after 2 consecutive days. Max carry-forward: 30 days"},
    "maternity": {"days": "26 weeks", "notice": "30 days", "carry_forward": False,
                  "notes": "After 80 days of employment. Can start 8 weeks before delivery"},
    "paternity": {"days": "2 weeks", "notice": "15 days", "carry_forward": False,
                  "notes": "Must take within 6 months of child's birth"},
}

OFFICE_DATA = {
    "bangalore": {"address": "WeWork Embassy Tech Village, Outer Ring Road, 5th Floor",
                  "employees": "200+", "teams": "All departments (HQ)",
                  "facilities": "Cafeteria (3rd floor), Gym, Basement parking"},
    "mumbai": {"address": "Worli Business District, Tower A, 12th Floor",
               "employees": "50", "teams": "Sales, Client Success, Marketing",
               "facilities": "Sea-facing meeting rooms for client presentations"},
    "hyderabad": {"address": "HITEC City, Cyber Gateway, 8th Floor",
                  "employees": "80", "teams": "Backend Engineering, Data Engineering",
                  "facilities": "24/7 access for oncall engineers"},
    "pune": {"address": "Hinjewadi Phase 2, Building C, 4th Floor",
             "employees": "40", "teams": "QA, DevOps, SRE",
             "facilities": "Performance testing lab"},
}

TECH_STACK = {
    "backend": "Python (FastAPI) for new services. Java (Spring Boot) for existing. RESTful APIs mandatory.",
    "frontend": "React + TypeScript (new projects). Angular (existing: Dashboard, Admin portal).",
    "database": "PostgreSQL (primary relational). MongoDB (document storage). Redis (caching + sessions).",
    "cloud": "AWS (EKS/Kubernetes). Docker for containers. Terraform for IaC. GitHub Actions for CI/CD.",
    "monitoring": "LangFuse (LLM tracing & metrics). PagerDuty (alerts).",
}

EXPENSE_LIMITS = {
    "meal_domestic": "Rs 500/day",
    "meal_international": "Rs 3,000/day",
    "team_dinner": "Rs 1,000/person",
    "monitor": "Rs 15,000 (through IT)",
    "mobile": "Rs 1,000/month",
    "internet": "Rs 1,500/month (WFH)",
    "ergonomic_chair": "Rs 10,000 (one-time)",
    "laptop": "Provided by company, replaced every 3 years",
}

# ============================================================
# PART A: Create the tools
# ============================================================
# Build at least 4 tools using the data above. Each tool should:
#   - Have a @tool decorator
#   - Have a descriptive docstring
#   - Use proper type hints
#   - Return formatted string responses
#
# Hints:
#   - leave_policy_lookup(leave_type: str) → look up LEAVE_DATA
#   - office_directory(city: str) → look up OFFICE_DATA
#   - tech_recommendation(category: str) → look up TECH_STACK
#   - expense_checker(expense_type: str) → look up EXPENSE_LIMITS

# TODO: Create your tools here

# @tool
# def leave_policy_lookup(leave_type: str) -> str:
#     """Look up UniGPS leave policy for a specific type (annual, sick, maternity, paternity)."""
#     policy = LEAVE_DATA.get(leave_type.lower())
#     if policy:
#         return (f"{leave_type.title()} Leave: {policy['days']} days. "
#                 f"Notice: {policy['notice']}. "
#                 f"Carry-forward: {'Yes' if policy['carry_forward'] else 'No'}. "
#                 f"Notes: {policy['notes']}")
#     return f"Unknown type: '{leave_type}'. Available: {', '.join(LEAVE_DATA.keys())}"
#
# @tool
# def office_directory(city: str) -> str:
#     """Get UniGPS office details — address, team size, departments, and facilities."""
#     office = OFFICE_DATA.get(city.lower())
#     if office:
#         return (f"UniGPS {city.title()}: {office['address']}. "
#                 f"{office['employees']} employees. Teams: {office['teams']}. "
#                 f"Facilities: {office['facilities']}")
#     return f"No office in '{city}'. Available: {', '.join(OFFICE_DATA.keys())}"
#
# @tool
# def tech_recommendation(category: str) -> str:
#     """Get UniGPS recommended technology stack for a category (backend, frontend, database, cloud, monitoring)."""
#     rec = TECH_STACK.get(category.lower())
#     if rec:
#         return f"UniGPS {category.title()} Stack: {rec}"
#     return f"Unknown category: '{category}'. Try: {', '.join(TECH_STACK.keys())}"
#
# @tool
# def expense_checker(expense_type: str) -> str:
#     """Check UniGPS expense policy limits for a specific type (meal_domestic, monitor, internet, etc.)."""
#     limit = EXPENSE_LIMITS.get(expense_type.lower().replace(" ", "_"))
#     if limit:
#         return f"{expense_type.replace('_', ' ').title()}: {limit}"
#     return f"Unknown type. Available: {', '.join(EXPENSE_LIMITS.keys())}"


# ============================================================
# PART B: Build the agent with memory
# ============================================================
# Create a ReAct agent with:
#   1. All your tools from Part A
#   2. MemorySaver for session persistence
#   3. A system prompt via state_modifier

# TODO: Build the agent
# llm = ChatGroq(model="llama-3.3-70b-versatile")
# memory = MemorySaver()
# agent = create_react_agent(
#     llm,
#     [leave_policy_lookup, office_directory, tech_recommendation, expense_checker],
#     checkpointer=memory,
#     state_modifier="You are UniBot, UniGPS's AI employee support assistant. "
#                    "Be friendly, concise, and always cite the policy source. "
#                    "If you don't know something, say so honestly.",
# )


# ============================================================
# PART C: Test with single-topic questions
# ============================================================
# Test your agent with one question per tool.

# TODO: Uncomment and test
# config = {"configurable": {"thread_id": "test-session"}}
#
# test_questions = [
#     "How many sick leave days do I get per year?",
#     "Where is the Pune office located?",
#     "What language should I use for a new backend service?",
#     "What's the limit for mobile reimbursement?",
# ]
#
# print("\n--- Single-Topic Tests ---")
# for q in test_questions:
#     response = agent.invoke({"messages": [("user", q)]}, config)
#     print(f"\nQ: {q}")
#     print(f"A: {response['messages'][-1].content[:200]}")


# ============================================================
# PART D: Test memory across turns
# ============================================================
# Have a multi-turn conversation using the same thread_id.

# TODO: Uncomment and test
# print("\n--- Multi-Turn Memory Test ---")
# config_mem = {"configurable": {"thread_id": "memory-test"}}
#
# turns = [
#     "Hi! I'm Vikram from the engineering team.",
#     "What database should I use for a new project?",
#     "What's my name?",
#     "I also need to check — how many annual leave days do I get?",
# ]
#
# for i, q in enumerate(turns, 1):
#     r = agent.invoke({"messages": [("user", q)]}, config_mem)
#     print(f"Turn {i}: {q}")
#     print(f"  → {r['messages'][-1].content[:200]}")
#     print()


# ============================================================
# PART E: Multi-user sessions
# ============================================================
# Verify that different thread_ids create isolated sessions.

# TODO: Uncomment and test
# print("\n--- Multi-User Sessions ---")
# config_user1 = {"configurable": {"thread_id": "priya-001"}}
# config_user2 = {"configurable": {"thread_id": "rahul-002"}}
#
# agent.invoke({"messages": [("user", "I'm Priya. Tell me about maternity leave.")]}, config_user1)
# agent.invoke({"messages": [("user", "I'm Rahul. What's the Hyderabad office like?")]}, config_user2)
#
# r1 = agent.invoke({"messages": [("user", "What did I ask about?")]}, config_user1)
# r2 = agent.invoke({"messages": [("user", "What did I ask about?")]}, config_user2)
# print(f"Priya's session: {r1['messages'][-1].content[:150]}")
# print(f"Rahul's session: {r2['messages'][-1].content[:150]}")


# ============================================================
# PART F (Bonus): Interactive mode with user switching
# ============================================================

# TODO: Uncomment for interactive mode
# print("\n" + "=" * 50)
# print("UniBot Interactive — Commands:")
# print("  /switch <name>  — switch user session")
# print("  /history        — show current session messages")
# print("  /quit           — exit")
# print("=" * 50)
#
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
#     if user_input == "/history":
#         config = {"configurable": {"thread_id": f"{current_user}-session"}}
#         state = agent.get_state(config)
#         for msg in state.values.get("messages", []):
#             print(f"  [{msg.type}] {msg.content[:80]}")
#         continue
#
#     config = {"configurable": {"thread_id": f"{current_user}-session"}}
#     response = agent.invoke({"messages": [("user", user_input)]}, config)
#     print(f"[UniBot] {response['messages'][-1].content}")

print("\n" + "=" * 50)
print("Challenge tips:")
print("- Start with Part A (tools) — test each with .invoke() first")
print("- Part B: build the agent, verify it starts up")
print("- Part C tests each tool through the agent")
print("- Part D verifies memory works across turns")
print("- Part E tests multi-user session isolation")
print("- Part F is bonus — interactive loop with user switching")
print("- Check solutions/lab08_challenge.py if you get stuck")
