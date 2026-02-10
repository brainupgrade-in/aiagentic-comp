"""
Lab 02: Understanding Embeddings — SOLUTION
"""

from langchain_community.embeddings import HuggingFaceEmbeddings

print("Loading embedding model...")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding model ready!")
print("=" * 50)


def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    return dot / (norm1 * norm2)


# Step 2: Embed a single text
text = "What is the refund policy?"
vector = embeddings.embed_query(text)
print(f"\nText: '{text}'")
print(f"Vector dimensions: {len(vector)}")
print(f"First 10 values: {[round(v, 4) for v in vector[:10]]}")

# Step 3: Compare similar vs different
texts = [
    "What is the refund policy?",
    "How do I return a product?",
    "What is the weather in Mumbai?",
]
vectors = [embeddings.embed_query(t) for t in texts]

print("\n--- Similarity Comparison ---")
print(f"'{texts[0]}'")
print(f"  vs '{texts[1]}'  → similarity: {cosine_similarity(vectors[0], vectors[1]):.4f}")
print(f"  vs '{texts[2]}'  → similarity: {cosine_similarity(vectors[0], vectors[2]):.4f}")

# Step 4: Batch embedding
documents = [
    "Refund within 30 days of purchase",
    "Free shipping on orders above Rs 500",
    "Contact support at help@unigps.in",
    "Return items in original packaging",
]
doc_vectors = embeddings.embed_documents(documents)
print(f"\n--- Batch Embedding ---")
print(f"Embedded {len(doc_vectors)} documents, {len(doc_vectors[0])} dims each")

# Step 5: Find best match
query = "How do I get my money back?"
query_vec = embeddings.embed_query(query)
print(f"\n--- Finding Most Relevant Document ---")
print(f"Query: '{query}'\n")

scores = []
for doc, doc_vec in zip(documents, doc_vectors):
    sim = cosine_similarity(query_vec, doc_vec)
    scores.append((sim, doc))
    print(f"  [{sim:.4f}] {doc}")

best = max(scores, key=lambda x: x[0])
print(f"\nBest match: '{best[1]}' (score: {best[0]:.4f})")

# TODO 1: Custom pairs
pairs = [
    ("Python is a programming language", "Python is a snake"),
    ("Bangalore weather", "Weather in Bengaluru"),
    ("Machine learning", "Deep learning"),
]
print("\n--- Custom Similarity Pairs ---")
for a, b in pairs:
    va = embeddings.embed_query(a)
    vb = embeddings.embed_query(b)
    sim = cosine_similarity(va, vb)
    print(f"  [{sim:.4f}] '{a}' vs '{b}'")

# TODO 2: Mini search engine
my_docs = [
    "How to set up a Docker container for Python",
    "Kubernetes pod networking explained",
    "FastAPI tutorial for beginners",
    "PostgreSQL performance tuning tips",
    "React component lifecycle methods",
]
print("\n--- Mini Search Engine ---")
my_query = "I want to learn web development with Python"
my_doc_vecs = embeddings.embed_documents(my_docs)
my_query_vec = embeddings.embed_query(my_query)
print(f"Query: '{my_query}'\n")
for doc, vec in zip(my_docs, my_doc_vecs):
    sim = cosine_similarity(my_query_vec, vec)
    print(f"  [{sim:.4f}] {doc}")

print("\n" + "=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- Embeddings turn text into vectors that capture meaning")
print("- Similar meaning → similar vectors (high cosine similarity)")
print("- all-MiniLM-L6-v2 runs locally, no API key needed")
print("- This is the foundation of RAG's similarity search!")
