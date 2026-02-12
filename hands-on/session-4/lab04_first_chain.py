"""
Lab 04: Your First Chain (LCEL)
================================
Goal: Build your first chain using LCEL pipe syntax: prompt | llm | parser

What you'll learn:
- What LCEL (LangChain Expression Language) is
- The pipe operator | connects components
- StrOutputParser extracts text from the response
- Why chains are better than manual step-by-step calls
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: The manual way (without chains)
# ============================================================
# This works, but it's verbose and hard to reuse.

print("--- Manual approach (3 separate steps) ---")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Be concise."),
    ("human", "{question}"),
])

# Step by step:
messages = prompt.invoke({"question": "What is Docker?"})  # Step 1: format prompt
response = llm.invoke(messages)                             # Step 2: send to LLM
text = response.content                                     # Step 3: extract text

print(text)
print()

# ============================================================
# Step 2: The LCEL way (one chain, one line)
# ============================================================
# The pipe | operator connects: prompt → llm → parser
# Each component's output automatically becomes the next one's input.

print("--- LCEL chain (one line!) ---")

chain = prompt | llm | StrOutputParser()

# Now invoke the entire chain in one call
result = chain.invoke({"question": "What is Docker?"})

print(result)
print(f"\nType: {type(result)}")  # It's a plain string now!
print()

# ============================================================
# Step 3: Understand the data flow
# ============================================================
# Let's trace what happens at each step.

print("--- Data flow through the chain ---")

# Stage 1: Prompt takes a dict → produces messages
stage1 = prompt.invoke({"question": "What is Kubernetes?"})
print(f"After prompt:  {type(stage1).__name__} → {len(stage1.to_messages())} messages")

# Stage 2: LLM takes messages → produces AIMessage
stage2 = llm.invoke(stage1)
print(f"After LLM:     {type(stage2).__name__} → '{stage2.content[:50]}...'")

# Stage 3: Parser takes AIMessage → produces string
parser = StrOutputParser()
stage3 = parser.invoke(stage2)
print(f"After parser:  {type(stage3).__name__} → '{stage3[:50]}...'")

# The chain does all three stages in one .invoke() call!

# ============================================================
# Step 4: Reuse the chain with different inputs
# ============================================================
# The chain is a reusable object. Pass different inputs each time.

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

# ============================================================
# TODO 1: Build a chain that translates text
# ============================================================
# Create a chain: translation_prompt | llm | StrOutputParser()
# The prompt should accept {text} and {language} variables.

# TODO: Build the translation chain
# translate_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a translator. Return only the translation."),
#     ("human", "Translate '{text}' to {language}"),
# ])
#
# translate_chain = translate_prompt | llm | StrOutputParser()
#
# result = translate_chain.invoke({"text": "Welcome to India", "language": "Tamil"})
# print(f"Translation: {result}")

# ============================================================
# TODO 2: Build a chain that summarizes text
# ============================================================
# Create a chain that takes {text} and {max_words} as input
# and returns a summary within the word limit.

# TODO: Build the summarizer chain and test it with a paragraph

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- LCEL chain: prompt | llm | parser")
print("- The pipe | passes output of each step to the next")
print("- StrOutputParser extracts plain text from AIMessage")
print("- Chains are reusable objects — invoke with different inputs")
