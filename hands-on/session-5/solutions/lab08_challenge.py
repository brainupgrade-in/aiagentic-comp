"""
Lab 08: Challenge — Build a Company Q&A Bot — SOLUTION
"""

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

print("=" * 50)
print("  Company Q&A Bot — SOLUTION")
print("=" * 50)

COMPANY_DOCS = [
    {
        "text": """UniGPS Leave Policy (Updated January 2025)

Annual Leave: All full-time employees receive 24 days of annual leave per year. Leave must be applied for at least 3 working days in advance through the HR portal. Unused annual leave cannot be carried forward to the next financial year. Employees with less than 6 months tenure receive prorated leave.

Sick Leave: 12 days per year. Employees must notify their manager by 10 AM on the day of absence. For absences exceeding 2 consecutive days, a medical certificate from a registered medical practitioner is mandatory. Unused sick leave can be carried forward up to a maximum of 30 days.

Maternity Leave: 26 weeks of paid leave as per the Maternity Benefit Act. This can be taken up to 8 weeks before the expected delivery date. Applicable after 80 days of continuous employment.

Paternity Leave: 2 weeks of paid leave. Must be taken within 6 months of the child's birth. Apply at least 15 days in advance.""",
        "source": "leave-policy.pdf",
        "category": "leave"
    },
    {
        "text": """UniGPS Work From Home Policy

Eligibility: All employees who have completed their probation period (6 months) are eligible for WFH. New employees must work from office for the first 6 months.

Schedule: Up to 3 days per week with team lead approval. Core hours are 10 AM to 4 PM IST — you must be available on Slack and email during these hours. Friday is a mandatory in-office day for all teams.

Equipment: Company-provided laptop must be used. VPN connection is mandatory for accessing internal systems. Contact IT helpdesk (it@unigps.in) for VPN setup.

Reimbursement: Internet allowance of Rs 1,500 per month. Ergonomic chair reimbursement up to Rs 10,000 (one-time). Submit receipts to finance@unigps.in by the 5th of each month.""",
        "source": "wfh-policy.pdf",
        "category": "wfh"
    },
    {
        "text": """UniGPS Expense Policy

Travel: All business travel must be pre-approved by your manager. Expenses must be submitted with original receipts within 7 working days of travel completion. Economy class flights for domestic travel; business class allowed for international flights over 6 hours.

Meals: Meal allowance is Rs 500 per day during client visits within India. Rs 3,000 per day for international travel. Team dinners up to Rs 1,000 per person with manager approval.

Equipment: Laptops provided by company, replaced every 3 years. External monitors (up to Rs 15,000), keyboards, and mice can be requested through IT. Software licenses must be requested through the IT helpdesk — do NOT purchase independently.

Communication: Mobile reimbursement of Rs 1,000 per month for roles requiring client communication. Provide monthly bill to finance.""",
        "source": "expense-policy.pdf",
        "category": "expense"
    },
    {
        "text": """UniGPS Technology Stack Guide

Backend: Primary languages are Python (using FastAPI framework) and Java (using Spring Boot). New microservices should use Python unless there's a specific reason for Java. All APIs must follow RESTful conventions.

Frontend: React is the standard for new projects. Angular is maintained for existing applications (UniGPS dashboard, Admin portal). TypeScript is mandatory for all frontend code.

Database: PostgreSQL is the primary relational database. MongoDB for document storage where schema flexibility is needed. Redis for caching and session management.

Cloud & Infrastructure: AWS is our primary cloud provider. All services run on EKS (Kubernetes). Docker is used for containerization. Terraform for infrastructure as code. CI/CD through GitHub Actions.

Monitoring: LangFuse for LLM tracing and metrics. PagerDuty for alerts.""",
        "source": "tech-guide.pdf",
        "category": "tech"
    },
    {
        "text": """UniGPS Office Directory

Bangalore (Headquarters): WeWork Embassy Tech Village, Outer Ring Road, 5th Floor. 200+ employees. All departments represented. Cafeteria on 3rd floor. Gym membership included. Parking available in basement (apply through admin). Office hours: 9 AM to 6 PM, Monday to Friday.

Mumbai: Worli Business District, Tower A, 12th Floor. 50 employees. Primarily sales, client success, and marketing teams. Sea-facing meeting rooms available for client presentations.

Hyderabad: HITEC City, Cyber Gateway, 8th Floor. 80 employees. Engineering hub for backend services and data engineering. 24/7 access for oncall engineers.

Pune: Hinjewadi Phase 2, Building C, 4th Floor. 40 employees. QA, DevOps, and SRE teams. Lab environment for performance testing available.

All offices have high-speed internet, meeting rooms (book via Outlook), and free tea/coffee. Report facility issues to admin@unigps.in.""",
        "source": "office-directory.pdf",
        "category": "office"
    },
]

# PART A: Build the knowledge base
docs = []
for d in COMPANY_DOCS:
    docs.append(Document(
        page_content=d["text"],
        metadata={"source": d["source"], "category": d["category"]}
    ))

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=50)
chunks = splitter.split_documents(docs)
print(f"Split {len(docs)} documents into {len(chunks)} chunks")

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings)
print(f"Vector store ready: {vectorstore._collection.count()} chunks")

# PART B: RAG chain with citations
def format_docs(docs):
    return "\n\n".join(
        f"[{d.metadata['source']}]\n{d.page_content}" for d in docs
    )

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
llm = ChatGroq(model="llama-3.3-70b-versatile")

prompt = ChatPromptTemplate.from_template("""You are UniGPS's AI assistant.
Answer using ONLY the context. Cite sources in parentheses.
If unsure, say "I don't have that information."

Context:
{context}

Question: {question}
Answer:""")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

# PART C: Test questions
test_questions = [
    "How many days of sick leave do I get?",
    "Can a new employee work from home?",
    "How much is the meal allowance abroad?",
    "What programming language should I use for a new microservice?",
    "Where is the Hyderabad office?",
    "How do I get a new monitor?",
    "What is the company's stock price?",
]

print("\n--- Testing Q&A Bot ---")
for q in test_questions:
    print(f"\nQ: {q}")
    print(f"A: {rag_chain.invoke(q)}")

# PART D: Category-specific chains
hr_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3, "filter": {"category": "leave"}}
)
hr_chain = (
    {"context": hr_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

tech_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3, "filter": {"category": "tech"}}
)
tech_chain = (
    {"context": tech_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt | llm | StrOutputParser()
)

print("\n--- HR-only chain ---")
print(f"Q: What leave options do new mothers have?")
print(f"A: {hr_chain.invoke('What leave options do new mothers have?')}")

print("\n--- Tech-only chain ---")
print(f"Q: What database should I use for a new project?")
print(f"A: {tech_chain.invoke('What database should I use for a new project?')}")

# PART F: Answer with sources
print("\n--- Answer with Sources ---")


def get_answer_with_sources(question):
    docs = retriever.invoke(question)
    context = format_docs(docs)
    answer = (prompt | llm | StrOutputParser()).invoke(
        {"context": context, "question": question}
    )
    return {
        "answer": answer,
        "sources": [
            {"source": d.metadata["source"], "text": d.page_content[:100]}
            for d in docs
        ]
    }


result = get_answer_with_sources("What is the WFH policy?")
print(f"\nAnswer: {result['answer']}")
print(f"\nSources used:")
for s in result["sources"]:
    print(f"  - [{s['source']}] {s['text']}...")

# PART E: Interactive mode
print("\n" + "=" * 50)
print("Interactive Q&A — type 'quit' to exit")
print("=" * 50)

while True:
    question = input("\nYour question: ").strip()
    if question.lower() in ("quit", "exit", "q"):
        break
    if not question:
        continue

    print("\nSearching knowledge base...")
    result = get_answer_with_sources(question)
    print(f"\nAnswer: {result['answer']}")
    print(f"\nSources:")
    for s in result["sources"]:
        print(f"  - [{s['source']}] {s['text'][:80]}...")
