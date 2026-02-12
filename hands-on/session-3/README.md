# Session 3: Reasoning, Planning & Tool Use — Hands-on Labs

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

# Quick test
python -c "from langchain_ollama import ChatOllama; print('Ready!')"
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Chain-of-Thought | How "think step by step" improves LLM accuracy |
| 02 | ReAct Pattern | The Thought → Action → Observation loop |
| 03 | Tree-of-Thought | Explore multiple solutions, evaluate, pick the best |
| 04 | Reflection | Generate → Critique → Improve cycle |
| 05 | Tool Calling | Build Python tools an LLM can decide to use |
| 06 | Memory | Stateless vs stateful — why conversation history matters |
| 07 | Challenge: Mini Agent | Combine reasoning + tools + memory into one agent |

## How to Run

```bash
cd hands-on/session-3

# Run any lab
python lab01_chain_of_thought.py

# Run with solutions to compare
python solutions/lab01_chain_of_thought.py
```

## What Makes This Session Different

Session 3 labs focus on **agentic AI patterns** — the reasoning strategies, tool use concepts, and memory systems that make agents intelligent. These are the patterns you'll implement with LangChain in Session 4 and beyond.

We use a local LLM (Ollama) to keep things simple and focused on the concepts, not the framework.

## Tips

- **Read the output carefully** — the key learning is seeing HOW the LLM responds differently with each pattern
- **Compare with/without** — most labs show the "without" approach first, then the improved version
- **Experiment with prompts** — small changes in prompts can dramatically change results
- **Look for `# TODO` markers** — these are exercises for you to try

## Estimated Time

~45-60 minutes for all labs (including experimentation)
