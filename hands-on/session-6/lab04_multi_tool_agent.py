"""
Lab 04: Multi-Tool Agent
==========================
Goal: Build an agent that orchestrates multiple tools to answer
      complex questions about UniGPS.

What you'll learn:
- How agents choose between multiple tools
- How agents chain multiple tool calls for complex questions
- Best practices for tool design in multi-tool systems
- How to observe agent decision-making via message traces
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

print("=" * 50)
print("  Multi-Tool Agent")
print("=" * 50)

# ============================================================
# Step 1: Create a toolkit for UniGPS
# ============================================================
# Each tool covers a different domain. The agent will choose
# the right tool based on the user's question.

@tool
def check_leave_balance(employee_name: str) -> str:
    """Check the leave balance for a UniGPS employee. Returns annual, sick, and casual leave remaining."""
    employees = {
        "Priya Sharma": {"annual": 18, "sick": 10, "casual": 3},
        "Rahul Patel": {"annual": 12, "sick": 8, "casual": 1},
        "Anita Desai": {"annual": 24, "sick": 12, "casual": 5},
        "Vikram Singh": {"annual": 6, "sick": 12, "casual": 4},
    }
    emp = employees.get(employee_name)
    if emp:
        return (f"{employee_name}: Annual={emp['annual']} days, "
                f"Sick={emp['sick']} days, Casual={emp['casual']} days remaining")
    return f"Employee '{employee_name}' not found. Known: {', '.join(employees.keys())}"

@tool
def get_office_info(city: str) -> str:
    """Get UniGPS office details including address, team size, and facilities for a city."""
    offices = {
        "bangalore": "WeWork Embassy Tech Village, 5th Floor. 200+ employees. All departments. Cafeteria, Gym.",
        "mumbai": "Worli Business District, Tower A, 12th Floor. 50 employees. Sales & marketing. Sea-facing rooms.",
        "hyderabad": "HITEC City, Cyber Gateway, 8th Floor. 80 employees. Engineering hub. 24/7 access.",
        "pune": "Hinjewadi Phase 2, Building C, 4th Floor. 40 employees. QA, DevOps & SRE.",
    }
    return offices.get(city.lower(), f"No UniGPS office in {city}. Offices: Bangalore, Mumbai, Hyderabad, Pune.")

@tool
def calculate_expense(expense_type: str, amount: float) -> str:
    """Check if a UniGPS expense is within policy limits. Types: meal_domestic, meal_international, team_dinner, monitor, mobile, internet."""
    limits = {
        "meal_domestic": 500,
        "meal_international": 3000,
        "team_dinner": 1000,
        "monitor": 15000,
        "mobile": 1000,
        "internet": 1500,
    }
    expense_key = expense_type.lower().replace(" ", "_")
    limit = limits.get(expense_key)
    if limit:
        status = "WITHIN LIMIT" if amount <= limit else "EXCEEDS LIMIT"
        return f"{expense_type}: Rs {amount:,.0f} — {status} (policy limit: Rs {limit:,.0f})"
    return f"Unknown expense type '{expense_type}'. Available: {', '.join(limits.keys())}"

@tool
def get_tech_stack(category: str) -> str:
    """Get UniGPS recommended technology for a category: backend, frontend, database, cloud, or monitoring."""
    stack = {
        "backend": "Python (FastAPI) for new services, Java (Spring Boot) for existing. RESTful APIs mandatory.",
        "frontend": "React + TypeScript for new projects. Angular maintained for Dashboard & Admin portal.",
        "database": "PostgreSQL (primary relational), MongoDB (document store), Redis (caching & sessions).",
        "cloud": "AWS (EKS/Kubernetes). Docker + Terraform. CI/CD via GitHub Actions.",
        "monitoring": "LangFuse (LLM tracing & metrics), PagerDuty (alerts).",
    }
    return stack.get(category.lower(), f"Unknown category '{category}'. Try: backend, frontend, database, cloud, monitoring.")

print("Tools created: check_leave_balance, get_office_info, calculate_expense, get_tech_stack")

# ============================================================
# Step 2: Build the multi-tool agent
# ============================================================

llm = ChatGroq(model="llama-3.3-70b-versatile")
agent = create_react_agent(llm, [check_leave_balance, get_office_info, calculate_expense, get_tech_stack])
print("Multi-tool agent ready!\n")

# ============================================================
# Step 3: Test with different questions
# ============================================================
# Each question targets a different tool. Watch which tool the agent picks.

test_questions = [
    "How many leave days does Priya Sharma have left?",
    "Where is the Hyderabad office and how many people work there?",
    "Is a Rs 800 team dinner within policy?",
    "What database should I use for a new microservice?",
    "What's the capital of France?",  # out-of-scope
]

print("--- Single-Tool Questions ---")
for q in test_questions:
    response = agent.invoke({"messages": [("user", q)]})
    final = response["messages"][-1].content
    tool_count = sum(1 for m in response["messages"] if m.type == "tool")
    print(f"\nQ: {q}")
    print(f"A: {final[:200]}")
    print(f"   (Tool calls: {tool_count})")

# ============================================================
# Step 4: Complex question requiring multiple tools
# ============================================================
# Some questions need information from multiple tools.
# The agent will chain multiple tool calls automatically.

print("\n--- Complex Multi-Tool Question ---")
complex_q = ("I'm Rahul Patel and I want to work from the Pune office next week. "
             "How many leave days do I have, and what's the Pune office like?")
print(f"Q: {complex_q}")

response = agent.invoke({"messages": [("user", complex_q)]})

print("\nMessage trace:")
for msg in response["messages"]:
    if msg.type == "human":
        print(f"  HUMAN: {msg.content[:80]}...")
    elif msg.type == "ai" and hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            print(f"  AI → Tool: {tc['name']}({tc['args']})")
    elif msg.type == "tool":
        print(f"  TOOL: {msg.content[:80]}...")
    elif msg.type == "ai":
        print(f"  AI: {msg.content[:200]}")

# ============================================================
# TODO 1: Add a WFH policy tool
# ============================================================
# Create a tool called `get_wfh_policy` that returns WFH eligibility
# rules: 6-month probation required, 3 days/week max, Friday mandatory
# in-office, core hours 10 AM - 4 PM IST.
# Rebuild the agent with all 5 tools and test with:
# "Can a new employee work from home?"

# @tool
# def get_wfh_policy() -> str:
#     """Get UniGPS Work From Home policy..."""
#     ...
#
# agent_v2 = create_react_agent(
#     llm, [check_leave_balance, get_office_info, calculate_expense, get_tech_stack, get_wfh_policy]
# )
# response = agent_v2.invoke({"messages": [("user", "Can a new employee work from home?")]})
# print(f"\nAnswer: {response['messages'][-1].content}")

# ============================================================
# TODO 2: Triple-tool question
# ============================================================
# Ask the agent a question that requires 3+ tool calls, like:
# "I'm Anita Desai. I need my leave balance, the Mumbai office
# address, and what frontend framework to use for a new project."
# Print the full message trace to count how many tools were called.

# response = agent.invoke({"messages": [("user", "YOUR QUESTION")]})
# tool_count = sum(1 for m in response["messages"] if m.type == "tool")
# print(f"\nTools called: {tool_count}")
# print(f"Answer: {response['messages'][-1].content}")

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- Agents automatically choose the right tool for each question")
print("- Complex questions may trigger multiple sequential tool calls")
print("- Out-of-scope questions get answered without any tools")
print("- Tool descriptions are the agent's 'menu' — make them clear!")
print("- The message trace reveals the agent's decision process")
