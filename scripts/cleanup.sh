#!/usr/bin/env bash
# cleanup.sh — End-of-day cleanup for the Agentic AI course.
#
# Removes that day's /tmp lab working dirs and stops the servers the course
# itself started. The Python environment is never touched — it is shared by all
# five days, so there is nothing to reinstall tomorrow.
#
# Stray processes on the course ports are REPORTED, not killed: a blanket
# "pkill uvicorn" would also take out unrelated apps on your machine.
#
# Usage (from repo root):
#   bash scripts/cleanup.sh            # everything (all days)
#   bash scripts/cleanup.sh 4          # Day 4 only
#   bash scripts/cleanup.sh 1 --purge-ollama   # also delete Ollama + the model (~2 GB)

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OLLAMA_MODEL="llama3.2:1b"

DAY="all"
PURGE_OLLAMA=0
for arg in "$@"; do
    case "$arg" in
        1|2|3|4|5|all)   DAY="$arg" ;;
        --purge-ollama)  PURGE_OLLAMA=1 ;;
        -h|--help)       awk 'NR>1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "${BASH_SOURCE[0]}"; exit 0 ;;
        *) echo "Unknown option: $arg (expected 1-5, all, or --purge-ollama)"; exit 1 ;;
    esac
done

usage_report() {
    df -h / 2>/dev/null | tail -1 | awk '{print "  Storage: "$3" used / "$2" total ("$5")"}' || true
    free -h 2>/dev/null | awk '/Mem:/{print "  Memory:  "$3" used / "$2" total"}' || true
}

# Report anything still holding a course port. Deliberately does not kill:
# port 8000 in particular is a common default for unrelated local apps.
report_port() {
    local port="$1" label="$2" pids
    pids=$(lsof -ti:"$port" 2>/dev/null || true)
    if [ -n "$pids" ]; then
        echo "  NOTE: port $port ($label) still in use by PID(s): $(echo "$pids" | tr '\n' ' ')"
        echo "        If it is a lab server, stop it with: kill $(echo "$pids" | tr '\n' ' ')"
    fi
}

# ── Per-day actions ───────────────────────────────────────────────────────────
clean_day1() {
    echo "[Day 1] Ollama + local LLM"
    if command -v ollama &>/dev/null; then
        # Unloads the model from RAM without fighting the systemd service
        ollama stop "$OLLAMA_MODEL" 2>/dev/null || true
        echo "  Unloaded $OLLAMA_MODEL from memory"
    fi
    if [ "$PURGE_OLLAMA" -eq 1 ]; then
        ollama rm "$OLLAMA_MODEL" 2>/dev/null || true
        if systemctl is-active --quiet ollama 2>/dev/null; then
            sudo systemctl stop ollama 2>/dev/null || true
            sudo systemctl disable ollama 2>/dev/null || true
        else
            pkill -x ollama 2>/dev/null || true
        fi
        sudo rm -f /usr/local/bin/ollama /usr/bin/ollama 2>/dev/null || true
        sudo rm -rf /usr/share/ollama 2>/dev/null || true
        rm -rf ~/.ollama
        echo "  Removed Ollama and $OLLAMA_MODEL (~2 GB freed)"
    else
        echo "  Ollama left installed. To reclaim ~2 GB: bash scripts/cleanup.sh 1 --purge-ollama"
    fi
    rm -rf /tmp/aidev-lab-02-* /tmp/k8s-lab-03-*
    echo "  Removed Day 1 lab temp dirs"
}

clean_day2() {
    echo "[Day 2] LangChain + RAG"
    rm -rf /tmp/k8s-lab-04-* /tmp/k8s-lab-05-* /tmp/k8s-lab-06-* /tmp/chroma-data
    echo "  Removed Day 2 lab temp dirs and ChromaDB data"
}

clean_day3() {
    echo "[Day 3] LangGraph + Multi-Agent"
    rm -rf /tmp/k8s-lab-07-* /tmp/k8s-lab-08-* /tmp/k8s-lab-09-*
    echo "  Removed Day 3 lab temp dirs"
    report_port 8000 "FastAPI labs"
}

clean_day4() {
    echo "[Day 4] Observability + Production"
    bash "$REPO_DIR/scripts/langfuse-server.sh" stop || true
    rm -f /tmp/langfuse.db /tmp/langfuse-server.log
    rm -rf /tmp/k8s-lab-10-* /tmp/prod-lab-11-* /tmp/k8s-lab-12-* /tmp/prod-lab-12-* \
           /tmp/langfuse-traces /tmp/langfuse-data
    echo "  Removed the LangFuse database, logs, and Day 4 lab temp dirs"
    report_port 8000 "FastAPI labs"
}

clean_day5() {
    echo "[Day 5] MCP + Safety + Capstone"
    rm -rf /tmp/aidev-lab-13-* /tmp/safety-lab-14-* /tmp/capstone-lab-15-*
    echo "  Removed Day 5 lab temp dirs"
    echo "  MCP lab servers run inside notebooks — restart the kernel to stop them"
    report_port 8000 "FastAPI labs"
}

# ── Run ───────────────────────────────────────────────────────────────────────
echo "============================================"
echo "  Cleanup — Day $DAY"
echo "============================================"
echo ""
echo "Before:"
usage_report
echo ""

case "$DAY" in
    1) clean_day1 ;;
    2) clean_day2 ;;
    3) clean_day3 ;;
    4) clean_day4 ;;
    5) clean_day5 ;;
    all)
        clean_day1; echo ""
        clean_day2; echo ""
        clean_day3; echo ""
        clean_day4; echo ""
        clean_day5
        ;;
esac

echo ""
echo "[All] Python bytecode caches"
find "$REPO_DIR" -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
echo "  Removed __pycache__ directories"

echo ""
echo "After:"
usage_report
echo ""
echo "Cleanup complete. The .venv and all packages are untouched — no setup needed tomorrow."
echo ""
