"""
Lab 06: Challenge — Design Your Own Agent — SOLUTION
"""

from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Part A: Agent Design
# ============================================================
print("=" * 50)
print("  Agent Design Workshop")
print("=" * 50)

scenarios = [
    {"name": "Restaurant Booking Agent",
     "task": "Book a good Italian restaurant for Saturday evening for 4 people in Bangalore"},
    {"name": "Code Review Agent",
     "task": "Review a pull request, check for bugs, suggest improvements, and post comments"},
    {"name": "Personal Finance Agent",
     "task": "Track expenses, alert on overspending, suggest savings"},
]

for s in scenarios:
    print(f"\n--- {s['name']} ---")
    r = llm.invoke([
        SystemMessage(content="""Design an agent. List:
1. TOOLS needed (3-4 specific tools)
2. MEMORY needed (what to remember)
3. PLANNING steps (4-5 steps)
One sentence per point."""),
        HumanMessage(content=f"Design an agent for: {s['task']}"),
    ])
    print(r.content)

# ============================================================
# Part B: Personal Assistant Agent
# ============================================================
print("\n" + "=" * 50)
print("  Personal Assistant Agent")
print("=" * 50)


def check_calendar(date):
    return {"today": "10 AM: Standup, 2 PM: Design review, 5 PM: Gym",
            "tomorrow": "9 AM: Client call, 12 PM: Lunch with Priya, 4 PM: Sprint planning",
            "friday": "11 AM: Demo day, 3 PM: Team outing"}.get(date.lower(), "No events")


def check_tasks(category):
    return {"work": "1. Fix login bug (high)\n2. Review PR #42\n3. Update docs",
            "personal": "1. Buy groceries\n2. Call dentist\n3. Pay electricity bill",
            "urgent": "1. Fix login bug (due today)\n2. Reply to client email"}.get(category.lower(), "None")


def get_time():
    return datetime.now().strftime("%I:%M %p")


def weather_tool(city):
    return {"Bangalore": "24°C, 70% chance of rain",
            "Mumbai": "32°C, Partly cloudy"}.get(city, "Unknown")


memory = [SystemMessage(content="""You are a personal assistant. Helpful, proactive, concise.
User is Raj, a software developer. Use tool results provided.""")]


def ask(user_msg, tool_data=""):
    memory.append(HumanMessage(content=f"[Tools: {tool_data}]\n{user_msg}" if tool_data else user_msg))
    r = llm.invoke(memory)
    memory.append(AIMessage(content=r.content))
    return r.content


# Conversation
print("\n--- Conversation ---\n")

r = ask("Good morning! What's on my plate today?",
        f"Calendar: {check_calendar('today')}\nUrgent: {check_tasks('urgent')}\nTime: {get_time()}")
print(f"You: Good morning! What's on my plate today?")
print(f"Bot: {r}\n")

r = ask("What about tomorrow?", f"Calendar: {check_calendar('tomorrow')}")
print(f"You: What about tomorrow?")
print(f"Bot: {r}\n")

r = ask("What personal tasks do I have?", f"Tasks: {check_tasks('personal')}")
print(f"You: What personal tasks do I have?")
print(f"Bot: {r}\n")

r = ask("When is my first meeting today?")
print(f"You: When is my first meeting today?")
print(f"Bot: {r}\n")

# TODO 1: Weather + Calendar combined
print("--- TODO 1: Umbrella question ---\n")
r = ask("Should I carry an umbrella to my team outing on Friday?",
        f"Weather: {weather_tool('Bangalore')}\nFriday: {check_calendar('friday')}")
print(f"You: Should I carry an umbrella to my team outing Friday?")
print(f"Bot: {r}\n")

print(f"[Memory: {len(memory)} messages]")

# TODO 2: Dream agent design
print("=" * 50)
print("Dream Agent: DevOps Incident Responder")
print("=" * 50)
print("""
Agent name: DevOps Incident Responder
Task: When an alert fires, diagnose the issue and fix it

Tools needed:
  1. monitoring_api — fetch metrics, logs, alerts
  2. ssh_tool — connect to servers, run commands
  3. git_tool — check recent deployments, rollback if needed
  4. slack_notifier — update the team on progress

Memory needed:
  - Recent incidents and their resolutions
  - Known problematic services/deployments
  - Team escalation contacts

Planning steps:
  1. Receive alert → identify affected service
  2. Pull metrics and logs for the service
  3. Check if a recent deployment caused it
  4. If yes → rollback; if no → analyze logs for root cause
  5. Apply fix, verify service is healthy
  6. Notify team with incident summary
""")

print("Lab 06 complete! Congratulations on finishing Session 1!")
