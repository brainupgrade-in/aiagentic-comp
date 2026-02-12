"""
Lab 08: Challenge — Complete UniGPS Multi-Agent Support System
================================================================
Goal: Build a production-grade multi-agent support system combining
      ALL patterns from this session.

Scenario:
  UniGPS needs a complete support desk system that:
  1. Uses an LLM supervisor to classify and route requests
  2. Has specialized worker agents (HR, Tech, Finance, Facilities)
  3. Supports handoff/escalation when a worker can't handle a request
  4. Aggregates results for multi-domain requests
  5. Implements fallback chains for reliability
  6. Tracks everything in an audit trail
  7. Uses checkpointing for conversation persistence

Requires: GROQ_API_KEY in .env
"""

import os
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 60)
print("  Challenge: UniGPS Multi-Agent Support System")
print("=" * 60)

# ============================================================
# YOUR TASK: Build the complete multi-agent system
# ============================================================
#
# State definition (provided):

class SupportRequest(TypedDict):
    # Input
    employee_name: str
    request: str
    # Routing
    category: str               # hr, tech, finance, facilities, general
    confidence: int             # 1-10 from LLM classifier
    # Processing
    worker_output: str
    needs_escalation: bool
    escalation_reason: str
    # Fallback
    error: str
    fallback_used: bool
    # Output
    final_response: str
    # Tracking
    audit: Annotated[list, add]

#
# Requirements:
#
# 1. LLM SUPERVISOR (router)
#    - Classify request into: hr, tech, finance, facilities, general
#    - Include confidence score (1-10)
#    - If confidence < 5, route to "clarify" agent
#    - Handle LLM errors gracefully (fallback to "general")
#
# 2. SPECIALIZED WORKERS (4 domain agents)
#    - HR: leave, policies, insurance, onboarding
#    - Tech: servers, laptops, deployments, bugs
#    - Finance: expenses, salary, tax, reimbursement
#    - Facilities: desk, parking, cafeteria, access cards
#    - Each with domain-specific system prompt
#
# 3. ESCALATION
#    - Worker can set needs_escalation=True if request is too complex
#    - Escalation goes to a "manager_agent" node
#    - Manager agent handles with broader authority
#
# 4. FALLBACK CHAIN
#    - Primary (LLM specialist) → Fallback (template) → Error response
#    - QA check: verify output length and quality
#
# 5. AUDIT TRAIL
#    - Every node adds to audit: Annotated[list, add]
#    - Include timestamps in audit entries
#
# 6. CHECKPOINTING
#    - MemorySaver with thread_id per employee
#    - Support conversation history
#
# Graph structure:
#   START → supervisor → [clarify | hr | tech | finance | facilities | general]
#         → [escalation_check] → [manager | qa_check] → [finalize | fallback]
#         → finalize → END

# ============================================================
# YOUR CODE BELOW
# ============================================================

# def supervisor(state: SupportRequest) -> dict:
#     """LLM-powered supervisor with confidence scoring."""
#     prompt = (
#         f"You are the UniGPS support desk supervisor.\n"
#         f"Classify this request into: hr, tech, finance, facilities, general\n"
#         f"Rate your confidence 1-10.\n"
#         f"Request: {state['request']}\n"
#         f"Reply:\nCATEGORY: ...\nCONFIDENCE: ..."
#     )
#     ...

# def route_supervisor(state: SupportRequest) -> str:
#     if state["confidence"] < 5:
#         return "clarify"
#     return state["category"]

# def clarify_agent(state: SupportRequest) -> dict:
#     ...

# def hr_worker(state: SupportRequest) -> dict:
#     ...

# def tech_worker(state: SupportRequest) -> dict:
#     ...

# def finance_worker(state: SupportRequest) -> dict:
#     ...

# def facilities_worker(state: SupportRequest) -> dict:
#     ...

# def general_worker(state: SupportRequest) -> dict:
#     ...

# def escalation_check(state: SupportRequest) -> dict:
#     """Check if the worker flagged for escalation."""
#     ...

# def route_escalation(state: SupportRequest) -> str:
#     return "manager" if state["needs_escalation"] else "qa_check"

# def manager_agent(state: SupportRequest) -> dict:
#     """Manager agent with broader authority."""
#     ...

# def qa_check(state: SupportRequest) -> dict:
#     """Verify response quality."""
#     ...

# def route_qa(state: SupportRequest) -> str:
#     return "fallback" if state["error"] else "finalize"

# def fallback(state: SupportRequest) -> dict:
#     ...

# def finalize(state: SupportRequest) -> dict:
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     ...

# Build graph
# graph = StateGraph(SupportRequest)
# ... add all nodes and edges ...

# memory = MemorySaver()
# app = graph.compile(checkpointer=memory)

# ============================================================
# Test cases (provided):
# ============================================================

test_requests = [
    {
        "employee_name": "Priya Sharma",
        "request": "I want to apply for 5 days casual leave from next Monday",
        "thread_id": "support-001",
    },
    {
        "employee_name": "Vikram Patel",
        "request": "The production database is running very slow and queries are timing out",
        "thread_id": "support-002",
    },
    {
        "employee_name": "Anita Desai",
        "request": "When will my travel expense reimbursement from last month be credited?",
        "thread_id": "support-003",
    },
    {
        "employee_name": "Rahul Kumar",
        "request": "I need a standing desk and a parking spot in the new building",
        "thread_id": "support-004",
    },
    {
        "employee_name": "Meera Joshi",
        "request": "asdfghjkl",
        "thread_id": "support-005",
    },
    {
        "employee_name": "Amit Singh",
        "request": "I need a policy exception for 30 days leave for my wedding",
        "thread_id": "support-006",
    },
]

# Uncomment to test when your implementation is ready:
#
# print("\n--- Processing Support Requests ---\n")
# for req in test_requests:
#     config = {"configurable": {"thread_id": req["thread_id"]}}
#     print(f"{'='*50}")
#     print(f"Employee: {req['employee_name']}")
#     print(f"Request: {req['request']}")
#
#     result = app.invoke({
#         "employee_name": req["employee_name"],
#         "request": req["request"],
#         "category": "", "confidence": 0,
#         "worker_output": "", "needs_escalation": False,
#         "escalation_reason": "", "error": "",
#         "fallback_used": False, "final_response": "",
#         "audit": [],
#     }, config)
#
#     print(f"\n  Category: {result.get('category', 'N/A')}")
#     print(f"  Confidence: {result.get('confidence', 'N/A')}/10")
#     print(f"  Escalated: {result.get('needs_escalation', False)}")
#     print(f"  Fallback: {result.get('fallback_used', False)}")
#     print(f"  Response: {result.get('final_response', 'N/A')[:80]}...")
#     print(f"  Audit trail:")
#     for entry in result.get("audit", []):
#         print(f"    {entry}")
#     print()
#
# # Summary
# print(f"\n{'='*60}")
# print("--- Summary ---")
# print(f"{'Thread':<14} {'Employee':<18} {'Category':<12} {'Escalated'}")
# print("-" * 60)
# for req in test_requests:
#     config = {"configurable": {"thread_id": req["thread_id"]}}
#     snap = app.get_state(config)
#     v = snap.values
#     print(
#         f"{req['thread_id']:<14} "
#         f"{req['employee_name']:<18} "
#         f"{v.get('category', 'N/A'):<12} "
#         f"{v.get('needs_escalation', False)}"
#     )

print("\n" + "=" * 60)
print("Challenge: Implement the complete multi-agent support system")
print("Patterns to use:")
print("  - LLM supervisor with confidence routing")
print("  - 4 specialized domain workers + general")
print("  - Escalation path for complex requests")
print("  - Fallback chain (LLM → template → error message)")
print("  - QA gate before finalizing")
print("  - Audit trail with timestamps")
print("  - MemorySaver checkpointing with thread_id")
print("\nCheck solutions/lab08_challenge.py when done!")
