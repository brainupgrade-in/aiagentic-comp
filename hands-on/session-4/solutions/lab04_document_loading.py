"""
Lab 04: Document Loading & Splitting — SOLUTION
"""

import os
import tempfile
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Step 1: Document object
doc = Document(
    page_content="Annual leave is 24 days per year for all full-time employees.",
    metadata={"source": "handbook.pdf", "page": 5, "category": "leave"},
)
print("=" * 50)
print(f"Content: {doc.page_content}")
print(f"Metadata: {doc.metadata}")

# Step 2: Sample text
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

tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False)
tmp.write(SAMPLE_TEXT)
tmp.close()

# Step 3: TextLoader
loader = TextLoader(tmp.name)
docs = loader.load()
print(f"\n--- TextLoader ---")
print(f"Loaded {len(docs)} document(s), {len(docs[0].page_content)} chars")

# Step 4: Split
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"\n--- Text Splitting ---")
print(f"Original: 1 doc, {len(docs[0].page_content)} chars → {len(chunks)} chunks")

for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1} ({len(chunk.page_content)} chars): '{chunk.page_content[:80]}...'")

# Step 5: Overlap demo
if len(chunks) >= 2:
    print(f"\n--- Overlap ---")
    print(f"End of chunk 1:   '...{chunks[0].page_content[-60:]}'")
    print(f"Start of chunk 2: '{chunks[1].page_content[:60]}...'")

# Step 6: Compare sizes
for size in [200, 500, 1000]:
    s = RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=50)
    c = s.split_documents(docs)
    print(f"\n  chunk_size={size:>4} → {len(c):>2} chunks (avg {sum(len(x.page_content) for x in c) // len(c)} chars)")

os.unlink(tmp.name)

# TODO 1: Different overlaps
print("\n--- Overlap comparison ---")
for overlap in [0, 50, 100]:
    s = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=overlap)
    c = s.split_text(SAMPLE_TEXT)
    print(f"  overlap={overlap:>3} → {len(c)} chunks")

# TODO 2: Custom documents
my_docs = [
    Document(page_content="Python is great for web development and data science.", metadata={"source": "blog", "topic": "python"}),
    Document(page_content="Docker containers package applications with all their dependencies.", metadata={"source": "blog", "topic": "devops"}),
]
my_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)
my_chunks = my_splitter.split_documents(my_docs)
print(f"\nCustom docs: {len(my_docs)} docs → {len(my_chunks)} chunks")
for c in my_chunks:
    print(f"  [{c.metadata}] {c.page_content[:60]}...")

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- Document = page_content + metadata")
print("- TextLoader reads files into Document objects")
print("- RecursiveCharacterTextSplitter breaks text into focused chunks")
print("- chunk_size controls precision vs context trade-off")
print("- chunk_overlap prevents losing context at boundaries")
