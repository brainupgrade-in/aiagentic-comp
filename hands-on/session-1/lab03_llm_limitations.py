"""
Lab 03: LLM Limitations — Why We Need Agents
===============================================
Goal: Discover what LLMs CANNOT do — and why agents exist.

What you'll learn:
- LLMs have no memory between messages
- LLMs can't access real-time information
- LLMs struggle with precise math
- LLMs can't take actions (send emails, book tickets, etc.)
- LLMs sometimes "hallucinate" (make up confident-sounding wrong answers)

These limitations are exactly why we need AGENTS!
"""

from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Limitation 1: NO MEMORY
# ============================================================

print("=" * 50)
print("LIMITATION 1: No Memory Between Messages")
print("=" * 50)

r1 = llm.invoke("My name is Raj and I live in Bangalore.")
print(f"Message 1: 'My name is Raj and I live in Bangalore.'")
print(f"AI: {r1.content}\n")

r2 = llm.invoke("What is my name and where do I live?")
print(f"Message 2: 'What is my name and where do I live?'")
print(f"AI: {r2.content}\n")

print(">>> The AI forgot! Each message is completely independent.")
print(">>> An AGENT solves this with MEMORY (Session 2, Component 2).\n")

# ============================================================
# Limitation 2: NO REAL-TIME INFORMATION
# ============================================================

print("=" * 50)
print("LIMITATION 2: No Real-Time Information")
print("=" * 50)

response = llm.invoke("What is the weather in Mumbai right now?")
print(f"Q: What is the weather in Mumbai right now?")
print(f"AI: {response.content}\n")

response = llm.invoke("What is the current price of Bitcoin?")
print(f"Q: What is the current price of Bitcoin?")
print(f"AI: {response.content}\n")

print(">>> The AI doesn't know current data — it only knows its training data.")
print(">>> An AGENT solves this with TOOLS (web search, weather API).\n")

# ============================================================
# Limitation 3: UNRELIABLE MATH
# ============================================================

print("=" * 50)
print("LIMITATION 3: Unreliable Math")
print("=" * 50)

math_problems = [
    ("What is 17 x 28?", 476),
    ("What is 1234 + 5678?", 6912),
    ("What is 15% of 847?", 127.05),
]

for question, correct in math_problems:
    response = llm.invoke(f"{question} Reply with ONLY the number.")
    print(f"Q: {question}")
    print(f"AI says: {response.content}")
    print(f"Correct: {correct}\n")

print(">>> LLMs 'guess' at math — they don't actually calculate.")
print(">>> An AGENT solves this with a CALCULATOR TOOL.\n")

# ============================================================
# Limitation 4: CAN'T TAKE ACTIONS
# ============================================================

print("=" * 50)
print("LIMITATION 4: Can't Take Actions")
print("=" * 50)

response = llm.invoke("Send an email to raj@example.com saying 'Meeting at 3 PM'")
print(f"Q: Send an email to raj@example.com saying 'Meeting at 3 PM'")
print(f"AI: {response.content}\n")

response = llm.invoke("Create a file called report.txt with today's date in it")
print(f"Q: Create a file called report.txt with today's date")
print(f"AI: {response.content}\n")

print(">>> The AI can TALK about doing things, but can't actually DO them.")
print(">>> An AGENT solves this with TOOLS (email API, file writer).\n")

# ============================================================
# Limitation 5: HALLUCINATION
# ============================================================

print("=" * 50)
print("LIMITATION 5: Hallucination (Confident Mistakes)")
print("=" * 50)

response = llm.invoke("Tell me about the Python library called 'superfast_ml' and who created it.")
print(f"Q: Tell me about 'superfast_ml' library")
print(f"AI: {response.content}\n")

print(">>> 'superfast_ml' doesn't exist! But the AI may confidently describe it.")
print(">>> This is called 'hallucination' — generating plausible but false information.")
print(">>> An AGENT can verify facts using TOOLS (search, documentation lookup).\n")

# ============================================================
# Summary: The Gap That Agents Fill
# ============================================================

print("=" * 50)
print("SUMMARY: Why We Need Agents")
print("=" * 50)
print("""
 LLM Limitation          Agent Solution
 ─────────────────       ──────────────────
 No memory            →  Memory component (conversation history, databases)
 No real-time data    →  Tools (web search, APIs)
 Bad at math          →  Tools (calculator, code execution)
 Can't take actions   →  Tools (email, file I/O, APIs)
 Hallucinations       →  Tools (fact-checking) + Reflection pattern

 An AGENT = LLM + Memory + Tools + Planning
 That's what this course is all about!
""")

# ============================================================
# TODO 1: Find more limitations
# ============================================================
# Try these and observe what happens:
#   a) "What time is it?" (no clock access)
#   b) "Count the words in this sentence: The quick brown fox" (try it!)
#   c) "What is on my desktop screen right now?" (no vision here)

# TODO: Test these and note what the LLM says

# ============================================================
# TODO 2: Real-time vs training data
# ============================================================
# Ask the LLM about something that happened very recently (this year).
# Then ask about something from 2020. Notice the difference in confidence.

# response = llm.invoke("Who won the 2024 Olympics 100m sprint?")
# print(response.content)
#
# response = llm.invoke("Who was the US President in 2020?")
# print(response.content)

print("Lab 03 complete! Now you know why agents are needed.")
