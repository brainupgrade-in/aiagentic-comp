#!/bin/bash
set -e

echo "============================================"
echo "  Day 4: Observability & Production Cleanup"
echo "============================================"
echo ""

echo "Before cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""

# Stop LangFuse server
echo "[1/4] Stopping LangFuse server..."
if [ -f /tmp/langfuse-server.pid ]; then
    LANGFUSE_PID=$(cat /tmp/langfuse-server.pid)
    if kill -0 $LANGFUSE_PID 2>/dev/null; then
        kill $LANGFUSE_PID
        echo "  ✓ Stopped LangFuse server (PID: $LANGFUSE_PID)"
    else
        echo "  LangFuse server not running (stale PID file)"
    fi
    rm -f /tmp/langfuse-server.pid
else
    # Try to find and kill by port
    LANGFUSE_PID=$(lsof -ti:3000 2>/dev/null || true)
    if [ -n "$LANGFUSE_PID" ]; then
        kill $LANGFUSE_PID
        echo "  ✓ Stopped process on port 3000 (PID: $LANGFUSE_PID)"
    else
        echo "  No LangFuse server running"
    fi
fi

# Clean up LangFuse database and logs
echo "[2/4] Cleaning up LangFuse data..."
rm -f /tmp/langfuse.db /tmp/langfuse-server.log
echo "  ✓ Removed database and logs"

# Clean up lab temp files
echo "[3/4] Removing lab temp files..."
rm -rf /tmp/ailab-10-* /tmp/ailab-11-* /tmp/prod-lab-12-* /tmp/ailab-12-*
echo "  ✓ Removed temp directories"

# Stop stale processes
echo "[4/4] Stopping stale processes..."
pkill -f "uvicorn.*8000" 2>/dev/null || true
pkill -f "fastapi" 2>/dev/null || true
echo "  ✓ Stopped stale FastAPI processes"

echo ""
echo "After cleanup:"
df -h / | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5" used)"}'
free -h | awk '/Mem:/{print "  Memory: "$3" used / "$2" total"}'
echo ""
echo "Day 4 cleanup complete. Ready for Day 5 (MCP + Capstone)."
echo ""
