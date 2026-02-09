"""
Lab 07: Chain Composition
==========================
Goal: Connect multiple chains — the output of one becomes the input of the next.

What you'll learn:
- How to chain two independent chains together
- Using lambda to transform data between chains
- RunnablePassthrough for passing data through unchanged
- Building complex workflows from simple pieces
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

llm = ChatOllama(model="llama3.2:1b")

# ============================================================
# Step 1: Two independent chains
# ============================================================
# Chain 1 generates a topic. Chain 2 writes about it.

print("--- Chain 1: Generate a topic ---")

topic_prompt = ChatPromptTemplate.from_template(
    "Give me one specific, interesting topic about {subject}. Reply with just the topic name, nothing else."
)
topic_chain = topic_prompt | llm | StrOutputParser()

topic = topic_chain.invoke({"subject": "space exploration"})
print(f"Generated topic: {topic}\n")

print("--- Chain 2: Write about the topic ---")

write_prompt = ChatPromptTemplate.from_template(
    "Write a 3-sentence explanation of: {topic}"
)
write_chain = write_prompt | llm | StrOutputParser()

explanation = write_chain.invoke({"topic": topic})
print(f"Explanation: {explanation}\n")

# ============================================================
# Step 2: Connect chains with lambda
# ============================================================
# Chain 1 outputs a string, but Chain 2 expects {"topic": string}.
# A lambda bridges the gap.

print("--- Combined chain (auto-connected) ---")

full_chain = (
    topic_chain
    | (lambda topic: {"topic": topic})  # Transform: str → dict
    | write_chain
)

result = full_chain.invoke({"subject": "artificial intelligence"})
print(f"Result: {result}\n")

# ============================================================
# Step 3: Three-stage pipeline
# ============================================================
# Stage 1: Generate a topic
# Stage 2: Write an explanation
# Stage 3: Simplify the explanation

print("--- Three-stage pipeline ---")

simplify_prompt = ChatPromptTemplate.from_template(
    "Rewrite this so a 10-year-old can understand it. Use simple words:\n\n{text}"
)
simplify_chain = simplify_prompt | llm | StrOutputParser()

three_stage = (
    topic_chain
    | (lambda topic: {"topic": topic})
    | write_chain
    | (lambda explanation: {"text": explanation})
    | simplify_chain
)

result = three_stage.invoke({"subject": "quantum computing"})
print(f"Kid-friendly explanation: {result}\n")

# ============================================================
# Step 4: RunnablePassthrough — pass data through
# ============================================================
# Sometimes you need the original input alongside generated output.
# RunnablePassthrough passes data through unchanged.

print("--- RunnablePassthrough ---")

from langchain_core.runnables import RunnableParallel

# This runs two things in parallel:
#   1. Passes the question through as-is
#   2. Generates an answer via the chain
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise. One sentence."),
    ("human", "{question}"),
])
answer_chain = answer_prompt | llm | StrOutputParser()

qa_chain = RunnableParallel(
    question=RunnablePassthrough(),  # Pass input through
    answer=answer_chain,             # Generate answer
)

result = qa_chain.invoke({"question": "What is Docker?"})
print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
print()

# ============================================================
# TODO 1: Build a "Topic → Quiz" pipeline
# ============================================================
# Chain 1: Takes a {subject} and generates a specific topic
# Chain 2: Takes the topic and creates a quiz question with 4 choices
# Bonus: Add Chain 3 that generates the answer explanation

# topic_chain is already defined above
# quiz_prompt = ChatPromptTemplate.from_template(
#     "Create a multiple-choice quiz question about: {topic}\n"
#     "Format: Question, then A), B), C), D) options."
# )
# quiz_chain = quiz_prompt | llm | StrOutputParser()
#
# topic_to_quiz = (
#     topic_chain
#     | (lambda t: {"topic": t})
#     | quiz_chain
# )
# print(topic_to_quiz.invoke({"subject": "Python programming"}))

# ============================================================
# TODO 2: Build a "Translate → Verify" pipeline
# ============================================================
# Chain 1: Translate text from English to Hindi
# Chain 2: Translate the Hindi back to English
# Compare: Does the back-translation match the original?

# This is a real technique used to verify translation quality!

# ============================================================
# TODO 3: RunnableParallel — run multiple analyses
# ============================================================
# Given a text, run three analyses in parallel:
#   1. Sentiment (positive/negative/neutral)
#   2. Summary (one sentence)
#   3. Key topics (list of keywords)

# parallel_analysis = RunnableParallel(
#     sentiment=sentiment_chain,
#     summary=summary_chain,
#     topics=topics_chain,
# )
# result = parallel_analysis.invoke({"text": "your text here"})

print("=" * 50)
print("Lab 07 complete! Key takeaways:")
print("- Lambda bridges transform data between chains")
print("- Multi-stage pipelines: chain1 | transform | chain2 | ...")
print("- RunnablePassthrough passes data through unchanged")
print("- RunnableParallel runs multiple chains simultaneously")
print("- Complex agents are built from simple, composable chains")
