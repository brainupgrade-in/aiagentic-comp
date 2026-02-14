# Lab 09: LangFuse Cloud Integration

## Overview

Session 12 Lab 09 has been updated to use **real LangFuse cloud credentials** instead of MockLangfuse. All observability data is now sent to the production LangFuse cloud dashboard at https://cloud.langfuse.com.

## What Changed

### Before (MockLangfuse)
```python
# Local JSON file storage
class MockLangfuse:
    def __init__(self, output_dir="/tmp/langfuse-traces"):
        self.output_dir = output_dir
        self._traces = []

    def flush(self):
        with open("traces.json", "w") as f:
            json.dump(self._traces, f)

langfuse = MockLangfuse(...)
```

### After (Real LangFuse Cloud)
```python
# Cloud-based observability
from langfuse import Langfuse
from langfuse.callback import CallbackHandler

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com"),
)
```

## Key Benefits

### 1. **Production-Grade Observability**
- Real-time trace collection and visualization
- Centralized dashboard accessible from anywhere
- Team collaboration and trace sharing
- Historical analysis and trend monitoring

### 2. **Automatic Instrumentation**
```python
# CallbackHandler captures all LangGraph steps automatically
langfuse_handler = CallbackHandler(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_BASE_URL"),
    session_id=session_id,
    user_id=req.employee_name,
    tags=["production", "support", "fastapi"],
)

# Just pass it to agent.invoke()
result = agent.invoke(state, config={"callbacks": [langfuse_handler]})
```

### 3. **Rich Dashboard Features**
- **Traces View:** Full execution flow visualization
- **Generations View:** All LLM calls with costs
- **Sessions View:** Multi-turn conversation grouping
- **Users View:** Per-user analytics and costs
- **Scores View:** User feedback and quality metrics
- **Analytics:** Cost trends, latency distribution, usage patterns

### 4. **Trace URLs**
```python
# Return direct links to traces
trace_url = f"{LANGFUSE_HOST}/trace/{trace_id}"

return SupportResponse(
    category=result["category"],
    response=result["final_response"],
    trace_id=trace_id,
    trace_url=trace_url,  # ← Users can click to see full trace
    latency_ms=latency_ms,
)
```

## Environment Configuration

### .env File
```bash
# LangFuse Cloud Credentials
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key-here
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key-here
LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

## Lab Structure

### Updated Cells

| Cell | Before | After |
|------|--------|-------|
| 3-4 | MockLangfuse class definition | Real LangFuse client initialization |
| 8 | Manual trace.generation() calls | CallbackHandler automatic capture |
| 11-12 | No trace URLs | Trace URLs returned in responses |
| 14-15 | Local trace queries | LangFuse dashboard instructions |
| 16-18 | Display local JSON | Dashboard exploration guide |
| 19-20 | TODO: Cost analysis | Complete with cloud dashboard |
| 21-22 | TODO: Quality metrics | Complete with scores API |
| 23 | TODO: Checklist | Verify in cloud dashboard |

### New Features

**1. Health Endpoint Enhancement**
```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "observability": "langfuse-cloud",
        "langfuse_host": os.getenv("LANGFUSE_BASE_URL"),
    }
```

**2. Feedback Endpoint**
```python
@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    langfuse.score(
        trace_id=feedback.trace_id,
        name="user_rating",
        value=feedback.rating,
        comment=feedback.comment,
    )
    return {"status": "success", "message": "Feedback submitted to LangFuse cloud"}
```

**3. Trace URL in Response**
```python
class SupportResponse(BaseModel):
    category: str
    response: str
    audit: list[str]
    trace_id: str
    trace_url: str  # ← New field
    latency_ms: int
```

## TODO Solutions

### TODO 1: Cost Analysis (Cloud Dashboard)
Students analyze real cost data from the LangFuse dashboard:

```python
# Example solution
total_cost = "0.00004"  # From dashboard
avg_cost_per_request = "0.00002"
supervisor_cost = "0.000003"  # Classification step
worker_cost = "0.000015"  # Response generation
most_expensive_step = "worker"  # Longer outputs cost more
```

### TODO 2: Quality Metrics (Scores Dashboard)
Students review user feedback scores:

```python
# Example solution
avg_rating = "4.5"  # Average of 5 and 4 stars
total_scores = "2"  # Two feedback submissions
high_rated_count = "2"  # Both are 4+
feedback_coverage_percent = "100"  # All traces have feedback
```

### TODO 3: Production Checklist (Dashboard Verification)
Students verify all observability features in the cloud:

```
✅ Trace Collection:
   - All requests create traces
   - User IDs and session IDs tracked
   - Tags applied (production, support, fastapi)

✅ LLM Observability:
   - All generations logged automatically
   - Input/output captured
   - Token usage tracked

✅ Cost Tracking:
   - Per-generation costs calculated
   - Total trace costs visible
   - Can filter by user/session

✅ Quality Monitoring:
   - Scores linked to traces
   - Comments provide insights
   - Low-rated traces identifiable

✅ Production Readiness:
   - Health endpoint reports status
   - Trace URLs returned to clients
   - Metadata enables debugging
```

## Testing the Lab

### Step 1: Verify Credentials
```bash
# Check .env file
cat .env | grep LANGFUSE

# Should show:
# LANGFUSE_SECRET_KEY=sk-lf-...
# LANGFUSE_PUBLIC_KEY=pk-lf-...
# LANGFUSE_BASE_URL=https://cloud.langfuse.com
```

### Step 2: Run the Lab
```bash
# Open in Jupyter or VS Code
jupyter notebook hands-on/session-12/lab09_production_observability.ipynb

# Or in VS Code:
code hands-on/session-12/lab09_production_observability.ipynb
```

### Step 3: Execute Cells
1. Run setup cells (0-6)
2. Run FastAPI app definition (7-8)
3. Run tests (9-15)
4. View LangFuse dashboard (16-18)
5. Complete TODOs (19-23)

### Step 4: Verify in Dashboard
1. Open https://cloud.langfuse.com
2. Navigate to "Traces" → See your 2 test traces
3. Navigate to "Generations" → See 4 LLM calls
4. Navigate to "Scores" → See 2 user ratings
5. Click on a trace → Explore full execution flow

## Dashboard Navigation Guide

### Traces View
- **What:** All support requests logged as traces
- **See:** Priya's sick leave request, Vikram's VPN issue
- **Filter:** By user (Priya, Vikram), session, tags, date
- **Click:** On a trace to see full details

### Generations View
- **What:** All LLM calls (supervisor + worker)
- **See:** 2 supervisor classifications, 2 worker responses
- **Metrics:** Model, tokens, cost, latency
- **Compare:** Different prompts and outputs

### Sessions View
- **What:** Grouped traces by session_id
- **See:** test-session-001, test-session-002
- **Metrics:** Total cost, trace count, avg latency
- **Use:** Multi-turn conversation analysis

### Users View
- **What:** Per-user analytics
- **See:** Priya (1 trace), Vikram (1 trace)
- **Metrics:** Total cost, trace count
- **Use:** User behavior patterns

### Scores View
- **What:** User feedback ratings
- **See:** 5-star (Priya), 4-star (Vikram)
- **Link:** Click to see associated trace
- **Analyze:** Quality trends over time

## Migration from Mock to Cloud

### Development Workflow
```
┌─────────────────────────────────────────────────┐
│  Local Development                              │
│  • Use MockLangfuse                             │
│  • Fast iteration (no network calls)            │
│  • JSON files for debugging                     │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Staging Environment                            │
│  • Use LangFuse cloud (staging project)         │
│  • Test with real observability                 │
│  • Validate dashboard views                     │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Production Environment                         │
│  • Use LangFuse cloud (production project)      │
│  • Full observability with team access          │
│  • Alerts, analytics, cost monitoring           │
└─────────────────────────────────────────────────┘
```

### Code Changes (None!)
```python
# Same code works for both mock and cloud!
# Just change environment variables in .env

# Development (.env)
LANGFUSE_HOST=http://localhost:8000  # Mock
LANGFUSE_SECRET_KEY=sk-mock
LANGFUSE_PUBLIC_KEY=pk-mock

# Production (.env)
LANGFUSE_HOST=https://cloud.langfuse.com  # Cloud
LANGFUSE_SECRET_KEY=sk-lf-real-key
LANGFUSE_PUBLIC_KEY=pk-lf-real-key
```

## Common Issues & Solutions

### Issue 1: "Connection refused" error
**Cause:** Invalid credentials or network issue
**Solution:**
```bash
# Verify credentials
echo $LANGFUSE_SECRET_KEY
echo $LANGFUSE_PUBLIC_KEY

# Test connection
curl -H "Authorization: Bearer $LANGFUSE_SECRET_KEY" \
  https://cloud.langfuse.com/api/public/health
```

### Issue 2: Traces not appearing in dashboard
**Cause:** Forgot to flush the handler
**Solution:**
```python
# Always flush after invoke
langfuse_handler.flush()

# Or use context manager (auto-flush)
with CallbackHandler(...) as handler:
    result = agent.invoke(state, config={"callbacks": [handler]})
```

### Issue 3: Incorrect costs displayed
**Cause:** Using wrong model name or missing usage data
**Solution:**
```python
# Ensure correct model name
llm = ChatGroq(model="llama-3.3-70b-versatile")  # Exact match

# LangChain automatically tracks usage
# No manual usage calculation needed with CallbackHandler
```

### Issue 4: "Trace ID not found" when submitting feedback
**Cause:** Trace hasn't synced yet
**Solution:**
```python
# Add small delay or retry logic
import time
time.sleep(1)  # Wait for sync
langfuse.score(trace_id=trace_id, ...)

# Or check if trace exists first
traces = langfuse.get_traces()
if trace_id in [t.id for t in traces]:
    langfuse.score(...)
```

## Production Best Practices

### 1. Environment Variables
```python
# ✅ Good: Use environment variables
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
)

# ❌ Bad: Hardcode credentials
langfuse = Langfuse(
    secret_key="sk-lf-hardcoded",  # Never do this!
    public_key="pk-lf-hardcoded",
)
```

### 2. Error Handling
```python
# ✅ Good: Wrap in try/except
try:
    langfuse_handler = CallbackHandler(...)
    result = agent.invoke(state, config={"callbacks": [langfuse_handler]})
    langfuse_handler.flush()
except Exception as e:
    logger.error(f"LangFuse error: {e}")
    # Continue without observability rather than failing
    result = agent.invoke(state)
```

### 3. Rich Metadata
```python
# ✅ Good: Include debugging context
langfuse_handler = CallbackHandler(
    session_id=session_id,
    user_id=user_id,
    tags=["production", "v2.0", "fastapi"],
    metadata={
        "endpoint": "/api/support",
        "request_preview": request[:100],
        "client_ip": request.client.host,
        "version": "2.0.1",
    }
)

# ❌ Bad: Minimal metadata
langfuse_handler = CallbackHandler()
```

### 4. Trace URLs
```python
# ✅ Good: Return trace URL for support tickets
return {
    "response": result,
    "trace_id": handler.get_trace_id(),
    "trace_url": f"{LANGFUSE_HOST}/trace/{handler.get_trace_id()}",
}

# ❌ Bad: No trace reference
return {"response": result}
```

### 5. Project Separation
```
Development:   langfuse-dev-project
Staging:       langfuse-staging-project
Production:    langfuse-prod-project
```

Use separate LangFuse projects for each environment to avoid mixing test data with production traces.

## Resources

- **LangFuse Dashboard:** https://cloud.langfuse.com
- **LangFuse Docs:** https://langfuse.com/docs
- **LangChain Integration:** https://langfuse.com/docs/integrations/langchain
- **CallbackHandler API:** https://langfuse.com/docs/integrations/langchain/tracing
- **Cost Tracking:** https://langfuse.com/docs/experimentation/cost-tracking
- **Scores API:** https://langfuse.com/docs/scores/overview
- **Community Discord:** https://discord.gg/7NXusRtqYU

## Credentials

Your LangFuse cloud credentials (from .env):

```
Secret Key: sk-lf-your-secret-key-here
Public Key: pk-lf-your-public-key-here
Base URL:   https://cloud.langfuse.com
```

**Security Note:** These credentials are stored in `.env` file which is gitignored. Never commit credentials to version control!

## Next Steps

1. **Complete Lab 09:** Run all cells and verify traces in dashboard
2. **Explore Dashboard:** Navigate all sections (Traces, Generations, Scores, etc.)
3. **Complete TODOs:** Fill in cost analysis and quality metrics from dashboard
4. **Experiment:** Try different prompts and compare costs/quality
5. **Share:** Use trace URLs to share interesting executions with team
6. **Scale:** Test with higher volumes to see dashboard under load

---

**Status:** ✅ Lab 09 fully updated for LangFuse cloud integration
**Files Modified:**
- `hands-on/session-12/lab09_production_observability.ipynb` (main lab)
- `hands-on/session-12/solutions/lab09_production_observability.ipynb` (solution)

**Date:** 2026-02-15
