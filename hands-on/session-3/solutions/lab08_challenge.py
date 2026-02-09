"""
Lab 08: Challenge — Build a Mini App — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:1b")

print("=" * 50)
print("  Tech Interview Prep Assistant")
print("=" * 50)

# PART A: Explanation chain
explain_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a tech interview coach. Explain concepts clearly and concisely, as if answering an interview question. Keep it to 2-3 sentences."),
    ("human", "Explain {technology} for a technical interview."),
])
explain_chain = explain_prompt | llm | StrOutputParser()

# PART B: Question generator chain
question_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior technical interviewer. Generate one challenging but fair interview question. Return just the question, nothing else."),
    ("human", "Generate an interview question about {technology}"),
])
question_chain = question_prompt | llm | StrOutputParser()

# PART C: Answer chain
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a senior engineer answering an interview question. Give a clear, structured answer in 3-4 sentences that would impress the interviewer."),
    ("human", "Answer this interview question:\n{question}"),
])
answer_chain = answer_prompt | llm | StrOutputParser()

# PART D: Run the pipeline
technologies = ["Docker", "Kubernetes", "REST API"]

for technology in technologies:
    print(f"\nTechnology: {technology}")
    print("-" * 40)

    explanation = explain_chain.invoke({"technology": technology})
    print(f"\nExplanation:\n{explanation}")

    question = question_chain.invoke({"technology": technology})
    print(f"\nInterview Question:\n{question}")

    answer = answer_chain.invoke({"question": question})
    print(f"\nModel Answer:\n{answer}")
    print()

# PART E: Interactive mode with streaming
print("=" * 50)
print("Interactive Mode (type 'quit' to exit)")
print("=" * 50)

while True:
    tech = input("\nEnter a technology (or 'quit' to exit): ").strip()
    if tech.lower() == "quit":
        break

    print(f"\nPreparing interview prep for: {tech}")
    print("-" * 40)

    print("\nExplanation: ", end="")
    for chunk in explain_chain.stream({"technology": tech}):
        print(chunk, end="", flush=True)

    print("\n\nInterview Question: ", end="")
    question = question_chain.invoke({"technology": tech})
    print(question)

    print("\nModel Answer: ", end="")
    for chunk in answer_chain.stream({"question": question}):
        print(chunk, end="", flush=True)
    print()
