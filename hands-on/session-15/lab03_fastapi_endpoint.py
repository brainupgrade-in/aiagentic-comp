#!/usr/bin/env python3
"""
Lab 03: Create FastAPI Endpoint

Write FastAPI endpoint code for the capstone support agent application:
health check, POST /api/support, and GET /api/tickets. Code is written
as strings and validated for required keywords and structure.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-03"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- FastAPI Application Structure
# ============================================================================

print("=" * 70)
print("STEP 1: FastAPI Application Structure for AI Agents")
print("=" * 70)
print()
print("  A production FastAPI app for an AI agent typically has:")
print()
print("  +------------------------+----------------------------------------+")
print("  | Endpoint               | Purpose                                |")
print("  +------------------------+----------------------------------------+")
print("  | GET  /healthz          | Liveness probe (K8s)                   |")
print("  | GET  /readyz           | Readiness probe (K8s)                  |")
print("  | POST /api/support      | Submit a support question to agent     |")
print("  | GET  /api/tickets      | List support tickets                   |")
print("  | GET  /api/tickets/{id} | Get a specific ticket                  |")
print("  | GET  /metrics          | Prometheus metrics                     |")
print("  +------------------------+----------------------------------------+")
print()
print("  Response models use Pydantic BaseModel for validation:")
print()
print('    class SupportRequest(BaseModel):')
print('        question: str')
print('        customer_email: str | None = None')
print('        session_id: str | None = None')
print()
print('    class SupportResponse(BaseModel):')
print('        answer: str')
print('        ticket_id: str | None = None')
print('        confidence: float')
print('        sources: list[str]')
print()

# ============================================================================
# STEP 2 -- Error Handling Patterns
# ============================================================================

print("=" * 70)
print("STEP 2: Error Handling Patterns in FastAPI")
print("=" * 70)
print()
print("  Production error handling uses HTTPException with proper codes:")
print()
print("  +------+---------------------------+---------------------------+")
print("  | Code | When                      | Example                   |")
print("  +------+---------------------------+---------------------------+")
print("  | 400  | Invalid request body      | Missing required field    |")
print("  | 404  | Resource not found        | Ticket ID doesn't exist   |")
print("  | 422  | Validation error          | Wrong field type          |")
print("  | 429  | Rate limit exceeded       | Too many LLM calls        |")
print("  | 500  | Internal server error     | LLM API failure           |")
print("  | 503  | Service unavailable       | ChromaDB down             |")
print("  +------+---------------------------+---------------------------+")
print()

# ============================================================================
# TODO 1 -- Write Health Check Endpoint Code
# ============================================================================

print("=" * 70)
print("TODO 1: Write the health check endpoint code")
print("=" * 70)
print()

# TODO: Replace "___" with a string containing the FastAPI health check code.
# The code should define two endpoints:
#   GET /healthz - returns {"status": "healthy"}
#   GET /readyz  - returns {"status": "ready", "checks": {"chromadb": "ok", "llm_api": "ok"}}
#
# Required keywords in your code string:
#   @app.get, /healthz, /readyz, status, healthy, ready, chromadb, llm_api
#
# Example:
# health_check_code = '''
# @app.get("/healthz")
# async def healthz():
#     return {"status": "healthy"}
#
# @app.get("/readyz")
# async def readyz():
#     return {"status": "ready", "checks": {"chromadb": "ok", "llm_api": "ok"}}
# '''

health_check_code = "___"

# -- Validate TODO 1 --------------------------------------------------------
total += 1
required_keywords = ["@app.get", "/healthz", "/readyz", "status",
                     "healthy", "ready", "chromadb", "llm_api"]
if isinstance(health_check_code, str) and health_check_code != "___":
    found = [kw for kw in required_keywords if kw in health_check_code]
    if len(found) == len(required_keywords):
        score += 1
        print("[PASS] Health check code contains all required keywords")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_keywords if kw not in health_check_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] health_check_code must be a non-placeholder string")
print()

# ============================================================================
# TODO 2 -- Write Support Endpoint Code
# ============================================================================

print("=" * 70)
print("TODO 2: Write the POST /api/support endpoint code")
print("=" * 70)
print()

# TODO: Replace "___" with a string containing the POST /api/support endpoint.
# The code should:
#   - Define a POST endpoint at /api/support
#   - Accept a SupportRequest body
#   - Return a SupportResponse
#   - Include try/except for error handling
#   - Raise HTTPException with status_code 500 on failure
#
# Required keywords:
#   @app.post, /api/support, SupportRequest, SupportResponse,
#   async def, try, except, HTTPException, status_code
#
# Example:
# support_endpoint_code = '''
# @app.post("/api/support", response_model=SupportResponse)
# async def handle_support(request: SupportRequest):
#     try:
#         answer = await agent.invoke(request.question)
#         return SupportResponse(
#             answer=answer.content,
#             ticket_id=answer.ticket_id,
#             confidence=answer.confidence,
#             sources=answer.sources,
#         )
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# '''

support_endpoint_code = "___"

# -- Validate TODO 2 --------------------------------------------------------
total += 1
required_keywords_2 = ["@app.post", "/api/support", "SupportRequest",
                       "SupportResponse", "async def", "try", "except",
                       "HTTPException", "status_code"]
if isinstance(support_endpoint_code, str) and support_endpoint_code != "___":
    found = [kw for kw in required_keywords_2 if kw in support_endpoint_code]
    if len(found) == len(required_keywords_2):
        score += 1
        print("[PASS] Support endpoint code contains all required keywords")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_keywords_2 if kw not in support_endpoint_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] support_endpoint_code must be a non-placeholder string")
print()

# ============================================================================
# TODO 3 -- Write Tickets Endpoint Code
# ============================================================================

print("=" * 70)
print("TODO 3: Write the GET /api/tickets endpoint code")
print("=" * 70)
print()

# TODO: Replace "___" with a string containing the GET /api/tickets endpoint.
# The code should:
#   - Define a GET endpoint at /api/tickets
#   - Accept optional query params: status (str), limit (int, default 50)
#   - Return a list of ticket dicts
#   - Include a GET /api/tickets/{ticket_id} endpoint for single ticket
#   - Raise HTTPException 404 if ticket not found
#
# Required keywords:
#   @app.get, /api/tickets, ticket_id, status, limit, 404,
#   HTTPException, async def, return
#
# Example:
# tickets_endpoint_code = '''
# @app.get("/api/tickets")
# async def list_tickets(status: str = None, limit: int = 50):
#     tickets = await ticket_store.list(status=status, limit=limit)
#     return tickets
#
# @app.get("/api/tickets/{ticket_id}")
# async def get_ticket(ticket_id: str):
#     ticket = await ticket_store.get(ticket_id)
#     if not ticket:
#         raise HTTPException(status_code=404, detail="Ticket not found")
#     return ticket
# '''

tickets_endpoint_code = "___"

# -- Validate TODO 3 --------------------------------------------------------
total += 1
required_keywords_3 = ["@app.get", "/api/tickets", "ticket_id", "status",
                       "limit", "404", "HTTPException", "async def", "return"]
if isinstance(tickets_endpoint_code, str) and tickets_endpoint_code != "___":
    found = [kw for kw in required_keywords_3 if kw in tickets_endpoint_code]
    if len(found) == len(required_keywords_3):
        score += 1
        print("[PASS] Tickets endpoint code contains all required keywords")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_keywords_3 if kw not in tickets_endpoint_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] tickets_endpoint_code must be a non-placeholder string")
print()

# ============================================================================
# TODO 4 -- Write Response Model Definitions
# ============================================================================

print("=" * 70)
print("TODO 4: Write the Pydantic response model definitions")
print("=" * 70)
print()

# TODO: Replace "___" with a string defining the Pydantic models.
# Define three models:
#   SupportRequest: question (str), customer_email (str, optional), session_id (str, optional)
#   SupportResponse: answer (str), ticket_id (str, optional), confidence (float), sources (list)
#   TicketModel: id (str), subject (str), status (str), priority (str), created_at (str)
#
# Required keywords:
#   BaseModel, SupportRequest, SupportResponse, TicketModel,
#   question, answer, confidence, sources, priority, created_at
#
# Example:
# response_models_code = '''
# class SupportRequest(BaseModel):
#     question: str
#     customer_email: str | None = None
#     session_id: str | None = None
#
# class SupportResponse(BaseModel):
#     answer: str
#     ticket_id: str | None = None
#     confidence: float
#     sources: list[str]
#
# class TicketModel(BaseModel):
#     id: str
#     subject: str
#     status: str
#     priority: str
#     created_at: str
# '''

response_models_code = "___"

# -- Validate TODO 4 --------------------------------------------------------
total += 1
required_keywords_4 = ["BaseModel", "SupportRequest", "SupportResponse",
                       "TicketModel", "question", "answer", "confidence",
                       "sources", "priority", "created_at"]
if isinstance(response_models_code, str) and response_models_code != "___":
    found = [kw for kw in required_keywords_4 if kw in response_models_code]
    if len(found) == len(required_keywords_4):
        score += 1
        print("[PASS] Response model definitions contain all required keywords")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_keywords_4 if kw not in response_models_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] response_models_code must be a non-placeholder string")
print()

# ============================================================================
# TODO 5 -- Assemble Complete Application Code
# ============================================================================

print("=" * 70)
print("TODO 5: Assemble the complete FastAPI application code")
print("=" * 70)
print()

# TODO: Replace "___" with the complete application code string.
# Combine all pieces into a full app.py file:
#   - Import section (FastAPI, HTTPException, BaseModel)
#   - App initialization: app = FastAPI(title="AI Support Agent", version="1.0.0")
#   - Response models (from TODO 4)
#   - Health endpoints (from TODO 1)
#   - Support endpoint (from TODO 2)
#   - Tickets endpoints (from TODO 3)
#
# Required keywords:
#   from fastapi import, FastAPI, HTTPException, BaseModel,
#   AI Support Agent, 1.0.0, /healthz, /api/support, /api/tickets
#
# Example:
# full_app_code = '''
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import Optional
#
# app = FastAPI(title="AI Support Agent", version="1.0.0")
#
# ''' + response_models_code + health_check_code + support_endpoint_code + tickets_endpoint_code

full_app_code = "___"

# -- Validate TODO 5 --------------------------------------------------------
total += 1
required_keywords_5 = ["from fastapi import", "FastAPI", "HTTPException",
                       "BaseModel", "AI Support Agent", "1.0.0",
                       "/healthz", "/api/support", "/api/tickets"]
if isinstance(full_app_code, str) and full_app_code != "___":
    found = [kw for kw in required_keywords_5 if kw in full_app_code]
    if len(found) == len(required_keywords_5):
        score += 1
        out_path = os.path.join(WORKDIR, "app.py")
        with open(out_path, "w") as f:
            f.write(full_app_code)
        print(f"[PASS] Complete application code saved to {out_path}")
        print(f"       Lines: {len(full_app_code.splitlines())}")
        print(f"       Keywords found: {found}")
    else:
        missing = [kw for kw in required_keywords_5 if kw not in full_app_code]
        print(f"[FAIL] Missing keywords: {missing}")
else:
    print("[FAIL] full_app_code must be a non-placeholder string")
print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 03 Score: {score}/{total}")
print("=" * 70)
