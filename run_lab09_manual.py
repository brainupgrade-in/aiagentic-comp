#!/usr/bin/env python3
"""
Execute Lab 09 with manual LangFuse trace creation
"""
import os
import time
import random
from datetime import datetime
from typing import TypedDict, Annotated, Optional
from operator import add
from dotenv import load_dotenv

load_dotenv()

from langfuse import Langfuse
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# Initialize LangFuse
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

print("=" * 80)
print("LangFuse Initialized")
print("=" * 80)
print()

# Setup LangGraph Agent
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class SupportState(TypedDict):
    request: str
    employee_name: str
    category: str
    worker_output: str
    error: str
    final_response: str
    audit: Annotated[list, add]
    trace_id: Optional[str]

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@company.com.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@company.com with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

def supervisor(state: SupportState) -> dict:
    prompt = f"Classify as: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "error": "", "audit": [f"Supervisor: classified as {cat}"]}

def worker(state: SupportState) -> dict:
    prompt = f"You are {state['category']} support.\nRequest: {state['request']}\nReply helpfully in 2 sentences."
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "", "audit": [f"Worker ({state['category']}) responded"]}
    except Exception as e:
        return {"worker_output": TEMPLATES.get(state["category"], TEMPLATES["general"]), "error": str(e), "audit": [f"Worker error, used template"]}

def finalize(state: SupportState) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS Support | {ts}", "audit": [f"Finalized at {ts}"]}

graph = StateGraph(SupportState)
graph.add_node("supervisor", supervisor)
graph.add_node("worker", worker)
graph.add_node("finalize", finalize)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_edge("worker", "finalize")
graph.add_edge("finalize", END)
agent = graph.compile()

print("✓ Agent compiled\n")

# Handler with manual tracing using propagate_attributes
def handle_support_request(employee_name: str, request: str, session_id: str):
    """Handle support request with manual LangFuse tracing."""
    from langfuse import propagate_attributes

    # Use propagate_attributes to set user_id and session_id for all nested observations
    with propagate_attributes(user_id=employee_name, session_id=session_id):
        # Create an observation (generation type)
        observation = langfuse.start_observation(
            as_type="generation",
            name="support_request",
            input={"employee": employee_name, "request": request},
            metadata={
                "endpoint": "/api/support",
                "tags": ["production", "support"],
            }
        )

        # Invoke agent
        result = agent.invoke({
            "request": request,
            "employee_name": employee_name,
            "category": "",
            "worker_output": "",
            "error": "",
            "final_response": "",
            "audit": [],
            "trace_id": None,
        })

        # Update observation with output
        observation.update(
            output={"category": result["category"], "response": result["final_response"]}
        )

        # End observation
        observation.end()

    return result

print("=" * 80)
print("Generating Test Data")
print("=" * 80)
print()

trace_count = 0

# Test 1-2: Basic requests
print("Basic Requests:")
result = handle_support_request("Priya", "I need to apply for sick leave", "test-session-001")
trace_count += 1
print(f"  ✓ Priya: {result['category']}")

result = handle_support_request("Vikram", "My VPN keeps disconnecting", "test-session-002")
trace_count += 1
print(f"  ✓ Vikram: {result['category']}")
print()

# Test 3: Category diversity
print("Category Diversity:")
for emp, req, sess in [
    ("Anjali", "I need to update my emergency contact information", "session-hr-001"),
    ("Rohan", "I can't access the shared drive", "session-tech-001"),
    ("Sneha", "When will I receive my travel reimbursement?", "session-finance-001"),
    ("Arjun", "Where is the cafeteria located?", "session-general-001"),
]:
    result = handle_support_request(emp, req, sess)
    trace_count += 1
    print(f"  ✓ {emp}: {result['category']}")
print()

# Test 4: Load testing
print("Load Testing (20 requests):")
employees = ["Amit", "Kavya", "Ravi", "Meera", "Sanjay", "Divya", "Karan", "Pooja", "Nikhil", "Isha"]
hr_requests = ["maternity leave", "salary slip", "performance review", "benefits enrollment"]
tech_requests = ["password reset", "VPN issues", "laptop upgrade", "software installation"]
finance_requests = ["expense approval", "invoice query", "budget allocation", "reimbursement status"]
general_requests = ["parking pass", "office supplies", "meeting room booking", "visitor access"]

all_requests = (
    [(emp, f"I need help with {req}", "hr") for emp in employees[:5] for req in random.sample(hr_requests, 2)][:5] +
    [(emp, f"Issue: {req}", "tech") for emp in employees[5:] for req in random.sample(tech_requests, 2)][:5] +
    [(emp, f"Question about {req}", "finance") for emp in employees[:5] for req in random.sample(finance_requests, 2)][:5] +
    [(emp, f"Help needed: {req}", "general") for emp in employees[5:] for req in random.sample(general_requests, 2)][:5]
)

for i, (emp, req, cat) in enumerate(all_requests):
    handle_support_request(emp, req, f"load-test-{i % 5}")
    trace_count += 1
    if (i + 1) % 5 == 0:
        print(f"  ✓ Processed {i + 1}/20")
print()

# Test 5: Multi-turn sessions
print("Multi-Turn Sessions:")
for emp, sess, requests in [
    ("Priya", "priya-session-multi", ["I need to request vacation days", "What is the approval process for vacation?", "Can I see my remaining leave balance?"]),
    ("Vikram", "vikram-session-multi", ["My laptop is running slow", "I've tried restarting but it's still slow", "Can someone from IT help me?"]),
    ("Sanjana", "sanjana-session-multi", ["I submitted an expense report last week", "When will it be processed?", "I need the reimbursement urgently"]),
]:
    print(f"  👤 {emp} ({sess})")
    for req in requests:
        handle_support_request(emp, req, sess)
        trace_count += 1
print()

# Flush
langfuse.flush()
time.sleep(3)

print("=" * 80)
print(f"✅ Generated {trace_count} traces")
print("=" * 80)
print()
print("🌐 View at: https://cloud.langfuse.com")
print()
