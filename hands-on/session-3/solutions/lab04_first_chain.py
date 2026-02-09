"""
Lab 04: Your First Chain (LCEL) — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:1b")

# Manual approach
print("--- Manual approach ---")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    ("human", "{question}"),
])

messages = prompt.invoke({"question": "What is Docker?"})
response = llm.invoke(messages)
text = response.content
print(text)
print()

# LCEL chain
print("--- LCEL chain ---")
chain = prompt | llm | StrOutputParser()
result = chain.invoke({"question": "What is Docker?"})
print(result)
print(f"Type: {type(result)}")
print()

# Data flow
print("--- Data flow ---")
stage1 = prompt.invoke({"question": "What is Kubernetes?"})
print(f"After prompt:  {type(stage1).__name__} → {len(stage1.to_messages())} messages")

stage2 = llm.invoke(stage1)
print(f"After LLM:     {type(stage2).__name__} → '{stage2.content[:50]}...'")

parser = StrOutputParser()
stage3 = parser.invoke(stage2)
print(f"After parser:  {type(stage3).__name__} → '{stage3[:50]}...'")

# Reuse
print("\n--- Reusing the chain ---")
questions = [
    "What is Git in one sentence?",
    "What is an API in one sentence?",
    "What is a database in one sentence?",
]
for q in questions:
    answer = chain.invoke({"question": q})
    print(f"Q: {q}")
    print(f"A: {answer}\n")

# TODO 1: Translation chain
print("--- Translation chain ---")
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Return only the translation."),
    ("human", "Translate '{text}' to {language}"),
])
translate_chain = translate_prompt | llm | StrOutputParser()

result = translate_chain.invoke({"text": "Welcome to India", "language": "Tamil"})
print(f"Translation: {result}")

# TODO 2: Summarizer chain
print("\n--- Summarizer chain ---")
summarize_prompt = ChatPromptTemplate.from_messages([
    ("system", "Summarize the given text in {max_words} words or fewer. Return only the summary."),
    ("human", "{text}"),
])
summarize_chain = summarize_prompt | llm | StrOutputParser()

result = summarize_chain.invoke({
    "text": "Docker is a platform that uses containerization technology to package applications and their dependencies into lightweight, portable containers. These containers can run consistently across different environments, from a developer's laptop to a production server. Docker simplifies deployment, scaling, and management of applications by isolating them from the underlying infrastructure.",
    "max_words": "20",
})
print(f"Summary: {result}")

print("\n" + "=" * 50)
print("Lab 04 complete!")
