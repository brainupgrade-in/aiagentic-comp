"""
Lab 03: ChromaDB Basics
========================
Goal: Learn ChromaDB — create collections, add documents with metadata,
      and run similarity searches.

What you'll learn:
- How to create a ChromaDB client and collection
- How to add documents with metadata (source, page, category)
- How to query documents by similarity
- How to filter queries using metadata
"""

import chromadb

# ============================================================
# Step 1: Create a ChromaDB client
# ============================================================
# ChromaDB can run in-memory (for experiments) or persistent (for production).
# We'll use in-memory for this lab — fast and no cleanup needed.

client = chromadb.Client()  # In-memory client
print("ChromaDB client ready!")
print("=" * 50)

# ============================================================
# Step 2: Create a collection
# ============================================================
# A collection is like a table in SQL — it holds related documents.
# ChromaDB automatically embeds your text when you add documents.

collection = client.get_or_create_collection("company_handbook")
print(f"Collection created: '{collection.name}'")

# ============================================================
# Step 3: Add documents with metadata
# ============================================================
# Each document has: text (document), metadata (key-value pairs), and an ID.
# Metadata lets you filter search results later.

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

print(f"Added {collection.count()} documents to the collection")

# ============================================================
# Step 4: Basic similarity search
# ============================================================
# Ask a question and ChromaDB finds the most similar documents.
# Notice: you don't need to use the exact words from the documents!

print("\n--- Similarity Search ---")
results = collection.query(
    query_texts=["How many holidays do I get?"],
    n_results=3,
)

print("Query: 'How many holidays do I get?'\n")
for i, (doc, meta, dist) in enumerate(zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
)):
    print(f"  {i+1}. [{dist:.4f}] {doc}")
    print(f"     Metadata: {meta}\n")

# ============================================================
# Step 5: Search with metadata filter
# ============================================================
# Combine similarity search with metadata filters for precise results.
# "Find expense-related info only"

print("--- Filtered Search (category = 'expense') ---")
results = collection.query(
    query_texts=["What can I claim?"],
    n_results=3,
    where={"category": "expense"},
)

print("Query: 'What can I claim?' (filtered to expense category)\n")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  - {doc}")
    print(f"    Metadata: {meta}\n")

# ============================================================
# Step 6: Search with multiple filters
# ============================================================
# Use $and / $or operators for complex filters.

print("--- Multi-Filter Search (source = 'tech-guide.pdf') ---")
results = collection.query(
    query_texts=["What technologies do we use?"],
    n_results=3,
    where={"source": "tech-guide.pdf"},
)

print("Query: 'What technologies do we use?' (from tech-guide.pdf only)\n")
for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print(f"  - {doc}")
    print(f"    Metadata: {meta}\n")

# ============================================================
# TODO 1: Add more documents and search
# ============================================================
# Add 3-4 new documents about a topic of your choice.
# Suggestions: security policies, meeting rules, dress code.
# Then query for them and see if ChromaDB finds them.

# TODO: Uncomment and modify
# collection.add(
#     documents=[
#         "YOUR DOCUMENT 1",
#         "YOUR DOCUMENT 2",
#         "YOUR DOCUMENT 3",
#     ],
#     metadatas=[
#         {"category": "YOUR_CATEGORY", "source": "handbook.pdf", "page": 20},
#         {"category": "YOUR_CATEGORY", "source": "handbook.pdf", "page": 20},
#         {"category": "YOUR_CATEGORY", "source": "handbook.pdf", "page": 21},
#     ],
#     ids=["doc10", "doc11", "doc12"],
# )
# results = collection.query(query_texts=["YOUR QUERY"], n_results=3)
# for doc in results["documents"][0]:
#     print(f"  Found: {doc}")

# ============================================================
# TODO 2: Try the $or filter
# ============================================================
# Search across multiple categories at once.
# Find documents that are either "leave" OR "wfh" related.

# TODO: Uncomment and try
# results = collection.query(
#     query_texts=["What are my benefits?"],
#     n_results=5,
#     where={"$or": [{"category": "leave"}, {"category": "wfh"}]},
# )
# print("\nLeave OR WFH results:")
# for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
#     print(f"  [{meta['category']}] {doc}")

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- ChromaDB stores documents + metadata + embeddings")
print("- Similarity search finds relevant docs even with different words")
print("- Metadata filters let you narrow search by category, source, etc.")
print("- ChromaDB auto-embeds your text (no manual embedding needed)")
