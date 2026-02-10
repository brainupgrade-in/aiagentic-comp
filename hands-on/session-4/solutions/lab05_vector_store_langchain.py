"""
Lab 05: LangChain + ChromaDB Integration — SOLUTION
"""

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

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
print("Creating vector store...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings, collection_name="company_docs")
print(f"Vector store: {vectorstore._collection.count()} documents")

# Direct search
print("\n--- Direct Similarity Search ---")
results = vectorstore.similarity_search("How many days off do I get?", k=3)
for i, doc in enumerate(results):
    print(f"  {i+1}. {doc.page_content[:80]}...")
    print(f"     {doc.metadata['source']}, Page {doc.metadata['page']}\n")

# Search with scores
print("--- Search with Scores ---")
results_with_scores = vectorstore.similarity_search_with_score("How do I work from home?", k=3)
for doc, score in results_with_scores:
    print(f"  [{score:.4f}] {doc.page_content[:70]}...")

# Retriever
print("\n--- Retriever ---")
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
docs = retriever.invoke("What is the expense policy?")
for doc in docs:
    print(f"  - {doc.page_content[:80]}...")
    print(f"    [{doc.metadata['category']}] {doc.metadata['source']} p.{doc.metadata['page']}\n")

# MMR
print("--- MMR Retriever ---")
retriever_mmr = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 3, "fetch_k": 6})
docs_mmr = retriever_mmr.invoke("Tell me about employee benefits")
for doc in docs_mmr:
    print(f"  [{doc.metadata['category']}] {doc.page_content[:70]}...")

# TODO 1: Metadata filter
retriever_filtered = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3, "filter": {"category": "leave"}},
)
leave_docs = retriever_filtered.invoke("What are my options?")
print("\n--- Filtered to 'leave' ---")
for doc in leave_docs:
    print(f"  - {doc.page_content[:80]}...")

# TODO 2: Add new documents
vectorstore.add_documents([
    Document(page_content="Performance reviews happen quarterly. Self-assessment due 1 week before the review.",
             metadata={"source": "handbook.pdf", "page": 18, "category": "hr"}),
])
print(f"\nTotal docs now: {vectorstore._collection.count()}")
new_results = retriever.invoke("When are performance reviews?")
for doc in new_results:
    print(f"  - {doc.page_content[:80]}...")

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- Chroma.from_documents() embeds + stores in one step")
print("- similarity_search() finds relevant docs by meaning")
print("- as_retriever() creates a reusable retriever with .invoke()")
print("- MMR search balances relevance with diversity")
print("- Metadata filters narrow results to specific categories")
