"""
Lab 02: Understanding Embeddings
=================================
Goal: Learn what embeddings are by generating them, comparing them, and seeing
      how similar meaning produces similar vectors.

What you'll learn:
- How to create an embedding model with HuggingFaceEmbeddings
- What an embedding vector looks like (list of numbers)
- How cosine similarity measures meaning closeness
- Why embeddings are the foundation of RAG
"""

from langchain_community.embeddings import HuggingFaceEmbeddings

# ============================================================
# Step 1: Create an embedding model
# ============================================================
# all-MiniLM-L6-v2 is a small, fast model (80 MB) that runs locally.
# No API key needed — it runs on your machine.
# It produces 384-dimensional vectors.

print("Loading embedding model (first time may take a minute to download)...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding model ready!")
print("=" * 50)

# ============================================================
# Step 2: Embed a single text
# ============================================================
# embed_query() converts text into a vector (list of numbers).
# Each number represents one dimension of meaning.

text = "What is the refund policy?"
vector = embeddings.embed_query(text)

print(f"\nText: '{text}'")
print(f"Vector dimensions: {len(vector)}")
print(f"First 10 values: {[round(v, 4) for v in vector[:10]]}")
print(f"(Each value is a float representing one aspect of meaning)")

# ============================================================
# Step 3: Compare similar vs different texts
# ============================================================
# Similar meaning → similar vectors → high cosine similarity
# Different meaning → different vectors → low cosine similarity


def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors (0 to 1)."""
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    return dot / (norm1 * norm2)


# Embed three texts
texts = [
    "What is the refund policy?",         # query
    "How do I return a product?",          # similar meaning
    "What is the weather in Mumbai?",      # unrelated
]

vectors = [embeddings.embed_query(t) for t in texts]

print("\n--- Similarity Comparison ---")
sim_similar = cosine_similarity(vectors[0], vectors[1])
sim_different = cosine_similarity(vectors[0], vectors[2])

print(f"'{texts[0]}'")
print(f"  vs '{texts[1]}'  → similarity: {sim_similar:.4f}")
print(f"  vs '{texts[2]}'  → similarity: {sim_different:.4f}")
print(f"\nThe refund/return pair is MUCH more similar — same meaning, different words!")

# ============================================================
# Step 4: Embed multiple documents at once
# ============================================================
# embed_documents() is optimized for batches of text.

documents = [
    "Refund within 30 days of purchase",
    "Free shipping on orders above Rs 500",
    "Contact support at help@unigps.in",
    "Return items in original packaging",
]

doc_vectors = embeddings.embed_documents(documents)
print(f"\n--- Batch Embedding ---")
print(f"Embedded {len(doc_vectors)} documents")
print(f"Each vector has {len(doc_vectors[0])} dimensions")

# ============================================================
# Step 5: Find the most relevant document
# ============================================================
# Given a query, find which document is most similar.
# This is exactly what a vector store does internally!

query = "How do I get my money back?"
query_vec = embeddings.embed_query(query)

print(f"\n--- Finding Most Relevant Document ---")
print(f"Query: '{query}'\n")

scores = []
for i, (doc, doc_vec) in enumerate(zip(documents, doc_vectors)):
    sim = cosine_similarity(query_vec, doc_vec)
    scores.append((sim, doc))
    print(f"  [{sim:.4f}] {doc}")

best = max(scores, key=lambda x: x[0])
print(f"\nBest match: '{best[1]}' (score: {best[0]:.4f})")

# ============================================================
# TODO 1: Test with your own similar/different pairs
# ============================================================
# Try embedding pairs of sentences and check their similarity.
# Suggestions:
#   - "Python is a programming language" vs "Python is a snake"
#   - "Bangalore weather" vs "Weather in Bengaluru"
#   - "Machine learning" vs "Deep learning"

# TODO: Uncomment and modify
# text_a = "YOUR TEXT A"
# text_b = "YOUR TEXT B"
# vec_a = embeddings.embed_query(text_a)
# vec_b = embeddings.embed_query(text_b)
# sim = cosine_similarity(vec_a, vec_b)
# print(f"\n'{text_a}' vs '{text_b}' → {sim:.4f}")

# ============================================================
# TODO 2: Build a mini search engine
# ============================================================
# Add more documents and find the best match for a query.
# Try adding documents about different topics and see which
# ones the search finds most relevant.

# TODO: Add your own documents and query
# my_docs = [
#     "YOUR DOCUMENT 1",
#     "YOUR DOCUMENT 2",
#     "YOUR DOCUMENT 3",
# ]
# my_query = "YOUR SEARCH QUERY"
# my_doc_vecs = embeddings.embed_documents(my_docs)
# my_query_vec = embeddings.embed_query(my_query)
# for doc, vec in zip(my_docs, my_doc_vecs):
#     sim = cosine_similarity(my_query_vec, vec)
#     print(f"  [{sim:.4f}] {doc}")

print("\n" + "=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- Embeddings turn text into vectors that capture meaning")
print("- Similar meaning → similar vectors (high cosine similarity)")
print("- all-MiniLM-L6-v2 runs locally, no API key needed")
print("- This is the foundation of RAG's similarity search!")
