"""
Lab 06: Streaming & Batch — SOLUTION
"""

import time
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:1b")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Keep responses to 2-3 sentences."),
    ("human", "{question}"),
])
chain = prompt | llm | StrOutputParser()

# .invoke()
print("--- .invoke() ---")
start = time.time()
result = chain.invoke({"question": "What is cloud computing?"})
elapsed = time.time() - start
print(result)
print(f"(Completed in {elapsed:.1f}s)\n")

# .stream()
print("--- .stream() ---")
start = time.time()
for chunk in chain.stream({"question": "What is cloud computing?"}):
    print(chunk, end="", flush=True)
elapsed = time.time() - start
print(f"\n(Streamed in {elapsed:.1f}s)\n")

# .batch()
print("--- .batch() ---")
start = time.time()
questions = [
    {"question": "What is Docker?"},
    {"question": "What is Kubernetes?"},
    {"question": "What is Terraform?"},
]
results = chain.batch(questions)
elapsed = time.time() - start
for q, r in zip(questions, results):
    print(f"Q: {q['question']}")
    print(f"A: {r}\n")
print(f"(Processed {len(questions)} questions in {elapsed:.1f}s)\n")

# Timing comparison
print("--- Timing comparison ---")
start = time.time()
for q in questions:
    chain.invoke(q)
invoke_time = time.time() - start

start = time.time()
chain.batch(questions)
batch_time = time.time() - start

print(f"Sequential .invoke() x{len(questions)}: {invoke_time:.1f}s")
print(f"Single .batch() call:        {batch_time:.1f}s")
print()

# TODO 1: Streaming translator
print("--- Streaming Translator ---")
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate to {language}. Return only the translation."),
    ("human", "{text}"),
])
translate_chain = translate_prompt | llm | StrOutputParser()

print("Translating to French: ", end="")
for chunk in translate_chain.stream({"text": "India is a beautiful country with diverse cultures", "language": "French"}):
    print(chunk, end="", flush=True)
print("\n")

# TODO 2: Batch — explain 5 technologies
print("--- Batch: 5 Technologies ---")
techs = [
    {"question": "Explain Git in one sentence"},
    {"question": "Explain Linux in one sentence"},
    {"question": "Explain REST API in one sentence"},
    {"question": "Explain CI/CD in one sentence"},
    {"question": "Explain Microservices in one sentence"},
]
results = chain.batch(techs)
for r in results:
    print(f"  {r}")

print("\n" + "=" * 50)
print("Lab 06 complete!")
