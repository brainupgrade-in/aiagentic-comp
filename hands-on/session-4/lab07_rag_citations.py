"""
Lab 07: RAG with Citations
============================
Goal: Enhance your RAG chain to include source citations and use
      metadata filtering for precise retrieval.

What you'll learn:
- How to format documents with source info for citations
- How to make the LLM include citations in its answers
- How to filter retrieval by metadata (category, source)
- How to see which documents were retrieved for a query
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
# Step 1: Build the knowledge base (same as Lab 06)
# ============================================================

documents = [
    Document(page_content="Annual leave is 24 days per year. Unused leave cannot be carried forward. Apply through the internal portal at least 3 days in advance.",
             metadata={"source": "handbook.pdf", "page": 5, "category": "leave"}),
    Document(page_content="Sick leave is 12 days per year. A medical certificate is required for absences of more than 2 consecutive days.",
             metadata={"source": "handbook.pdf", "page": 5, "category": "leave"}),
    Document(page_content="Maternity leave is 26 weeks as per government regulations. Paternity leave is 2 weeks. Apply at least 30 days in advance.",
             metadata={"source": "handbook.pdf", "page": 6, "category": "leave"}),
    Document(page_content="Employees can work from home up to 3 days per week with team lead approval. Core hours are 10 AM to 4 PM IST.",
             metadata={"source": "handbook.pdf", "page": 8, "category": "wfh"}),
    Document(page_content="VPN connection is mandatory for accessing internal systems from home. Contact IT helpdesk for VPN setup.",
             metadata={"source": "handbook.pdf", "page": 8, "category": "wfh"}),
    Document(page_content="Internet reimbursement of Rs 1,500 per month for WFH employees. Submit broadband bill to finance by the 5th of each month.",
             metadata={"source": "handbook.pdf", "page": 9, "category": "expense"}),
    Document(page_content="Travel expenses must be submitted with original receipts within 7 days. Meal allowance during client visits is Rs 500 per day.",
             metadata={"source": "handbook.pdf", "page": 12, "category": "expense"}),
    Document(page_content="Laptops are provided by the company and replaced every 3 years. Software license requests go through the IT helpdesk.",
             metadata={"source": "tech-guide.pdf", "page": 7, "category": "tech"}),
    Document(page_content="Tech stack: Python (FastAPI), Java (Spring Boot) for backend. React, Angular for frontend. PostgreSQL, MongoDB for databases.",
             metadata={"source": "tech-guide.pdf", "page": 3, "category": "tech"}),
    Document(page_content="Bangalore office: WeWork Embassy Tech Village, 5th Floor (HQ). Mumbai: Worli Business District, Tower A. Hyderabad: HITEC City, Cyber Gateway.",
             metadata={"source": "handbook.pdf", "page": 15, "category": "office"}),
]

print("Building knowledge base...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatGroq(model="llama-3.3-70b-versatile")
print("=" * 50)

# ============================================================
# Step 2: Format documents WITH source info
# ============================================================
# Instead of just joining text, we include the source and page
# so the LLM can cite them in its answer.


def format_docs_with_sources(docs):
    """Format documents with source metadata for citation."""
    formatted = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        page = doc.metadata.get("page", "?")
        formatted.append(f"[Source: {source}, Page {page}]\n{doc.page_content}")
    return "\n\n".join(formatted)


# ============================================================
# Step 3: Citation-aware prompt
# ============================================================
# Tell the LLM to include source references in its answer.

citation_prompt = ChatPromptTemplate.from_template(
    """You are a helpful company assistant. Answer the question using ONLY the context below.
For each fact you mention, include the source in parentheses like (handbook.pdf, p.5).
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}

Question: {question}

Answer (with citations):"""
)

# ============================================================
# Step 4: Build the citation RAG chain
# ============================================================

citation_chain = (
    {"context": retriever | format_docs_with_sources, "question": RunnablePassthrough()}
    | citation_prompt
    | llm
    | StrOutputParser()
)

print("\n--- RAG with Citations ---")
questions = [
    "How many sick days do I get, and do I need a doctor's note?",
    "What are the WFH rules?",
    "How do I claim travel expenses?",
]

for q in questions:
    print(f"\nQ: {q}")
    answer = citation_chain.invoke(q)
    print(f"A: {answer}")

# ============================================================
# Step 5: See which documents were retrieved
# ============================================================
# Sometimes you want to inspect what the retriever found.
# This helps debug why an answer might be wrong or incomplete.

print("\n--- Retrieved Documents Inspection ---")
query = "What tech stack does the company use?"
retrieved_docs = retriever.invoke(query)

print(f"Query: '{query}'")
print(f"Retrieved {len(retrieved_docs)} documents:\n")
for i, doc in enumerate(retrieved_docs):
    print(f"  {i+1}. [{doc.metadata['source']}, p.{doc.metadata['page']}]")
    print(f"     {doc.page_content[:80]}...\n")

answer = citation_chain.invoke(query)
print(f"Answer: {answer}")

# ============================================================
# Step 6: Filtered retrieval
# ============================================================
# Create a retriever that only searches specific categories.

print("\n--- Filtered Retrieval (leave category only) ---")
leave_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3, "filter": {"category": "leave"}},
)

leave_chain = (
    {"context": leave_retriever | format_docs_with_sources, "question": RunnablePassthrough()}
    | citation_prompt
    | llm
    | StrOutputParser()
)

q = "What are all the types of leave available?"
print(f"Q: {q}")
print(f"A: {leave_chain.invoke(q)}")

# ============================================================
# TODO 1: Create a filtered chain for expenses
# ============================================================
# Build a chain that only retrieves expense-related documents.
# Test it with: "What can I expense?" and "How much is the meal allowance?"

# TODO: Uncomment and build
# expense_retriever = vectorstore.as_retriever(
#     search_kwargs={"k": 3, "filter": {"category": "expense"}},
# )
# expense_chain = (
#     {"context": expense_retriever | format_docs_with_sources, "question": RunnablePassthrough()}
#     | citation_prompt | llm | StrOutputParser()
# )
# print(f"\nExpense Q: What can I expense?")
# print(f"Expense A: {expense_chain.invoke('What can I expense?')}")

# ============================================================
# TODO 2: Improve the citation format
# ============================================================
# Modify format_docs_with_sources to include the category in the
# source info, like: [Source: handbook.pdf, Page 5, Category: leave]
# Then update the prompt to include the category in citations.

# TODO: Create an improved format function
# def better_format(docs):
#     formatted = []
#     for doc in docs:
#         source = doc.metadata.get("source", "unknown")
#         page = doc.metadata.get("page", "?")
#         category = doc.metadata.get("category", "general")
#         formatted.append(f"[{source}, p.{page}, {category}]\n{doc.page_content}")
#     return "\n\n".join(formatted)
#
# better_chain = (
#     {"context": retriever | better_format, "question": RunnablePassthrough()}
#     | citation_prompt | llm | StrOutputParser()
# )
# print(f"\nBetter citations: {better_chain.invoke('Tell me about WFH policy')}")

print("\n" + "=" * 50)
print("Lab 07 complete! Key takeaways:")
print("- Include source/page info in the context for citations")
print("- Prompt the LLM to cite sources: '(handbook.pdf, p.5)'")
print("- Inspect retrieved docs to debug answer quality")
print("- Metadata filters create category-specific retrievers")
