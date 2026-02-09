"""
Lab 03: Prompt Templates
=========================
Goal: Build reusable prompts with variables using ChatPromptTemplate.

What you'll learn:
- Why templates are better than hardcoded strings
- How to create and use ChatPromptTemplate
- How variables get substituted at runtime
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: The problem with hardcoded prompts
# ============================================================
# Imagine building a translation app. Without templates:

print("--- Hardcoded approach (bad) ---")
response = llm.invoke("Translate 'Good morning' to French")
print(f"French: {response.content}")

# To translate to Spanish, you'd need to write a whole new string.
# To translate a different phrase, another new string. Not scalable!

# ============================================================
# Step 2: ChatPromptTemplate — define once, reuse forever
# ============================================================
# Variables go in {curly_braces}. They get filled in at runtime.

print("\n--- Template approach (good) ---")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate accurately and only return the translation."),
    ("human", "Translate '{text}' to {language}"),
])

# Use the same template for different inputs
for text, lang in [("Good morning", "French"), ("Good morning", "Japanese"), ("Thank you", "Hindi")]:
    messages = prompt.invoke({"text": text, "language": lang})
    response = llm.invoke(messages)
    print(f"  '{text}' → {lang}: {response.content}")

# ============================================================
# Step 3: Look inside the template
# ============================================================
# Let's see what the template produces before sending to the LLM.

print("\n--- What the template produces ---")
messages = prompt.invoke({"text": "Hello", "language": "Spanish"})
print(f"Type: {type(messages)}")
print(f"Messages: {messages.to_messages()}")

# It creates a list of properly formatted messages — exactly what the LLM expects!

# ============================================================
# Step 4: Template with more variables
# ============================================================

print("\n--- Template with multiple variables ---")

explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}. Explain concepts at a {level} level. Keep it to {length}."),
    ("human", "Explain {topic}"),
])

response = llm.invoke(
    explain_prompt.invoke({
        "role": "friendly teacher",
        "level": "beginner",
        "length": "2 sentences",
        "topic": "what a variable is in programming",
    })
)
print(response.content)

# ============================================================
# TODO 1: Build a code review template
# ============================================================
# Create a template that reviews code snippets.
# Variables: {language} (e.g., Python), {code} (the code to review)
# SystemMessage: Act as a senior code reviewer.

# TODO: Create the template
# review_prompt = ChatPromptTemplate.from_messages([
#     ("system", "..."),
#     ("human", "..."),
# ])
#
# response = llm.invoke(review_prompt.invoke({
#     "language": "Python",
#     "code": "def add(a, b): return a + b",
# }))
# print(f"\n--- Code Review ---")
# print(response.content)

# ============================================================
# TODO 2: Build an email writer template
# ============================================================
# Create a template with variables: {tone} (formal/casual), {recipient}, {subject}
# The LLM should write a short email.

# TODO: Build and test the template
# email_prompt = ChatPromptTemplate.from_messages([
#     ("system", "..."),
#     ("human", "..."),
# ])

# ============================================================
# TODO 3: from_template shorthand
# ============================================================
# For simple prompts with just one human message (no system message),
# you can use the shorter from_template() method:

# simple_prompt = ChatPromptTemplate.from_template(
#     "Tell me a fun fact about {topic}"
# )
# response = llm.invoke(simple_prompt.invoke({"topic": "octopuses"}))
# print(f"\n--- Fun Fact ---")
# print(response.content)

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- ChatPromptTemplate makes prompts reusable with {variables}")
print("- .invoke() fills in the variables and returns formatted messages")
print("- Templates enforce consistency across different inputs")
print("- from_messages() for system+human, from_template() for simple prompts")
