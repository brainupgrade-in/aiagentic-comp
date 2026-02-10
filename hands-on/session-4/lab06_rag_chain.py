"""
Lab 06: Your First RAG Chain
==============================
Goal: Build a complete RAG chain that retrieves relevant documents and
      generates grounded answers using LCEL.

What you'll learn:
- How to combine a retriever + prompt + LLM into a RAG chain
- What RunnablePassthrough does in a RAG chain
- How context injection works in the prompt
- The complete data flow from question to answer
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

# ============================================================
# Step 1: Set up the knowledge base
# ============================================================
# We'll reuse the company documents from Lab 05.
# In production, this would be pre-built and loaded from disk.

documents = [
    Document(page_content="Annual leave is 24 days per year. Unused leave cannot be carried forward. Apply through the internal portal at least 3 days in advance.",
             metadata={"source": "handbook.pdf", "page": 5}),
    Document(page_content="Sick leave is 12 days per year. A medical certificate is required for absences of more than 2 consecutive days.",
             metadata={"source": "handbook.pdf", "page": 5}),
    Document(page_content="Maternity leave is 26 weeks as per government regulations. Paternity leave is 2 weeks. Apply at least 30 days in advance.",
             metadata={"source": "handbook.pdf", "page": 6}),
    Document(page_content="Employees can work from home up to 3 days per week with team lead approval. Core hours are 10 AM to 4 PM IST.",
             metadata={"source": "handbook.pdf", "page": 8}),
    Document(page_content="VPN connection is mandatory for accessing internal systems from home. Contact IT helpdesk for VPN setup assistance.",
             metadata={"source": "handbook.pdf", "page": 8}),
    Document(page_content="Internet reimbursement of Rs 1,500 per month for WFH employees. Submit broadband bill to finance by the 5th of each month.",
             metadata={"source": "handbook.pdf", "page": 9}),
    Document(page_content="Travel expenses must be submitted with original receipts within 7 days. Meal allowance during client visits is Rs 500 per day.",
             metadata={"source": "handbook.pdf", "page": 12}),
    Document(page_content="Laptops are provided by the company and replaced every 3 years. Software license requests go through the IT helpdesk.",
             metadata={"source": "tech-guide.pdf", "page": 7}),
    Document(page_content="Tech stack: Python (FastAPI), Java (Spring Boot) for backend. React, Angular for frontend. PostgreSQL, MongoDB for databases. AWS for cloud.",
             metadata={"source": "tech-guide.pdf", "page": 3}),
    Document(page_content="Bangalore office: WeWork Embassy Tech Village, 5th Floor (HQ, 200+ employees). Mumbai office: Worli Business District, Tower A, 12th Floor.",
             metadata={"source": "handbook.pdf", "page": 15}),
]

print("=" * 50)
print("Building knowledge base...")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print(f"Knowledge base ready: {vectorstore._collection.count()} documents")

# ============================================================
# Step 2: Create the LLM
# ============================================================
llm = ChatGroq(model="llama-3.3-70b-versatile")
print("LLM ready (Groq)")

# ============================================================
# Step 3: Create the RAG prompt
# ============================================================
# The prompt tells the LLM to ONLY use the provided context.
# This prevents hallucination — no context, no answer.

rag_prompt = ChatPromptTemplate.from_template(
    """You are a helpful company assistant. Answer the question based ONLY on the following context.
If the context doesn't contain the answer, say "I don't have that information in our handbook."

Context:
{context}

Question: {question}

Answer:"""
)

# ============================================================
# Step 4: Build the RAG chain with LCEL
# ============================================================
# This is where it all comes together!
#
# The chain works like this:
#   1. User asks a question (string)
#   2. The retriever gets relevant docs from ChromaDB
#   3. format_docs converts Document objects to a string
#   4. RunnablePassthrough passes the original question through
#   5. The prompt template injects context + question
#   6. The LLM generates an answer grounded in the context
#   7. StrOutputParser extracts the text


def format_docs(docs):
    """Join document contents into a single string for the prompt."""
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

print("RAG chain built!")
print("=" * 50)

# ============================================================
# Step 5: Ask questions!
# ============================================================

questions = [
    "How many days of annual leave do I get?",
    "Can I work from home?",
    "What is the meal allowance for client visits?",
    "Where is the Bangalore office?",
]

for q in questions:
    print(f"\nQ: {q}")
    answer = rag_chain.invoke(q)
    print(f"A: {answer}")

# ============================================================
# Step 6: Test with an out-of-scope question
# ============================================================
# The LLM should say it doesn't know — because the context
# doesn't contain this information.

print("\n--- Out-of-scope test ---")
q = "What is the company's stock price?"
print(f"Q: {q}")
answer = rag_chain.invoke(q)
print(f"A: {answer}")

# ============================================================
# TODO 1: Ask your own questions
# ============================================================
# Try questions that are in the knowledge base but use different words.
# For example: "How do I expense a client dinner?"
# The retriever should still find the right context.

# TODO: Uncomment and try your own questions
# my_questions = [
#     "YOUR QUESTION 1",
#     "YOUR QUESTION 2",
# ]
# for q in my_questions:
#     print(f"\nQ: {q}")
#     print(f"A: {rag_chain.invoke(q)}")

# ============================================================
# TODO 2: Modify the system prompt
# ============================================================
# Try changing the prompt to make the assistant:
#   - More formal ("You are an HR compliance officer...")
#   - More casual ("Hey! I'm your friendly company bot...")
#   - Respond in bullet points ("Always respond in bullet points")
# See how the prompt affects the answer style.

# TODO: Create a different prompt and rebuild the chain
# my_prompt = ChatPromptTemplate.from_template(
#     """YOUR CUSTOM SYSTEM PROMPT
# Context: {context}
# Question: {question}
# Answer:"""
# )
# my_chain = (
#     {"context": retriever | format_docs, "question": RunnablePassthrough()}
#     | my_prompt | llm | StrOutputParser()
# )
# print(f"\nCustom prompt: {my_chain.invoke('How many leaves do I get?')}")

print("\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- RAG chain = retriever | format | prompt | llm | parser")
print("- RunnablePassthrough passes the question through unchanged")
print("- The LLM only uses the context you provide — no hallucination")
print("- Prompt engineering shapes how the answer is delivered")
