"""
Lab 04: From LLM to Agent — See the Difference
=================================================
Goal: See the same task handled by a plain LLM vs an "agent" with tools.

What you'll learn:
- A plain LLM can only guess at answers requiring live data
- An "agent" (LLM + tools) can fetch real data and give accurate answers
- Tools bridge the gap between "knowing" and "doing"
"""

from datetime import datetime
import math
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Scenario 1: "What time is it?"
# ============================================================

print("=" * 50)
print('Scenario 1: "What time is it?"')
print("=" * 50)

# Plain LLM — can only guess
print("--- Plain LLM ---")
response = llm.invoke("What is the current date and time?")
print(f"LLM says: {response.content}\n")

# Agent approach — uses a tool!
print("--- Agent (LLM + Clock Tool) ---")

def clock_tool():
    """Returns the current date and time."""
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")

current_time = clock_tool()
# Feed the tool result to the LLM
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant. Use the provided data to answer."),
    HumanMessage(content=f"The current time is: {current_time}\n\nWhat is the current date and time?"),
])
print(f"Agent says: {response.content}")
print(f"(Used clock tool → got: {current_time})\n")

# ============================================================
# Scenario 2: "What is 17 x 28 + 55?"
# ============================================================

print("=" * 50)
print('Scenario 2: "What is 17 x 28 + 55?"')
print("=" * 50)

# Plain LLM — might get it wrong
print("--- Plain LLM ---")
response = llm.invoke("What is 17 x 28 + 55? Reply with just the number.")
print(f"LLM says: {response.content}")
print(f"Correct:  {17 * 28 + 55}\n")

# Agent approach — uses a calculator!
print("--- Agent (LLM + Calculator Tool) ---")

def calculator_tool(expression: str) -> str:
    """Safely evaluate a math expression."""
    try:
        return str(eval(expression, {"__builtins__": {}, "math": math}))
    except Exception as e:
        return f"Error: {e}"

calc_result = calculator_tool("17 * 28 + 55")
response = llm.invoke([
    SystemMessage(content="You are a helpful assistant. Use the calculation result to answer."),
    HumanMessage(content=f"The calculation result for '17 * 28 + 55' is: {calc_result}\n\nWhat is 17 x 28 + 55?"),
])
print(f"Agent says: {response.content}")
print(f"(Used calculator tool → got: {calc_result})\n")

# ============================================================
# Scenario 3: "Tell me about the weather in Mumbai"
# ============================================================

print("=" * 50)
print('Scenario 3: "Weather in Mumbai"')
print("=" * 50)

# Plain LLM — makes up something or says it can't
print("--- Plain LLM ---")
response = llm.invoke("What is the weather in Mumbai right now? Give specific temperature.")
print(f"LLM says: {response.content}\n")

# Agent approach — uses a weather tool!
print("--- Agent (LLM + Weather Tool) ---")

def weather_tool(city: str) -> str:
    """Simulated weather API (in real life, this calls a weather service)."""
    weather_data = {
        "Mumbai": "32°C, Partly Cloudy, Humidity: 78%",
        "Delhi": "28°C, Sunny, Humidity: 45%",
        "Bangalore": "24°C, Light Rain, Humidity: 82%",
    }
    return weather_data.get(city, "Data unavailable")

weather = weather_tool("Mumbai")
response = llm.invoke([
    SystemMessage(content="You are a weather assistant. Report the weather data provided."),
    HumanMessage(content=f"Current weather data for Mumbai: {weather}\n\nWhat is the weather in Mumbai?"),
])
print(f"Agent says: {response.content}")
print(f"(Used weather tool → got: {weather})\n")

# ============================================================
# Scenario 4: The full picture — side by side
# ============================================================

print("=" * 50)
print("Side-by-Side Comparison")
print("=" * 50)

question = "What is the square root of today's date (day number)?"

# Plain LLM
print(f"Question: {question}\n")
print("--- Plain LLM ---")
response = llm.invoke(question)
print(f"  {response.content}\n")

# Agent
print("--- Agent ---")
day = datetime.now().day
sqrt_result = calculator_tool(f"math.sqrt({day})")
response = llm.invoke([
    SystemMessage(content="Use the provided data to answer clearly."),
    HumanMessage(content=f"Today's date is day {day}. The square root of {day} is {sqrt_result}.\n\n{question}"),
])
print(f"  {response.content}")
print(f"  (Used clock tool → day {day}, then calculator → {sqrt_result})")

# ============================================================
# TODO 1: Build your own comparison
# ============================================================
# Pick a question that needs external data, like:
#   - "How far is it from Mumbai to Delhi?" (needs a distance tool)
#   - "Convert 1000 INR to USD" (needs a currency tool)
#
# Step 1: Ask the plain LLM
# Step 2: Create a tool function that returns the data
# Step 3: Feed the tool result to the LLM
# Compare the answers!

# TODO: Implement your own LLM vs Agent comparison

# ============================================================
# TODO 2: Multi-tool scenario
# ============================================================
# "What is the temperature in Bangalore in Fahrenheit?"
# This needs TWO tools:
#   1. weather_tool("Bangalore") → gets °C
#   2. calculator_tool() → converts to °F
#
# Try building this two-step agent!

# TODO: Chain two tools together

print("\n" + "=" * 50)
print("Lab 04 complete!")
print()
print("Key takeaways:")
print("- Plain LLM: smart but blind (no access to live data)")
print("- Agent (LLM + Tools): smart AND connected to the world")
print("- Tools give the LLM real information to work with")
print("- The LLM's job is to REASON; tools provide the DATA")
print("- This is the foundation of all agentic AI!")
