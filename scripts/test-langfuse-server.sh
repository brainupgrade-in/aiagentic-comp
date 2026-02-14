#!/bin/bash
# Test script for LangFuse server setup
# Verifies that the server can start, respond to health checks, and handle basic API calls

set -e

echo "============================================"
echo "  LangFuse Server Test"
echo "============================================"
echo ""

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export LANGFUSE_SECRET_KEY="sk-lf-course-secret"
export LANGFUSE_PUBLIC_KEY="pk-lf-course-key"
export LANGFUSE_HOST="http://localhost:3000"

# Check if virtual environment exists
if [ ! -f "$REPO_DIR/.venv/bin/python" ]; then
    echo "ERROR: Virtual environment not found at $REPO_DIR/.venv"
    echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

source "$REPO_DIR/.venv/bin/activate"

# Check if required packages are installed
echo "[1/6] Checking dependencies..."
python -c "import fastapi, uvicorn, pydantic" 2>/dev/null || {
    echo "ERROR: Missing dependencies. Install with: pip install -r requirements.txt"
    exit 1
}
echo "  ✓ All dependencies installed"

# Start the server in background
echo ""
echo "[2/6] Starting LangFuse server..."
nohup python "$REPO_DIR/scripts/langfuse-server.py" > /tmp/langfuse-server-test.log 2>&1 &
SERVER_PID=$!
echo "  ✓ Server started (PID: $SERVER_PID)"

# Wait for server to start
echo ""
echo "[3/6] Waiting for server to be ready..."
sleep 3

# Check if server is running
if ! kill -0 $SERVER_PID 2>/dev/null; then
    echo "  ERROR: Server failed to start. Check /tmp/langfuse-server-test.log"
    cat /tmp/langfuse-server-test.log
    exit 1
fi

# Test health endpoint
echo ""
echo "[4/6] Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:3000/api/public/health)
if echo "$HEALTH_RESPONSE" | grep -q '"status":"ok"'; then
    echo "  ✓ Health check passed"
    echo "  Response: $HEALTH_RESPONSE"
else
    echo "  ERROR: Health check failed"
    echo "  Response: $HEALTH_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Test API endpoints
echo ""
echo "[5/6] Testing API endpoints..."

# Create a trace
TRACE_RESPONSE=$(curl -s -X POST http://localhost:3000/api/public/traces \
    -H "Authorization: Bearer $LANGFUSE_SECRET_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "test_trace",
        "userId": "test-user",
        "sessionId": "test-session",
        "tags": ["test"]
    }')

TRACE_ID=$(echo "$TRACE_RESPONSE" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
if [ -n "$TRACE_ID" ]; then
    echo "  ✓ Created trace: $TRACE_ID"
else
    echo "  ERROR: Failed to create trace"
    echo "  Response: $TRACE_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Create a generation
GEN_RESPONSE=$(curl -s -X POST http://localhost:3000/api/public/generations \
    -H "Authorization: Bearer $LANGFUSE_SECRET_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"traceId\": \"$TRACE_ID\",
        \"name\": \"test_generation\",
        \"model\": \"llama-3.3-70b-versatile\",
        \"input\": \"test input\",
        \"output\": \"test output\",
        \"usage\": {
            \"input_tokens\": 10,
            \"output_tokens\": 20
        }
    }")

if echo "$GEN_RESPONSE" | grep -q '"cost"'; then
    echo "  ✓ Created generation with cost calculation"
else
    echo "  ERROR: Failed to create generation"
    echo "  Response: $GEN_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Create a score
SCORE_RESPONSE=$(curl -s -X POST http://localhost:3000/api/public/scores \
    -H "Authorization: Bearer $LANGFUSE_SECRET_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"traceId\": \"$TRACE_ID\",
        \"name\": \"user_rating\",
        \"value\": 5,
        \"comment\": \"Excellent!\"
    }")

if echo "$SCORE_RESPONSE" | grep -q '"value":5'; then
    echo "  ✓ Created score"
else
    echo "  ERROR: Failed to create score"
    echo "  Response: $SCORE_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Get traces
TRACES_RESPONSE=$(curl -s "http://localhost:3000/api/public/traces?userId=test-user" \
    -H "Authorization: Bearer $LANGFUSE_SECRET_KEY")

if echo "$TRACES_RESPONSE" | grep -q '"totalItems":1'; then
    echo "  ✓ Retrieved traces successfully"
else
    echo "  ERROR: Failed to retrieve traces"
    echo "  Response: $TRACES_RESPONSE"
    kill $SERVER_PID
    exit 1
fi

# Cleanup
echo ""
echo "[6/6] Cleaning up..."
kill $SERVER_PID
sleep 1
rm -f /tmp/langfuse.db /tmp/langfuse-server-test.log
echo "  ✓ Server stopped and temp files removed"

echo ""
echo "============================================"
echo "  ✓ All tests passed!"
echo "============================================"
echo ""
echo "The LangFuse server is ready for Session 12 Lab 09."
echo ""
