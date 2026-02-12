#!/bin/bash
set -e

echo "============================================"
echo "  Day 1: Ollama + Local LLM Setup"
echo "============================================"
echo ""

# Check available resources
echo "Current resource usage:"
free -h | head -2
echo ""

# Install Ollama
echo "[1/2] Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama server in background
echo "[2/2] Pulling llama3.2:1b model (~1.3 GB)..."
ollama serve &>/dev/null &
sleep 3
ollama pull llama3.2:1b

echo ""
echo "============================================"
echo "  Day 1 setup complete!"
echo "============================================"
echo ""
echo "Today's sessions:"
echo "  Session 1: Introduction to Agentic AI"
echo "  Session 2: AI Coding Assistants & Vibe Coding"
echo "  Session 3: Reasoning, Planning & Tool Use"
echo ""
echo "Test it:"
echo "  ollama run llama3.2:1b 'Hello, world!'"
echo ""
echo "In Python:"
echo "  from langchain_ollama import ChatOllama"
echo "  llm = ChatOllama(model='llama3.2:1b')"
echo "  print(llm.invoke('Hello'))"
echo ""
echo "Labs:"
echo "  python hands-on/session-1/lab01_meet_your_llm.py"
echo "  python hands-on/session-2/lab01_coding_agent_anatomy.py"
echo "  python hands-on/session-3/lab01_chain_of_thought.py"
echo ""
echo "IMPORTANT: Run 'bash scripts/day1-cleanup.sh' at end of day"
echo "to free ~2 GB for remaining days."
echo ""
