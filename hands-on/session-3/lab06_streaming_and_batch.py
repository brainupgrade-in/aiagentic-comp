"""
Lab 06: Streaming & Batch
==========================
Goal: Learn the three ways to run a chain — invoke, stream, and batch.

What you'll learn:
- .invoke() — run once, get complete result
- .stream() — get tokens as they're generated (real-time)
- .batch() — process multiple inputs at once
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

# ============================================================
# Step 1: .invoke() — wait for complete response
# ============================================================
# You've been using this. It waits until the full response is ready.

print("--- .invoke() ---")
start = time.time()
result = chain.invoke({"question": "What is cloud computing?"})
elapsed = time.time() - start

print(result)
print(f"(Completed in {elapsed:.1f}s — you waited for the entire response)\n")

# ============================================================
# Step 2: .stream() — real-time token output
# ============================================================
# In a chat UI, users don't want to wait 5 seconds staring at a blank screen.
# .stream() yields tokens as the LLM generates them — feels much faster.

print("--- .stream() ---")
start = time.time()

for chunk in chain.stream({"question": "What is cloud computing?"}):
    print(chunk, end="", flush=True)  # flush=True ensures immediate display

elapsed = time.time() - start
print(f"\n(Streamed in {elapsed:.1f}s — text appeared as it was generated)\n")

# ============================================================
# Step 3: .batch() — process multiple inputs
# ============================================================
# When you need answers to many questions, batch is more efficient
# than calling invoke in a loop.

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

# ============================================================
# Step 4: Compare — invoke loop vs batch
# ============================================================

print("--- Timing comparison ---")

# Sequential invoke
start = time.time()
for q in questions:
    chain.invoke(q)
invoke_time = time.time() - start

# Batch
start = time.time()
chain.batch(questions)
batch_time = time.time() - start

print(f"Sequential .invoke() x{len(questions)}: {invoke_time:.1f}s")
print(f"Single .batch() call:        {batch_time:.1f}s")
print(f"Batch is {'faster' if batch_time < invoke_time else 'similar speed'} on this model")
print()

# ============================================================
# TODO 1: Build a streaming translator
# ============================================================
# Create a translation chain and use .stream() to show the
# translation appearing word by word.

# translate_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a translator. Translate to {language}. Return only the translation."),
#     ("human", "{text}"),
# ])
# translate_chain = translate_prompt | llm | StrOutputParser()
#
# print("Translating...")
# for chunk in translate_chain.stream({"text": "India is a beautiful country with diverse cultures", "language": "French"}):
#     print(chunk, end="", flush=True)
# print()

# ============================================================
# TODO 2: Batch process — explain 5 technologies
# ============================================================
# Use .batch() to explain 5 technologies in parallel.

# techs = [
#     {"question": "Explain Git in one sentence"},
#     {"question": "Explain Linux in one sentence"},
#     {"question": "Explain REST API in one sentence"},
#     {"question": "Explain CI/CD in one sentence"},
#     {"question": "Explain Microservices in one sentence"},
# ]
# results = chain.batch(techs)
# for t, r in zip(techs, results):
#     print(f"  {r}")

print("=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- .invoke()  → complete result, good for scripts/APIs")
print("- .stream()  → real-time tokens, good for chat UIs")
print("- .batch()   → multiple inputs, good for bulk processing")
print("- All three work on ANY LCEL chain — no extra code needed")
