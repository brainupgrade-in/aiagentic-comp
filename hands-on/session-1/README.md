# Session 1: Introduction to Agentic AI — Hands-on Labs

## Prerequisites

- Codespace is running with Day 1 setup complete (`bash scripts/day1-setup.sh`)
- Ollama is running with `llama3.2:1b` model pulled
- Python virtual environment is activated

Verify your setup:
```bash
# Check Ollama is running and model is available
ollama list

# Activate virtual environment (if not already)
source ~/.venv/bin/activate

# Quick test — should print "Ready"
python -c "from langchain_ollama import ChatOllama; print('Ready')"
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Meet Your LLM | Talk to a local AI for the first time — send a message, read the response |
| 02 | Exploring LLM Superpowers | What LLMs are great at — writing, translation, code, creativity |
| 03 | LLM Limitations | What LLMs can't do — no memory, no math, no real-time data, no actions |
| 04 | From LLM to Agent | See the same task done by a plain LLM vs an "agent" with tools |
| 05 | The Four Building Blocks | Experience each agent component — brain, memory, tools, planning |
| 06 | Challenge: Design Your Agent | Given a scenario, design what an agent needs to solve it |

## How to Run

```bash
cd hands-on/session-1

# Run any lab
python lab01_meet_your_llm.py

# Run with solutions to compare
python solutions/lab01_meet_your_llm.py
```

## Tips for First-Timers

- **Don't worry about the code details yet** — Sessions 3-4 teach the patterns and framework. For now, focus on *what the LLM does*, not how the code works.
- **The LLM is running locally** — your questions never leave your machine. Feel free to ask anything!
- **Small model, big ideas** — we use `llama3.2:1b` (a small model). Larger models are even more capable, but this is enough to learn the concepts.
- **Experiment!** — change the questions, try weird inputs, break things. That's how you learn.

## Estimated Time

~40-50 minutes for all labs (including experimentation)
