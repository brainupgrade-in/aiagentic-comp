# LangFuse-Compatible Server

A lightweight Python-based LangFuse server for Session 12 Lab 09.

## Overview

This is a production-like LangFuse server implementation that:
- Implements the LangFuse REST API endpoints
- Uses SQLite for data persistence
- Runs as a Python FastAPI application (no Docker needed)
- Supports traces, generations, scores, and cost tracking

## Architecture

```
┌─────────────────────────────────────────────────┐
│  FastAPI Application (langfuse-server.py)      │
├─────────────────────────────────────────────────┤
│  Endpoints:                                     │
│  • POST /api/public/traces                     │
│  • POST /api/public/generations                │
│  • POST /api/public/scores                     │
│  • GET  /api/public/traces                     │
│  • GET  /api/public/traces/{trace_id}          │
│  • GET  /api/public/health                     │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  SQLite Database (/tmp/langfuse.db)            │
├─────────────────────────────────────────────────┤
│  Tables:                                        │
│  • traces (user_id, session_id, metadata)      │
│  • generations (model, tokens, cost)           │
│  • scores (rating, feedback)                   │
└─────────────────────────────────────────────────┘
```

## Starting the Server

### Automatic (Recommended)

```bash
# Run day4-setup.sh — it starts the LangFuse server automatically
bash scripts/day4-setup.sh
```

The script will:
1. Start the server on port 3000
2. Save PID to `/tmp/langfuse-server.pid`
3. Log output to `/tmp/langfuse-server.log`
4. Create database at `/tmp/langfuse.db`

### Manual

```bash
# Activate virtual environment
source .venv/bin/activate

# Run the server
python scripts/langfuse-server.py

# Or run in background
nohup python scripts/langfuse-server.py > /tmp/langfuse-server.log 2>&1 &
echo $! > /tmp/langfuse-server.pid
```

## Stopping the Server

### Automatic (Recommended)

```bash
# Run day4-cleanup.sh — it stops the server and cleans up
bash scripts/day4-cleanup.sh
```

### Manual

```bash
# Using saved PID
if [ -f /tmp/langfuse-server.pid ]; then
    kill $(cat /tmp/langfuse-server.pid)
    rm /tmp/langfuse-server.pid
fi

# Or find by port
kill $(lsof -ti:3000)
```

## API Endpoints

### Health Check

```bash
curl http://localhost:3000/api/public/health
```

Response:
```json
{
  "status": "ok",
  "version": "1.0.0",
  "database": true
}
```

### Create Trace

```bash
curl -X POST http://localhost:3000/api/public/traces \
  -H "Authorization: Bearer sk-lf-course-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_trace",
    "userId": "user123",
    "sessionId": "session456",
    "tags": ["test"]
  }'
```

### Create Generation

```bash
curl -X POST http://localhost:3000/api/public/generations \
  -H "Authorization: Bearer sk-lf-course-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "traceId": "trace-xxx",
    "name": "llm_call",
    "model": "llama-3.3-70b-versatile",
    "input": "What is AI?",
    "output": "AI is artificial intelligence...",
    "usage": {
      "input_tokens": 10,
      "output_tokens": 50
    }
  }'
```

### Get Traces

```bash
# All traces
curl http://localhost:3000/api/public/traces \
  -H "Authorization: Bearer sk-lf-course-secret"

# Filter by user
curl "http://localhost:3000/api/public/traces?userId=user123" \
  -H "Authorization: Bearer sk-lf-course-secret"

# Get specific trace
curl http://localhost:3000/api/public/traces/trace-xxx \
  -H "Authorization: Bearer sk-lf-course-secret"
```

## Environment Variables

Set these in your `.env` file:

```bash
# LangFuse server credentials
LANGFUSE_SECRET_KEY=sk-lf-course-secret
LANGFUSE_PUBLIC_KEY=pk-lf-course-key
LANGFUSE_HOST=http://localhost:3000
```

## Database Schema

### Traces Table

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Trace ID (primary key) |
| name | TEXT | Trace name |
| user_id | TEXT | User identifier |
| session_id | TEXT | Session identifier |
| metadata | TEXT | JSON metadata |
| tags | TEXT | JSON array of tags |
| created_at | TEXT | ISO 8601 timestamp |

### Generations Table

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Generation ID (primary key) |
| trace_id | TEXT | Parent trace ID |
| name | TEXT | Generation name |
| model | TEXT | LLM model name |
| input | TEXT | JSON input |
| output | TEXT | JSON output |
| usage | TEXT | JSON token usage |
| metadata | TEXT | JSON metadata |
| cost | REAL | Calculated cost in USD |
| created_at | TEXT | ISO 8601 timestamp |

### Scores Table

| Column | Type | Description |
|--------|------|-------------|
| id | TEXT | Score ID (primary key) |
| trace_id | TEXT | Parent trace ID |
| name | TEXT | Score name (e.g., "user_rating") |
| value | REAL | Numeric score value |
| data_type | TEXT | Score type (default: "NUMERIC") |
| comment | TEXT | Optional feedback comment |
| created_at | TEXT | ISO 8601 timestamp |

## Cost Calculation

The server automatically calculates costs based on token usage and model pricing:

| Model | Input Price (per token) | Output Price (per token) |
|-------|------------------------|-------------------------|
| llama-3.3-70b-versatile | $0.00000059 | $0.00000079 |
| llama-3.2-1b | $0.00000004 | $0.00000004 |
| mixtral-8x7b-32768 | $0.00000027 | $0.00000027 |

Formula: `cost = (input_tokens × input_price) + (output_tokens × output_price)`

## Usage in Labs

### Labs 01-08: MockLangfuse (Local JSON)

These labs use `MockLangfuse` class which writes to local JSON files:

```python
from langfuse import MockLangfuse

langfuse = MockLangfuse(
    public_key="pk-mock",
    secret_key="sk-mock",
    host="http://localhost:8000",
    output_dir="/tmp/langfuse-traces"
)
```

### Lab 09: Real LangFuse Server

Lab 09 uses the real server running on port 3000:

```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
```

## Troubleshooting

### Server won't start - port 3000 in use

```bash
# Find what's using port 3000
lsof -i :3000

# Kill the process
kill $(lsof -ti:3000)
```

### Database locked error

```bash
# Stop all Python processes accessing the DB
pkill -f langfuse-server

# Remove the database and restart
rm /tmp/langfuse.db
bash scripts/day4-setup.sh
```

### Check server logs

```bash
# View recent logs
tail -f /tmp/langfuse-server.log

# View all logs
cat /tmp/langfuse-server.log
```

### API authentication fails

Make sure your `.env` file has the correct keys:

```bash
# Check current values
cat .env | grep LANGFUSE

# Should match:
LANGFUSE_SECRET_KEY=sk-lf-course-secret
LANGFUSE_PUBLIC_KEY=pk-lf-course-key
LANGFUSE_HOST=http://localhost:3000
```

## Differences from Real LangFuse

This server is simplified for course purposes. Real LangFuse includes:

1. **Web UI Dashboard** — This server is API-only
2. **User Authentication** — This server uses simple Bearer token auth
3. **PostgreSQL/MySQL** — This server uses SQLite
4. **Advanced Features** — Prompt management, experiments, datasets
5. **Scalability** — This server is single-instance, not clustered

For production use, deploy the official LangFuse server:
- **Cloud:** https://cloud.langfuse.com
- **Self-hosted:** https://langfuse.com/docs/deployment/self-host

## Files Created

| File | Description |
|------|-------------|
| `/tmp/langfuse.db` | SQLite database (persistent across requests) |
| `/tmp/langfuse-server.log` | Server logs (stdout/stderr) |
| `/tmp/langfuse-server.pid` | Process ID (for cleanup) |

## Session 12 Lab 09 Integration

Lab 09 demonstrates a production FastAPI application that:

1. Creates traces for each support request
2. Logs LLM generations with token usage
3. Calculates costs per request
4. Collects user feedback via scores
5. Exposes observability metrics in health probes

The LangFuse server enables:
- ✅ Centralized trace storage (SQLite DB)
- ✅ Cost tracking across requests
- ✅ User feedback collection
- ✅ Historical trace queries
- ✅ Production-like observability patterns

## License

Part of the Agentic AI Course © Gheware UniGPS Solutions LLP
