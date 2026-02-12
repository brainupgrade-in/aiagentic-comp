"""
Lab 08: Challenge — Build a Mini App
======================================
Goal: Combine everything from Session 3 into a working application.

Your mission: Build a "Tech Interview Prep" assistant that:
1. Takes a technology name as input
2. Generates an explanation suitable for an interview
3. Creates a practice interview question
4. Provides a model answer

This exercise has NO pre-written solution code — only hints and structure.
Use what you learned in Labs 01-07 to build it yourself!
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="llama3.2:1b")

print("=" * 50)
print("  Tech Interview Prep Assistant")
print("=" * 50)

# ============================================================
# PART A: Build the explanation chain
# ============================================================
# Create a chain that takes {technology} and returns a clear,
# interview-ready explanation (2-3 sentences).
#
# Hint: Use ChatPromptTemplate with a system message like:
#   "You are a tech interview coach. Explain concepts clearly
#    and concisely, as if answering an interview question."

# TODO: Build explain_chain
# explain_prompt = ChatPromptTemplate.from_messages([...])
# explain_chain = explain_prompt | llm | StrOutputParser()


# ============================================================
# PART B: Build the question generator chain
# ============================================================
# Create a chain that takes {technology} and generates ONE
# challenging interview question.
#
# Hint: SystemMessage should say something like:
#   "You are a senior interviewer. Generate one technical
#    interview question. Just the question, nothing else."

# TODO: Build question_chain
# question_prompt = ChatPromptTemplate.from_messages([...])
# question_chain = question_prompt | llm | StrOutputParser()


# ============================================================
# PART C: Build the answer chain
# ============================================================
# Create a chain that takes {question} and generates a model
# answer that would impress an interviewer (3-4 sentences).

# TODO: Build answer_chain
# answer_prompt = ChatPromptTemplate.from_messages([...])
# answer_chain = answer_prompt | llm | StrOutputParser()


# ============================================================
# PART D: Wire them together
# ============================================================
# Option 1 (Simple): Call each chain separately
# Option 2 (Advanced): Use chain composition with lambda
#
# The flow should be:
#   technology → explain_chain → explanation
#   technology → question_chain → question
#   question → answer_chain → model_answer

# TODO: Run the full pipeline for a technology
# technology = "Docker"
#
# print(f"\nTechnology: {technology}")
# print("-" * 40)
#
# explanation = explain_chain.invoke({"technology": technology})
# print(f"\nExplanation:\n{explanation}")
#
# question = question_chain.invoke({"technology": technology})
# print(f"\nInterview Question:\n{question}")
#
# answer = answer_chain.invoke({"question": question})
# print(f"\nModel Answer:\n{answer}")


# ============================================================
# PART E (Bonus): Interactive mode with streaming
# ============================================================
# Make it interactive! Ask the user for a technology name,
# then stream the responses in real-time.

# TODO: Uncomment and complete
# while True:
#     tech = input("\nEnter a technology (or 'quit' to exit): ").strip()
#     if tech.lower() == "quit":
#         break
#
#     print(f"\nPreparing interview prep for: {tech}")
#     print("-" * 40)
#
#     print("\nExplanation: ", end="")
#     for chunk in explain_chain.stream({"technology": tech}):
#         print(chunk, end="", flush=True)
#
#     print("\n\nInterview Question: ", end="")
#     question = question_chain.invoke({"technology": tech})
#     print(question)
#
#     print("\nModel Answer: ", end="")
#     for chunk in answer_chain.stream({"question": question}):
#         print(chunk, end="", flush=True)
#     print()


# ============================================================
# PART F (Bonus): Use PydanticOutputParser for structured output
# ============================================================
# Instead of plain text, return a structured object:
#
# class InterviewPrep(BaseModel):
#     technology: str
#     explanation: str
#     question: str
#     model_answer: str
#     difficulty: str  # "Easy", "Medium", "Hard"
#
# This makes the output usable in a web API!

print("\n" + "=" * 50)
print("Challenge tips:")
print("- Start with Part A, test it, then move to Part B")
print("- Use .stream() for a better user experience")
print("- Check solutions/lab08_challenge.py if you're stuck")
print("- Experiment with different system messages!")
