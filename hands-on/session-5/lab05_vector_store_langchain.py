"""
Lab 05: LangChain + ChromaDB Integration
==========================================
Goal: Use LangChain's Chroma wrapper to store document chunks and create
      a retriever for searching them.

What you'll learn:
- How to use Chroma.from_documents() to embed and store chunks
- How to create a retriever with vectorstore.as_retriever()
- How retriever.invoke() finds relevant documents
- The difference between "similarity" and "mmr" search types
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ============================================================
# Step 1: Prepare sample documents
# ============================================================
# We'll create Document objects with metadata — this simulates
# what you'd get from loading PDFs or web pages.

documents = [
    Document(page_content="Annual leave is 24 days per year. Unused leave cannot be carried forward. Apply through the internal portal at least 3 days in advance.",
             metadata={"source": "handbook.pdf", "page": 5, "category": "leave"}),
    Document(page_content="Sick leave is 12 days per year. A medical certificate is required for absences of more than 2 consecutive days.",
             metadata={"source": "handbook.pdf", "page": 5, "category": "leave"}),
    Document(page_content="Maternity leave is 26 weeks as per government regulations. Paternity leave is 2 weeks. Apply at least 30 days in advance.",
             metadata={"source": "handbook.pdf", "page": 6, "category": "leave"}),
    Document(page_content="Employees can work from home up to 3 days per week with team lead approval. Core hours are 10 AM to 4 PM IST.",
             metadata={"source": "handbook.pdf", "page": 8, "category": "wfh"}),
    Document(page_content="VPN connection is mandatory for accessing internal systems from home. Contact IT for VPN setup.",
             metadata={"source": "handbook.pdf", "page": 8, "category": "wfh"}),
    Document(page_content="Internet reimbursement of Rs 1,500 per month is provided for work-from-home employees. Submit broadband bill by the 5th.",
             metadata={"source": "handbook.pdf", "page": 9, "category": "expense"}),
    Document(page_content="Travel expenses must be submitted with original receipts within 7 days. Meal allowance during client visits is Rs 500 per day.",
             metadata={"source": "handbook.pdf", "page": 12, "category": "expense"}),
    Document(page_content="Laptops are provided by the company and replaced every 3 years. Software license requests go through the IT helpdesk.",
             metadata={"source": "tech-guide.pdf", "page": 7, "category": "tech"}),
    Document(page_content="Our tech stack: Python (FastAPI) and Java (Spring Boot) for backend, React and Angular for frontend, PostgreSQL and MongoDB for databases.",
             metadata={"source": "tech-guide.pdf", "page": 3, "category": "tech"}),
    Document(page_content="Bangalore office: WeWork Embassy Tech Village, 5th Floor. Headquarters with 200+ employees. Mumbai office: Worli Business District, Tower A.",
             metadata={"source": "handbook.pdf", "page": 15, "category": "office"}),
]

print("=" * 50)
print(f"Prepared {len(documents)} documents")

# ============================================================
# Step 2: Create embeddings and store in ChromaDB
# ============================================================
# Chroma.from_documents() does THREE things in one call:
#   1. Embeds all documents using the embedding model
#   2. Stores the embeddings + text + metadata in ChromaDB
#   3. Returns a Chroma vectorstore object

print("\nCreating vector store (embedding + storing)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="company_docs",
)

print(f"Vector store created with {vectorstore._collection.count()} documents")

# ============================================================
# Step 3: Search the vector store directly
# ============================================================
# similarity_search() returns Document objects ranked by relevance.

print("\n--- Direct Similarity Search ---")
results = vectorstore.similarity_search(
    "How many days off do I get?",
    k=3,
)

print("Query: 'How many days off do I get?'\n")
for i, doc in enumerate(results):
    print(f"  {i+1}. {doc.page_content[:80]}...")
    print(f"     Source: {doc.metadata['source']}, Page: {doc.metadata['page']}\n")

# ============================================================
# Step 4: Search with scores
# ============================================================
# similarity_search_with_score() also returns the distance score.

print("--- Search with Scores ---")
results_with_scores = vectorstore.similarity_search_with_score(
    "How do I work from home?",
    k=3,
)

print("Query: 'How do I work from home?'\n")
for doc, score in results_with_scores:
    print(f"  [{score:.4f}] {doc.page_content[:70]}...")
    print(f"           Category: {doc.metadata['category']}\n")

# ============================================================
# Step 5: Create a retriever
# ============================================================
# A retriever wraps the vector store with a standard .invoke() interface.
# This is what you'll plug into a RAG chain.

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

print("--- Retriever ---")
docs = retriever.invoke("What is the expense policy?")

print("Query: 'What is the expense policy?'\n")
for doc in docs:
    print(f"  - {doc.page_content[:80]}...")
    print(f"    [{doc.metadata['category']}] {doc.metadata['source']} p.{doc.metadata['page']}\n")

# ============================================================
# Step 6: Try MMR (Max Marginal Relevance) search
# ============================================================
# MMR balances relevance with diversity — avoids returning
# redundant/similar results. Good when documents overlap.

retriever_mmr = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 6},  # fetch 6, pick 3 diverse ones
)

print("--- MMR Retriever (diverse results) ---")
docs_mmr = retriever_mmr.invoke("Tell me about employee benefits")

print("Query: 'Tell me about employee benefits'\n")
for doc in docs_mmr:
    print(f"  [{doc.metadata['category']}] {doc.page_content[:70]}...")

# ============================================================
# TODO 1: Search with metadata filter
# ============================================================
# Create a retriever that only searches within a specific category.
# Hint: Use search_kwargs with a "filter" parameter.

# TODO: Uncomment and try
# retriever_filtered = vectorstore.as_retriever(
#     search_type="similarity",
#     search_kwargs={"k": 3, "filter": {"category": "leave"}},
# )
# leave_docs = retriever_filtered.invoke("What are my options?")
# print("\n--- Filtered to 'leave' category ---")
# for doc in leave_docs:
#     print(f"  - {doc.page_content[:80]}...")

# ============================================================
# TODO 2: Add new documents and search again
# ============================================================
# Add a few more documents to the existing vectorstore and search.

# TODO: Uncomment and add your documents
# vectorstore.add_documents([
#     Document(page_content="YOUR NEW DOCUMENT TEXT",
#              metadata={"source": "new-doc.pdf", "page": 1, "category": "YOUR_CATEGORY"}),
# ])
# print(f"\nTotal docs now: {vectorstore._collection.count()}")
# new_results = retriever.invoke("YOUR QUERY ABOUT NEW DOCUMENTS")
# for doc in new_results:
#     print(f"  - {doc.page_content[:80]}...")

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- Chroma.from_documents() embeds + stores in one step")
print("- similarity_search() finds relevant docs by meaning")
print("- as_retriever() creates a reusable retriever with .invoke()")
print("- MMR search balances relevance with diversity")
print("- Metadata filters narrow results to specific categories")
