#!/usr/bin/env bash
# langfuse-server.sh — Control the local LangFuse-compatible server (Day 4, Session 12 Lab 09).
#
# Wraps scripts/langfuse-server.py (FastAPI + SQLite) on port 3000.
#
# Usage (from repo root):
#   bash scripts/langfuse-server.sh start
#   bash scripts/langfuse-server.sh status
#   bash scripts/langfuse-server.sh stop

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="/tmp/langfuse-server.pid"
LOG_FILE="/tmp/langfuse-server.log"
HEALTH_URL="http://localhost:3000/api/public/health"

if [ -x "$REPO_DIR/.venv/Scripts/python.exe" ]; then
    VENV_PY="$REPO_DIR/.venv/Scripts/python.exe"
else
    VENV_PY="$REPO_DIR/.venv/bin/python"
fi

is_up() { curl -sf "$HEALTH_URL" &>/dev/null; }

start() {
    if is_up; then
        echo "  LangFuse server already running on http://localhost:3000"
        return 0
    fi
    if [ ! -x "$VENV_PY" ]; then
        echo "  ERROR: .venv not found — run: bash scripts/setup.sh"
        exit 1
    fi
    nohup "$VENV_PY" "$REPO_DIR/scripts/langfuse-server.py" > "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    for _ in 1 2 3 4 5 6 7 8 9 10; do
        is_up && break
        sleep 1
    done
    if is_up; then
        echo "  LangFuse server started — http://localhost:3000 (PID $(cat "$PID_FILE"))"
        echo "  Database: /tmp/langfuse.db   Logs: $LOG_FILE"
    else
        echo "  ERROR: server failed to start. Check $LOG_FILE"
        exit 1
    fi
}

stop() {
    STOPPED=0
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if kill -0 "$PID" 2>/dev/null; then
            kill "$PID"
            echo "  Stopped LangFuse server (PID $PID)"
            STOPPED=1
        fi
        rm -f "$PID_FILE"
    fi
    if [ "$STOPPED" -eq 0 ]; then
        PID=$(lsof -ti:3000 2>/dev/null || true)
        if [ -n "$PID" ]; then
            kill $PID
            echo "  Stopped process on port 3000 (PID $PID)"
        else
            echo "  No LangFuse server running"
        fi
    fi
}

status() {
    if is_up; then
        echo "  RUNNING — http://localhost:3000"
        [ -f "$PID_FILE" ] && echo "  PID: $(cat "$PID_FILE")"
        [ -f /tmp/langfuse.db ] && echo "  Database: /tmp/langfuse.db ($(du -h /tmp/langfuse.db | cut -f1))"
    else
        echo "  STOPPED — start it with: bash scripts/langfuse-server.sh start"
    fi
}

case "${1:-status}" in
    start)  start ;;
    stop)   stop ;;
    status) status ;;
    *) echo "Usage: bash scripts/langfuse-server.sh {start|stop|status}"; exit 1 ;;
esac
