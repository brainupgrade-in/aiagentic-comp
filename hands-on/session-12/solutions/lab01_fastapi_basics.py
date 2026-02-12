"""
Lab 01 Solution: FastAPI Basics
=================================
"""

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from datetime import datetime

print("=" * 50)
print("  FastAPI Basics (Solution)")
print("=" * 50)

app = FastAPI(title="UniGPS Support API", version="1.0.0")

# --- Pydantic Models ---

class SupportRequest(BaseModel):
    employee_name: str
    request: str

class SupportResponse(BaseModel):
    category: str
    response: str
    timestamp: str

TEMPLATES = {
    "hr": "Your HR request has been logged. Check the HR portal for updates.",
    "tech": "A Jira ticket has been created. IT will respond within 4 hours.",
    "finance": "Your finance query is being reviewed. Expect a reply in 2 business days.",
    "general": "Your request has been received. A team member will respond shortly.",
}

def classify_request(text: str) -> str:
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
    return {"status": "healthy", "service": "UniGPS Support API", "version": "1.0.0"}

@app.post("/api/support", response_model=SupportResponse)
async def handle_support(req: SupportRequest):
    category = classify_request(req.request)
    return SupportResponse(
        category=category,
        response=f"Hi {req.employee_name}, {TEMPLATES[category]}",
        timestamp=datetime.now().isoformat(),
    )

SUPPORT_HISTORY = {}

@app.get("/api/support/{ticket_id}")
async def get_ticket(ticket_id: str):
    if ticket_id not in SUPPORT_HISTORY:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found")
    return SUPPORT_HISTORY[ticket_id]

# ============================================================
# TODO 1 Solution: Validated request model
# ============================================================

class ValidatedRequest(BaseModel):
    employee_name: str = Field(..., min_length=2, max_length=50)
    request: str = Field(..., min_length=5, max_length=500)
    priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")

class ValidatedResponse(BaseModel):
    category: str
    response: str
    priority: str
    timestamp: str

@app.post("/api/support/v2", response_model=ValidatedResponse)
async def handle_support_v2(req: ValidatedRequest):
    category = classify_request(req.request)
    return ValidatedResponse(
        category=category,
        response=f"Hi {req.employee_name}, {TEMPLATES[category]}",
        priority=req.priority,
        timestamp=datetime.now().isoformat(),
    )

# ============================================================
# TODO 2 Solution: Ticket store with list endpoint
# ============================================================

ticket_store = []

@app.post("/api/support/v3")
async def handle_with_history(req: SupportRequest):
    category = classify_request(req.request)
    ticket = {
        "id": f"TKT-{len(ticket_store) + 1:04d}",
        "employee_name": req.employee_name,
        "request": req.request,
        "category": category,
        "response": TEMPLATES[category],
        "timestamp": datetime.now().isoformat(),
    }
    ticket_store.append(ticket)
    return ticket

@app.get("/api/tickets")
async def list_tickets(category: str = None, limit: int = 10):
    results = ticket_store
    if category:
        results = [t for t in results if t["category"] == category]
    return {"tickets": results[-limit:], "total": len(results)}

# --- Tests ---

client = TestClient(app)

print("\n--- Step 1 & 2: Basic Endpoints ---\n")

resp = client.get("/health")
print(f"  GET /health → {resp.status_code}: {resp.json()}")

for case in [
    {"employee_name": "Priya", "request": "I need sick leave"},
    {"employee_name": "Vikram", "request": "Server is down"},
]:
    resp = client.post("/api/support", json=case)
    data = resp.json()
    print(f"  POST → {data['category']}: {data['response'][:60]}...")

# 404 test
resp = client.get("/api/support/FAKE-123")
print(f"  GET /api/support/FAKE-123 → {resp.status_code}")

# Validation test (missing field)
resp = client.post("/api/support", json={"employee_name": "Test"})
print(f"  POST (missing 'request') → {resp.status_code}")

print("\n--- TODO 1: Validated Requests ---\n")

# Too short
resp = client.post("/api/support/v2", json={
    "employee_name": "A", "request": "Help"
})
print(f"  Too short → {resp.status_code} (expected 422)")

# Invalid priority
resp = client.post("/api/support/v2", json={
    "employee_name": "Priya", "request": "I need help", "priority": "invalid"
})
print(f"  Invalid priority → {resp.status_code} (expected 422)")

# Valid with priority
resp = client.post("/api/support/v2", json={
    "employee_name": "Priya", "request": "I need help with leave", "priority": "high"
})
data = resp.json()
print(f"  Valid request → {resp.status_code}: priority={data['priority']}, category={data['category']}")

print("\n--- TODO 2: Ticket Store ---\n")

# Create tickets
for case in [
    {"employee_name": "Priya", "request": "I need sick leave"},
    {"employee_name": "Vikram", "request": "Server is down"},
    {"employee_name": "Anita", "request": "Submit expense report"},
]:
    resp = client.post("/api/support/v3", json=case)
    data = resp.json()
    print(f"  Created: {data['id']} ({data['category']})")

# List all
resp = client.get("/api/tickets")
print(f"  GET /api/tickets → {resp.json()['total']} tickets")

# Filter by category
resp = client.get("/api/tickets?category=hr")
hr_count = len(resp.json()["tickets"])
print(f"  GET /api/tickets?category=hr → {hr_count} tickets")

# Limit
resp = client.get("/api/tickets?limit=1")
print(f"  GET /api/tickets?limit=1 → {len(resp.json()['tickets'])} ticket")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print("- TODO 1: Field validation with min_length, max_length, pattern")
print("- TODO 2: Ticket store with category filter and limit")
