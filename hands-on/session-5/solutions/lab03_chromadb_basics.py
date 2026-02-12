"""
Lab 03: ChromaDB Basics — SOLUTION
"""

import chromadb

client = chromadb.Client()
print("ChromaDB client ready!")
print("=" * 50)

collection = client.get_or_create_collection("company_handbook")
print(f"Collection: '{collection.name}'")

# Add documents
collection.add(
    documents=[
        "Annual leave is 24 days per year. Unused leave cannot be carried forward to the next year.",
        "Sick leave is 12 days per year. A medical certificate is required for more than 2 consecutive days.",
        "Employees can work from home up to 3 days per week. Core hours are 10 AM to 4 PM IST.",
        "Travel expenses must be submitted with receipts within 7 days of travel.",
        "Internet reimbursement is Rs 1,500 per month for work-from-home employees.",
        "The Bangalore office is at WeWork Embassy Tech Village, 5th Floor.",
        "The Mumbai office is at Worli Business District, Tower A, 12th Floor.",
        "Our tech stack includes Python (FastAPI), React, PostgreSQL, and AWS.",
        "Laptops are provided by the company and replaced every 3 years.",
        "Maternity leave is 26 weeks as per government regulations.",
    ],
    metadatas=[
        {"category": "leave", "source": "handbook.pdf", "page": 5},
        {"category": "leave", "source": "handbook.pdf", "page": 5},
        {"category": "wfh", "source": "handbook.pdf", "page": 8},
        {"category": "expense", "source": "handbook.pdf", "page": 12},
        {"category": "expense", "source": "handbook.pdf", "page": 12},
        {"category": "office", "source": "handbook.pdf", "page": 15},
        {"category": "office", "source": "handbook.pdf", "page": 15},
        {"category": "tech", "source": "tech-guide.pdf", "page": 3},
        {"category": "tech", "source": "tech-guide.pdf", "page": 7},
        {"category": "leave", "source": "handbook.pdf", "page": 6},
    ],
    ids=[f"doc{i}" for i in range(10)],
)
print(f"Added {collection.count()} documents")

# Basic search
print("\n--- Similarity Search ---")
results = collection.query(query_texts=["How many holidays do I get?"], n_results=3)
print("Query: 'How many holidays do I get?'\n")
for doc, meta, dist in zip(results["documents"][0], results["metadatas"][0], results["distances"][0]):
    print(f"  [{dist:.4f}] {doc}")
    print(f"     Metadata: {meta}\n")

# Filtered search
print("--- Filtered Search (category = 'expense') ---")
results = collection.query(query_texts=["What can I claim?"], n_results=3, where={"category": "expense"})
print("Query: 'What can I claim?' (expense only)\n")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  - {doc}")
    print(f"    Metadata: {meta}\n")

# Multi-filter
print("--- Multi-Filter Search (source = 'tech-guide.pdf') ---")
results = collection.query(query_texts=["What technologies do we use?"], n_results=3, where={"source": "tech-guide.pdf"})
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  - {doc}")
    print(f"    Metadata: {meta}\n")

# TODO 1: Add more documents
collection.add(
    documents=[
        "All employees must use strong passwords with at least 12 characters.",
        "Two-factor authentication is mandatory for accessing company systems.",
        "Report security incidents to security@unigps.in within 24 hours.",
    ],
    metadatas=[
        {"category": "security", "source": "handbook.pdf", "page": 20},
        {"category": "security", "source": "handbook.pdf", "page": 20},
        {"category": "security", "source": "handbook.pdf", "page": 21},
    ],
    ids=["doc10", "doc11", "doc12"],
)
print("--- New docs added ---")
results = collection.query(query_texts=["What are the password rules?"], n_results=3)
for doc in results["documents"][0]:
    print(f"  Found: {doc}")

# TODO 2: $or filter
results = collection.query(
    query_texts=["What are my benefits?"],
    n_results=5,
    where={"$or": [{"category": "leave"}, {"category": "wfh"}]},
)
print("\n--- Leave OR WFH results ---")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  [{meta['category']}] {doc}")

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- ChromaDB stores documents + metadata + embeddings")
print("- Similarity search finds relevant docs even with different words")
print("- Metadata filters let you narrow search by category, source, etc.")
print("- ChromaDB auto-embeds your text (no manual embedding needed)")
