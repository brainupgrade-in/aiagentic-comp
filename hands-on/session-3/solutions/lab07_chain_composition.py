"""
Lab 07: Chain Composition — SOLUTION
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

llm = ChatOllama(model="llama3.2:1b")

# Chain 1: Generate a topic
print("--- Chain 1: Generate a topic ---")
topic_prompt = ChatPromptTemplate.from_template(
    "Give me one specific, interesting topic about {subject}. Reply with just the topic name, nothing else."
)
topic_chain = topic_prompt | llm | StrOutputParser()

topic = topic_chain.invoke({"subject": "space exploration"})
print(f"Generated topic: {topic}\n")

# Chain 2: Write about it
print("--- Chain 2: Write about the topic ---")
write_prompt = ChatPromptTemplate.from_template(
    "Write a 3-sentence explanation of: {topic}"
)
write_chain = write_prompt | llm | StrOutputParser()

explanation = write_chain.invoke({"topic": topic})
print(f"Explanation: {explanation}\n")

# Combined chain
print("--- Combined chain ---")
full_chain = (
    topic_chain
    | (lambda topic: {"topic": topic})
    | write_chain
)
result = full_chain.invoke({"subject": "artificial intelligence"})
print(f"Result: {result}\n")

# Three-stage pipeline
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
print(f"Kid-friendly: {result}\n")

# RunnablePassthrough
print("--- RunnablePassthrough ---")
answer_prompt = ChatPromptTemplate.from_messages([
    ("system", "Be concise. One sentence."),
    ("human", "{question}"),
])
answer_chain = answer_prompt | llm | StrOutputParser()

qa_chain = RunnableParallel(
    question=RunnablePassthrough(),
    answer=answer_chain,
)
result = qa_chain.invoke({"question": "What is Docker?"})
print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}\n")

# TODO 1: Topic → Quiz pipeline
print("--- Topic → Quiz Pipeline ---")
quiz_prompt = ChatPromptTemplate.from_template(
    "Create a multiple-choice quiz question about: {topic}\n"
    "Format: Question, then A), B), C), D) options."
)
quiz_chain = quiz_prompt | llm | StrOutputParser()

topic_to_quiz = (
    topic_chain
    | (lambda t: {"topic": t})
    | quiz_chain
)
print(topic_to_quiz.invoke({"subject": "Python programming"}))
print()

# TODO 2: Translate → Verify pipeline
print("--- Translate → Verify Pipeline ---")
to_hindi = ChatPromptTemplate.from_template(
    "Translate to Hindi. Return only the translation:\n{text}"
)
to_english = ChatPromptTemplate.from_template(
    "Translate to English. Return only the translation:\n{text}"
)

hindi_chain = to_hindi | llm | StrOutputParser()
english_chain = to_english | llm | StrOutputParser()

original = "Technology makes life easier"
hindi = hindi_chain.invoke({"text": original})
back = english_chain.invoke({"text": hindi})

print(f"Original:         {original}")
print(f"Hindi:            {hindi}")
print(f"Back to English:  {back}")
print()

# TODO 3: Parallel analysis
print("--- Parallel Analysis ---")
text_to_analyze = "Python is an amazing programming language. It makes development fast and fun. I love using it for data science and machine learning projects."

sentiment_prompt = ChatPromptTemplate.from_template(
    "Reply with exactly one word - Positive, Negative, or Neutral:\n{text}"
)
summary_prompt = ChatPromptTemplate.from_template(
    "Summarize in one sentence:\n{text}"
)
topics_prompt = ChatPromptTemplate.from_template(
    "List 3 key topics as comma-separated words:\n{text}"
)

parallel_analysis = RunnableParallel(
    sentiment=sentiment_prompt | llm | StrOutputParser(),
    summary=summary_prompt | llm | StrOutputParser(),
    topics=topics_prompt | llm | StrOutputParser(),
)

result = parallel_analysis.invoke({"text": text_to_analyze})
print(f"Sentiment: {result['sentiment']}")
print(f"Summary: {result['summary']}")
print(f"Topics: {result['topics']}")

print("\n" + "=" * 50)
print("Lab 07 complete!")
