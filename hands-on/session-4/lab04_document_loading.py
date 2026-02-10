"""
Lab 04: Document Loading & Splitting
======================================
Goal: Learn how to load documents and split them into chunks suitable
      for embedding and storage in a vector store.

What you'll learn:
- How to use LangChain's TextLoader and document objects
- How RecursiveCharacterTextSplitter works
- Why chunk size and overlap matter
- How to prepare documents for a RAG pipeline
"""

import os
import tempfile
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# ============================================================
# Step 1: Understand the Document object
# ============================================================
# In LangChain, a Document has two parts:
#   - page_content: the actual text
#   - metadata: info about the source (file, page, etc.)

doc = Document(
    page_content="Annual leave is 24 days per year for all full-time employees.",
    metadata={"source": "handbook.pdf", "page": 5, "category": "leave"},
)

print("=" * 50)
print("--- Document Object ---")
print(f"Content: {doc.page_content}")
print(f"Metadata: {doc.metadata}")
print(f"Type: {type(doc)}")

# ============================================================
# Step 2: Create sample documents from text
# ============================================================
# For this lab, we'll create a sample text file with company policies.
# In production, you'd load real PDFs, web pages, etc.

SAMPLE_TEXT = """UniGPS Employee Handbook

CHAPTER 1: LEAVE POLICY

Annual leave is 24 days per year for all full-time employees. Leave must be applied for at least 3 days in advance through the internal portal. Unused annual leave cannot be carried forward to the next financial year.

Sick leave is 12 days per year. Employees must inform their manager by 10 AM on the day of sick leave. A medical certificate is required for absences exceeding 2 consecutive days.

Maternity leave is 26 weeks as per government regulations. Paternity leave is 2 weeks. Both must be applied for at least 30 days before the expected date.

CHAPTER 2: WORK FROM HOME

Employees can work from home up to 3 days per week with team lead approval. Core hours are 10 AM to 4 PM IST — you must be available during this window.

VPN connection is mandatory for accessing internal systems from home. Monthly in-office day is the first Monday of every month for all teams.

Internet reimbursement of Rs 1,500 per month is provided for WFH employees. Submit your broadband bill to the finance team by the 5th of each month.

CHAPTER 3: EXPENSE REIMBURSEMENT

Travel expenses must be submitted with original receipts within 7 days of travel completion. Meal allowance during client visits is Rs 500 per day.

Hardware (laptops, monitors) is provided by the company. Laptops are replaced every 3 years. Software license requests should be submitted through the IT helpdesk.

CHAPTER 4: OFFICE LOCATIONS

Bangalore: WeWork Embassy Tech Village, 5th Floor. This is our headquarters with 200+ employees.
Mumbai: Worli Business District, Tower A, 12th Floor. Client-facing teams are primarily based here.
Hyderabad: HITEC City, Cyber Gateway, 8th Floor. Engineering hub for backend services.
Pune: Hinjewadi Phase 2, Building C. QA and DevOps teams are based here.

All offices operate Monday to Friday, 9 AM to 6 PM."""

# Write to a temp file so we can use TextLoader
tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
tmp.write(SAMPLE_TEXT)
tmp.close()

# ============================================================
# Step 3: Load with TextLoader
# ============================================================
# TextLoader reads a text file and returns a list of Document objects.

loader = TextLoader(tmp.name)
docs = loader.load()

print(f"\n--- TextLoader ---")
print(f"Loaded {len(docs)} document(s)")
print(f"Total characters: {len(docs[0].page_content)}")
print(f"Metadata: {docs[0].metadata}")
print(f"First 100 chars: {docs[0].page_content[:100]}...")

# ============================================================
# Step 4: Split into chunks
# ============================================================
# A single big document is too large for good embeddings.
# RecursiveCharacterTextSplitter breaks it into smaller, focused chunks.

splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,      # max characters per chunk
    chunk_overlap=50,    # overlap between adjacent chunks
    separators=["\n\n", "\n", " ", ""],  # split priority
)

chunks = splitter.split_documents(docs)

print(f"\n--- Text Splitting ---")
print(f"Original: 1 document, {len(docs[0].page_content)} characters")
print(f"After splitting: {len(chunks)} chunks")
print(f"Chunk size range: {min(len(c.page_content) for c in chunks)}-{max(len(c.page_content) for c in chunks)} characters")

print(f"\n--- First 3 Chunks ---")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1} ({len(chunk.page_content)} chars):")
    print(f"  '{chunk.page_content[:80]}...'")

# ============================================================
# Step 5: See the effect of chunk_overlap
# ============================================================
# Overlap ensures context isn't lost at chunk boundaries.
# Look at where one chunk ends and the next begins.

print(f"\n--- Overlap Demonstration ---")
if len(chunks) >= 2:
    end_of_first = chunks[0].page_content[-60:]
    start_of_second = chunks[1].page_content[:60]
    print(f"End of chunk 1:   '...{end_of_first}'")
    print(f"Start of chunk 2: '{start_of_second}...'")
    print("(Notice the overlapping text that appears in both chunks)")

# ============================================================
# Step 6: Compare different chunk sizes
# ============================================================
# Smaller chunks = more precise search, but less context per result.
# Larger chunks = more context, but search may be less focused.

for size in [200, 500, 1000]:
    s = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=50)
    c = s.split_documents(docs)
    print(f"\n  chunk_size={size:>4} → {len(c):>2} chunks (avg {sum(len(x.page_content) for x in c) // len(c)} chars each)")

# Clean up temp file
os.unlink(tmp.name)

# ============================================================
# TODO 1: Split with different overlap values
# ============================================================
# Try chunk_overlap = 0 (no overlap) vs 100 (lots of overlap).
# Compare the number of chunks and look at the boundaries.

# TODO: Uncomment and experiment
# for overlap in [0, 50, 100]:
#     s = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=overlap)
#     c = s.split_text(SAMPLE_TEXT)
#     print(f"\n  overlap={overlap:>3} → {len(c)} chunks")

# ============================================================
# TODO 2: Create documents from your own text
# ============================================================
# Create a list of Document objects from any text you like.
# Add meaningful metadata (source, topic, date, etc.).

# TODO: Create your own documents
# my_docs = [
#     Document(page_content="YOUR TEXT", metadata={"source": "my_doc", "topic": "example"}),
#     Document(page_content="ANOTHER TEXT", metadata={"source": "my_doc", "topic": "example"}),
# ]
# my_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
# my_chunks = my_splitter.split_documents(my_docs)
# print(f"\nYour docs: {len(my_docs)} docs → {len(my_chunks)} chunks")
# for c in my_chunks:
#     print(f"  [{c.metadata}] {c.page_content[:60]}...")

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- Document = page_content + metadata")
print("- TextLoader reads files into Document objects")
print("- RecursiveCharacterTextSplitter breaks text into focused chunks")
print("- chunk_size controls precision vs context trade-off")
print("- chunk_overlap prevents losing context at boundaries")
