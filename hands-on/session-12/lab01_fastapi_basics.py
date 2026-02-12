"""
Lab 01: FastAPI Basics
========================
Goal: Build a basic FastAPI app with Pydantic request/response models,
      health checks, and request validation.

What you'll learn:
- Creating FastAPI endpoints
- Pydantic models for request/response validation
- Health check endpoints
- Using TestClient for testing without running a server

No API key needed — pure Python + FastAPI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from datetime import datetime

print("=" * 50)
print("  FastAPI Basics")
print("=" * 50)

# ============================================================
# Step 1: Basic FastAPI app with Pydantic models
# ============================================================

app = FastAPI(title="UniGPS Support API", version="1.0.0")

# --- Pydantic Models ---

class SupportRequest(BaseModel):
    employee_name: str
    request: str

class SupportResponse(BaseModel):
    category: str
    response: str
    timestamp: str

# --- Template responses (no LLM needed) ---

TEMPLATES = {
    "hr": "Your HR request has been logged. Check the HR portal for updates.",
    "tech": "A Jira ticket has been created. IT will respond within 4 hours.",
    "finance": "Your finance query is being reviewed. Expect a reply in 2 business days.",
    "general": "Your request has been received. A team member will respond shortly.",
}

def classify_request(text: str) -> str:
    """Simple keyword-based classification."""
    msg = text.lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "policy", "hr"]):
        return "hr"
    elif any(w in msg for w in ["server", "bug", "deploy", "laptop", "vpn"]):
        return "tech"
    elif any(w in msg for w in ["expense", "salary", "invoice", "budget"]):
        return "finance"
    return "general"

# --- Endpoints ---

@app.get("/health")
async def health_check():
    """Health check for load balancers."""
    return {"status": "healthy", "service": "UniGPS Support API", "version": "1.0.0"}

@app.post("/api/support", response_model=SupportResponse)
async def handle_support(req: SupportRequest):
    """Handle a support request."""
    category = classify_request(req.request)
    response_text = TEMPLATES[category]
    return SupportResponse(
        category=category,
        response=f"Hi {req.employee_name}, {response_text}",
        timestamp=datetime.now().isoformat(),
    )

# --- Test with TestClient (no server needed!) ---

client = TestClient(app)

print("\n--- Step 1: Basic Endpoints ---\n")

# Test health check
resp = client.get("/health")
print(f"  GET /health → {resp.status_code}: {resp.json()}")

# Test support endpoint
test_cases = [
    {"employee_name": "Priya", "request": "I need sick leave"},
    {"employee_name": "Vikram", "request": "Server is down"},
    {"employee_name": "Anita", "request": "Submit expense report"},
    {"employee_name": "Rahul", "request": "Where is meeting room 5?"},
]

for case in test_cases:
    resp = client.post("/api/support", json=case)
    data = resp.json()
    print(f"  POST /api/support → {data['category']}: {data['response'][:60]}...")


# ============================================================
# Step 2: Error handling with HTTPException
# ============================================================

print("\n\n--- Step 2: Error Handling ---\n")

SUPPORT_HISTORY = {}

@app.get("/api/support/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Retrieve a support ticket by ID."""
    if ticket_id not in SUPPORT_HISTORY:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found")
    return SUPPORT_HISTORY[ticket_id]

# Test 404
resp = client.get("/api/support/FAKE-123")
print(f"  GET /api/support/FAKE-123 → {resp.status_code}: {resp.json()}")

# Test invalid JSON (missing required field)
resp = client.post("/api/support", json={"employee_name": "Test"})
print(f"  POST (missing 'request') → {resp.status_code} (validation error)")

# Test valid request
resp = client.post("/api/support", json={"employee_name": "Priya", "request": "Leave request"})
print(f"  POST (valid) → {resp.status_code}: category={resp.json()['category']}")


# ============================================================
# TODO 1: Add request validation with Field constraints
# ============================================================
# Add min_length and max_length constraints to the Pydantic model.
# Create a new endpoint /api/support/v2 with the validated model.
#
# Hint:
#   from pydantic import Field
#
#   class ValidatedRequest(BaseModel):
#       employee_name: str = Field(..., min_length=2, max_length=50)
#       request: str = Field(..., min_length=5, max_length=500)
#       priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")
#
#   @app.post("/api/support/v2")
#   async def handle_support_v2(req: ValidatedRequest):
#       ...
#
# Test cases:
#   - {"employee_name": "A", "request": "Help"} → should fail (too short)
#   - {"employee_name": "Priya", "request": "I need help", "priority": "invalid"} → should fail
#   - {"employee_name": "Priya", "request": "I need help", "priority": "high"} → should pass


# ============================================================
# TODO 2: Add a GET endpoint to list recent support tickets
# ============================================================
# Create an in-memory ticket store and a GET endpoint to list tickets.
#
# Hint:
#   ticket_store = []
#
#   @app.post("/api/support/v3")
#   async def handle_with_history(req: SupportRequest):
#       category = classify_request(req.request)
#       ticket = {
#           "id": f"TKT-{len(ticket_store) + 1:04d}",
#           "employee_name": req.employee_name,
#           "request": req.request,
#           "category": category,
#           "response": TEMPLATES[category],
#           "timestamp": datetime.now().isoformat(),
#       }
#       ticket_store.append(ticket)
#       return ticket
#
#   @app.get("/api/tickets")
#   async def list_tickets(category: str = None, limit: int = 10):
#       """List tickets, optionally filtered by category."""
#       results = ticket_store
#       if category:
#           results = [t for t in results if t["category"] == category]
#       return {"tickets": results[-limit:], "total": len(results)}
#
# Test:
#   1. POST 3 requests (hr, tech, finance)
#   2. GET /api/tickets → should list all 3
#   3. GET /api/tickets?category=hr → should list only HR tickets
#   4. GET /api/tickets?limit=1 → should list only the most recent


print("\n" + "=" * 50)
print("Lab 01 complete!")
print("Patterns: Pydantic models, REST endpoints, error handling, TestClient")
