"""
Lab 06: Challenge — Design Your Own Agent
============================================
Goal: Given real-world scenarios, think through what an agent needs
and build a simple working prototype.

This exercise combines everything from Session 1:
- What is an agent?
- LLM capabilities and limitations
- The four building blocks (Brain, Memory, Tools, Planning)
"""

from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# PART A: Agent Design Exercise
# ============================================================
# For each scenario, the LLM will help YOU think through what
# tools, memory, and planning the agent needs.

print("=" * 50)
print("  Agent Design Workshop")
print("=" * 50)

scenarios = [
    {
        "name": "Restaurant Booking Agent",
        "task": "Book a good Italian restaurant for Saturday evening for 4 people in Bangalore",
    },
    {
        "name": "Code Review Agent",
        "task": "Review a pull request, check for bugs, suggest improvements, and post comments",
    },
    {
        "name": "Personal Finance Agent",
        "task": "Track my expenses, alert me if I'm overspending, and suggest ways to save money this month",
    },
]

for scenario in scenarios:
    print(f"\n--- {scenario['name']} ---")
    print(f"Task: {scenario['task']}\n")

    response = llm.invoke([
        SystemMessage(content="""You are an AI architect designing agents. For the given task, list:
1. What TOOLS would this agent need? (list 3-4 specific tools)
2. What MEMORY does it need? (what must it remember?)
3. What PLANNING steps would it follow? (list 4-5 steps)
Keep each point to one sentence."""),
        HumanMessage(content=f"Design an agent for: {scenario['task']}"),
    ])
    print(response.content)

# ============================================================
# PART B: Build a Simple Agent Prototype
# ============================================================
# Let's build a "Personal Assistant" agent with tools and memory.

print("\n" + "=" * 50)
print("  Build: Personal Assistant Agent")
print("=" * 50)

# Define tools for our assistant
def check_calendar(date: str) -> str:
    """Check what's on the calendar."""
    events = {
        "today": "10 AM: Team standup, 2 PM: Design review, 5 PM: Gym",
        "tomorrow": "9 AM: Client call, 12 PM: Lunch with Priya, 4 PM: Sprint planning",
        "friday": "11 AM: Demo day, 3 PM: Team outing",
    }
    return events.get(date.lower(), "No events found")


def check_tasks(category: str) -> str:
    """Check pending tasks."""
    tasks = {
        "work": "1. Fix login bug (high priority)\n2. Review PR #42\n3. Update docs",
        "personal": "1. Buy groceries\n2. Call dentist\n3. Pay electricity bill",
        "urgent": "1. Fix login bug (due today)\n2. Reply to client email",
    }
    return tasks.get(category.lower(), "No tasks found")


def get_time() -> str:
    return datetime.now().strftime("%I:%M %p")


TOOLS = {
    "check_calendar": check_calendar,
    "check_tasks": check_tasks,
    "get_time": get_time,
}

# Memory (conversation history)
memory = [
    SystemMessage(content="""You are a personal assistant. You are helpful, proactive, and concise.
You know the user's name is Raj and he is a software developer.
When answering, use the tool results provided to give accurate information."""),
]


def assistant_respond(user_message: str, tool_data: str = "") -> str:
    """Get a response from the assistant with optional tool data."""
    memory.append(HumanMessage(content=user_message))

    if tool_data:
        # Include tool results in the context
        prompt_msg = f"[Tool results: {tool_data}]\n\nUser says: {user_message}"
        memory[-1] = HumanMessage(content=prompt_msg)

    response = llm.invoke(memory)
    memory.append(AIMessage(content=response.content))
    return response.content


# Simulate a conversation with the assistant
print("\n--- Conversation ---\n")

# Turn 1: Simple greeting (uses Memory — knows user's name)
reply = assistant_respond("Good morning! What's on my plate today?",
                          tool_data=f"Calendar: {check_calendar('today')}\nUrgent tasks: {check_tasks('urgent')}\nTime: {get_time()}")
print(f"You: Good morning! What's on my plate today?")
print(f"Assistant: {reply}\n")

# Turn 2: Follow-up (uses Memory — remembers the context)
reply = assistant_respond("What about tomorrow?",
                          tool_data=f"Calendar: {check_calendar('tomorrow')}")
print(f"You: What about tomorrow?")
print(f"Assistant: {reply}\n")

# Turn 3: Task check (uses Tools)
reply = assistant_respond("What personal tasks do I have pending?",
                          tool_data=f"Personal tasks: {check_tasks('personal')}")
print(f"You: What personal tasks do I have pending?")
print(f"Assistant: {reply}\n")

# Turn 4: Memory test (remembers earlier context)
reply = assistant_respond("When is my first meeting today?")
print(f"You: When is my first meeting today?")
print(f"Assistant: {reply}")
print("(^ Should remember from Turn 1!)\n")

print(f"[Total messages in memory: {len(memory)}]")

# ============================================================
# PART C: Your Turn!
# ============================================================

# TODO 1: Add a new tool and use it
# ============================================================
# Add a "weather_tool" and use it to answer:
# "Should I carry an umbrella to my team outing on Friday?"
# This needs: weather tool + calendar tool (knows Friday has a team outing)

# def weather_tool(city):
#     return "Bangalore: 24°C, 70% chance of rain"
#
# tool_data = f"Weather: {weather_tool('Bangalore')}\nFriday calendar: {check_calendar('friday')}"
# reply = assistant_respond("Should I carry an umbrella to my team outing on Friday?", tool_data=tool_data)
# print(f"You: Should I carry an umbrella to the team outing Friday?")
# print(f"Assistant: {reply}")

# TODO 2: Design your dream agent
# ============================================================
# Think of a real problem you face. Design an agent for it:
# - What task does it do?
# - What tools does it need?
# - What does it need to remember?
# - What steps would it follow?
#
# Write your design as comments here:
# Agent name: ___
# Task: ___
# Tools needed: ___
# Memory needed: ___
# Steps: ___

# TODO 3: Build it!
# ============================================================
# If you have time, try building a simple prototype of your
# dream agent using the pattern above (tools + memory + LLM).

print("\n" + "=" * 50)
print("Lab 06 complete! You've designed and built agents!")
print()
print("Key takeaways:")
print("- Start by identifying: what tools, memory, and planning does the agent need?")
print("- Even a simple agent (LLM + tools + memory) is surprisingly useful")
print("- The LLM is the brain; everything else is infrastructure")
print("- In the next sessions, you'll use LangChain to build this properly!")
print()
print("Congratulations — you've completed Session 1 hands-on labs!")
print("You now understand what agents are, why they exist, and how they work.")
