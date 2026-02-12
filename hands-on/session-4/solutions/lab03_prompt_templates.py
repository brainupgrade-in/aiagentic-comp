"""
Lab 03: Prompt Templates — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="llama3.2:1b")

# Translation template
print("--- Translation Template ---")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate accurately and only return the translation."),
    ("human", "Translate '{text}' to {language}"),
])

for text, lang in [("Good morning", "French"), ("Good morning", "Japanese"), ("Thank you", "Hindi")]:
    messages = prompt.invoke({"text": text, "language": lang})
    response = llm.invoke(messages)
    print(f"  '{text}' → {lang}: {response.content}")

# Look inside
print("\n--- What the template produces ---")
messages = prompt.invoke({"text": "Hello", "language": "Spanish"})
print(f"Type: {type(messages)}")
print(f"Messages: {messages.to_messages()}")

# Multi-variable template
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

# TODO 1: Code review template
print("\n--- Code Review ---")
review_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior {language} code reviewer. Review the code for correctness, style, and potential issues. Be concise."),
    ("human", "Review this code:\n```\n{code}\n```"),
])

response = llm.invoke(review_prompt.invoke({
    "language": "Python",
    "code": "def add(a, b): return a + b",
}))
print(response.content)

# TODO 2: Email writer template
print("\n--- Email Writer ---")
email_prompt = ChatPromptTemplate.from_messages([
    ("system", "You write short, professional emails. Tone: {tone}. Keep it under 5 sentences."),
    ("human", "Write an email to {recipient} about: {subject}"),
])

response = llm.invoke(email_prompt.invoke({
    "tone": "formal",
    "recipient": "the engineering team",
    "subject": "scheduled maintenance this weekend",
}))
print(response.content)

# TODO 3: from_template shorthand
print("\n--- Fun Fact (from_template) ---")
simple_prompt = ChatPromptTemplate.from_template(
    "Tell me a fun fact about {topic}"
)
response = llm.invoke(simple_prompt.invoke({"topic": "octopuses"}))
print(response.content)

print("\n" + "=" * 50)
print("Lab 03 complete!")
