"""
Lab 02: Your First ReAct Agent
================================
Goal: Build a ReAct agent that can think, decide which tool to use,
      observe the result, and formulate an answer.

What you'll learn:
- How create_react_agent() builds an agent from an LLM + tools
- The ReAct loop: Think → Act → Observe → Decide
- How to examine the full message trace
- What happens when no tool is needed
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

print("=" * 50)
print("  Your First ReAct Agent")
print("=" * 50)

# ============================================================
# Step 1: Create tools for the agent
# ============================================================
# These are mock tools with hardcoded data — perfect for learning.
# In production, these would call real APIs or databases.

@tool
def get_weather(city: str) -> str:
    """Get the current weather for an Indian city. Returns temperature and conditions."""
    weather = {
        "bangalore": "28°C, Partly Cloudy, Humidity 65%",
        "mumbai": "32°C, Humid, Humidity 80%",
        "hyderabad": "34°C, Sunny, Humidity 45%",
        "pune": "30°C, Clear Sky, Humidity 50%",
        "delhi": "38°C, Hot and Dry, Humidity 30%",
    }
    return weather.get(city.lower(), f"No weather data available for {city}")

@tool
def get_population(city: str) -> str:
    """Get the approximate population of an Indian city."""
    population = {
        "bangalore": "13.2 million (2024 est.)",
        "mumbai": "21.7 million (2024 est.)",
        "hyderabad": "10.5 million (2024 est.)",
        "pune": "7.4 million (2024 est.)",
        "delhi": "32.9 million (2024 est.)",
    }
    return population.get(city.lower(), f"Population data not available for {city}")

print("Tools created: get_weather, get_population")

# ============================================================
# Step 2: Build the ReAct agent
# ============================================================
# create_react_agent() takes an LLM and a list of tools.
# It returns a compiled graph that can think, act, and observe.

llm = ChatGroq(model="llama-3.3-70b-versatile")
agent = create_react_agent(llm, [get_weather, get_population])
print("ReAct agent ready!\n")

# ============================================================
# Step 3: Ask a question that requires a tool
# ============================================================
# The agent will: Think → Call get_weather → Observe result → Answer

print("--- Question 1: Needs a tool ---")
response = agent.invoke({"messages": [("user", "What's the weather in Bangalore?")]})

# Examine the full message trace
print("Full message trace:")
for msg in response["messages"]:
    prefix = msg.type.upper()
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"  {prefix}: [Calling tool: {msg.tool_calls[0]['name']}({msg.tool_calls[0]['args']})]")
    elif msg.type == "tool":
        print(f"  {prefix}: {msg.content}")
    else:
        print(f"  {prefix}: {msg.content[:200]}")

# ============================================================
# Step 4: Get just the final answer
# ============================================================
# The last message is always the agent's final response.

final_answer = response["messages"][-1].content
print(f"\nFinal answer: {final_answer}")

# ============================================================
# Step 5: Question that doesn't need a tool
# ============================================================
# If the agent can answer directly, it skips tool calls.

print("\n--- Question 2: No tool needed ---")
response2 = agent.invoke({"messages": [("user", "What is 2 + 2?")]})
print(f"Answer: {response2['messages'][-1].content}")
print(f"Messages in trace: {len(response2['messages'])}")

# ============================================================
# Step 6: Question using the other tool
# ============================================================

print("\n--- Question 3: Different tool ---")
response3 = agent.invoke({"messages": [("user", "What's the population of Mumbai?")]})
print(f"Answer: {response3['messages'][-1].content}")

# ============================================================
# Step 7: Out-of-scope question
# ============================================================
# The tool only has Indian cities. What happens with others?

print("\n--- Question 4: Out of scope ---")
response4 = agent.invoke({"messages": [("user", "What's the weather in Paris?")]})
print(f"Answer: {response4['messages'][-1].content}")

# ============================================================
# TODO 1: Multi-tool question
# ============================================================
# Ask the agent a question that could use BOTH tools, like:
# "Tell me about Hyderabad — what's the weather and population?"
# Examine the message trace — how many tool calls does it make?

# response = agent.invoke({"messages": [("user", "YOUR QUESTION HERE")]})
# print("\nMessage trace:")
# for msg in response["messages"]:
#     print(f"  {msg.type}: {msg.content[:100]}")

# ============================================================
# TODO 2: Add a new tool
# ============================================================
# Create a tool called `get_famous_food` that returns famous dishes
# for Indian cities, e.g.:
#   bangalore → "Masala Dosa, Bisi Bele Bath, Filter Coffee"
#   mumbai    → "Vada Pav, Pav Bhaji, Bombay Sandwich"
#   hyderabad → "Hyderabadi Biryani, Haleem, Irani Chai"
#
# Then rebuild the agent with all three tools and test:
# "What's the famous food in Pune?"

# @tool
# def get_famous_food(city: str) -> str:
#     ...
#
# agent_v2 = create_react_agent(llm, [get_weather, get_population, get_famous_food])
# response = agent_v2.invoke({"messages": [("user", "What's the famous food in Pune?")]})
# print(f"Answer: {response['messages'][-1].content}")

print("\n" + "=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- create_react_agent(llm, tools) builds a ReAct agent")
print("- The agent decides WHEN and WHICH tool to use")
print("- Message trace shows: Human → AI (tool call) → Tool → AI (answer)")
print("- If no tool is needed, the agent answers directly")
print("- Out-of-scope data is handled gracefully by the tool")
