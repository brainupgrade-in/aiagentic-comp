"""
Lab 04: From LLM to Agent — SOLUTION
"""

from datetime import datetime
import math
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

llm = ChatOllama(model="llama3.2:1b")


# Tools
def clock_tool():
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


def calculator_tool(expression):
    try:
        return str(eval(expression, {"__builtins__": {}, "math": math}))
    except Exception as e:
        return f"Error: {e}"


def weather_tool(city):
    data = {"Mumbai": "32°C, Partly Cloudy, Humidity: 78%",
            "Delhi": "28°C, Sunny, Humidity: 45%",
            "Bangalore": "24°C, Light Rain, Humidity: 82%"}
    return data.get(city, "Data unavailable")


# Scenario 1: Time
print("=" * 50)
print("Scenario 1: What time is it?")
print("=" * 50)
print("--- Plain LLM ---")
print(f"LLM: {llm.invoke('What is the current date and time?').content}\n")
print("--- Agent ---")
t = clock_tool()
r = llm.invoke([
    SystemMessage(content="Use the data provided to answer accurately."),
    HumanMessage(content=f"Current time: {t}\nWhat is the current date and time?"),
])
print(f"Agent: {r.content} (tool: {t})\n")

# Scenario 2: Math
print("=" * 50)
print("Scenario 2: Math")
print("=" * 50)
print("--- Plain LLM ---")
print(f"LLM: {llm.invoke('What is 17 x 28 + 55? Just the number.').content}")
print(f"Correct: {17 * 28 + 55}\n")
print("--- Agent ---")
calc = calculator_tool("17 * 28 + 55")
r = llm.invoke([
    SystemMessage(content="Use the calculation result to answer."),
    HumanMessage(content=f"Calculation: 17 * 28 + 55 = {calc}\nWhat is 17 x 28 + 55?"),
])
print(f"Agent: {r.content} (tool: {calc})\n")

# Scenario 3: Weather
print("=" * 50)
print("Scenario 3: Weather")
print("=" * 50)
print("--- Plain LLM ---")
print(f"LLM: {llm.invoke('Weather in Mumbai now? Specific temperature.').content}\n")
print("--- Agent ---")
w = weather_tool("Mumbai")
r = llm.invoke([
    SystemMessage(content="Report the weather data provided."),
    HumanMessage(content=f"Weather data: {w}\nWhat is the weather in Mumbai?"),
])
print(f"Agent: {r.content} (tool: {w})\n")

# TODO 1: Distance comparison
print("=" * 50)
print("TODO 1: Distance")
print("=" * 50)


def distance_tool(route):
    distances = {"Mumbai-Delhi": "1,400 km", "Mumbai-Bangalore": "980 km", "Delhi-Bangalore": "2,150 km"}
    return distances.get(route, "Unknown route")


print("--- Plain LLM ---")
print(f"LLM: {llm.invoke('How far is Mumbai from Delhi?').content}\n")
print("--- Agent ---")
d = distance_tool("Mumbai-Delhi")
r = llm.invoke([
    SystemMessage(content="Use the data provided."),
    HumanMessage(content=f"Distance data: Mumbai to Delhi = {d}\nHow far is Mumbai from Delhi?"),
])
print(f"Agent: {r.content} (tool: {d})\n")

# TODO 2: Multi-tool — temperature conversion
print("=" * 50)
print("TODO 2: Multi-tool (Weather + Calculator)")
print("=" * 50)

w = weather_tool("Bangalore")
# Extract temperature number (24 from "24°C, Light Rain...")
temp_c = 24
temp_f = calculator_tool(f"{temp_c} * 9 / 5 + 32")

r = llm.invoke([
    SystemMessage(content="Use the data provided to give a complete answer."),
    HumanMessage(content=f"Bangalore weather: {w}\nTemperature conversion: {temp_c}°C = {temp_f}°F\n\nWhat is the temperature in Bangalore in Fahrenheit?"),
])
print(f"Agent: {r.content}")
print(f"(Tool 1: weather → {w})")
print(f"(Tool 2: calculator → {temp_c}°C = {temp_f}°F)")

print("\nLab 04 complete!")
