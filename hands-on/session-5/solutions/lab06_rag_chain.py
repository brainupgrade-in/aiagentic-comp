"""
Lab 06: Your First RAG Chain — SOLUTION
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

llm = ChatGroq(model="llama-3.3-70b-versatile")
print("RAG chain ready!")
print("=" * 50)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_prompt = ChatPromptTemplate.from_template(
    """You are a helpful company assistant. Answer the question based ONLY on the following context.
If the context doesn't contain the answer, say "I don't have that information in our handbook."

Context:
{context}

Question: {question}

Answer:"""
)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

# Standard questions
questions = [
    "How many days of annual leave do I get?",
    "Can I work from home?",
    "What is the meal allowance for client visits?",
    "Where is the Bangalore office?",
]

for q in questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_chain.invoke(q)}")

# Out-of-scope test
print("\n--- Out-of-scope test ---")
q = "What is the company's stock price?"
print(f"Q: {q}")
print(f"A: {rag_chain.invoke(q)}")

# TODO 1: Custom questions
my_questions = [
    "How do I expense a client dinner?",
    "What databases does the company use?",
]
print("\n--- Custom questions ---")
for q in my_questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_chain.invoke(q)}")

# TODO 2: Modified prompt
casual_prompt = ChatPromptTemplate.from_template(
    """Hey! You're a friendly company chatbot. Answer in a casual, helpful tone.
Use bullet points where possible. Based ONLY on context below.

Context: {context}
Question: {question}
Answer:"""
)
casual_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | casual_prompt | llm | StrOutputParser()
)
print("\n--- Casual prompt ---")
print(f"A: {casual_chain.invoke('How many leaves do I get?')}")

print("\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- RAG chain = retriever | format | prompt | llm | parser")
print("- RunnablePassthrough passes the question through unchanged")
print("- The LLM only uses the context you provide — no hallucination")
print("- Prompt engineering shapes how the answer is delivered")
