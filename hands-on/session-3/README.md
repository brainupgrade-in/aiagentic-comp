# Session 3: Reasoning, Planning & Tool Use — Hands-on Labs

## Prerequisites

- Setup complete (`source scripts/setup.sh` — verify with `bash scripts/setup.sh --verify`)
- Ollama is running with `llama3.2:1b` model pulled
- Python virtual environment is activated

Verify your setup:
```bash
# Check Ollama is running and model is available
ollama list

# Activate virtual environment (if not already)
source .venv/bin/activate

# Quick test
python -c "from langchain_ollama import ChatOllama; print('Ready')"
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

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-3/
├── lab01_chain_of_thought.ipynb         ← Start here
├── lab02_react_pattern.ipynb
├── lab03_tree_of_thought.ipynb
├── lab04_reflection.ipynb
├── lab05_tool_calling.ipynb
├── lab06_memory.ipynb
├── lab07_challenge.ipynb
└── solutions/                           ← Completed versions
    ├── lab01_chain_of_thought.ipynb
    ├── ...
    └── lab07_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## What Makes This Session Different

Session 3 labs focus on **agentic AI patterns** — the reasoning strategies, tool use concepts, and memory systems that make agents intelligent. These are the patterns you'll implement with LangChain in Session 4 and beyond.

We use a local LLM (Ollama) to keep things simple and focused on the concepts, not the framework.

## Tips

- **Read the output carefully** — the key learning is seeing HOW the LLM responds differently with each pattern
- **Compare with/without** — most labs show the "without" approach first, then the improved version
- **Experiment with prompts** — small changes in prompts can dramatically change results
- Look for `# TODO` markers and `"___"` placeholders — that's where you write code
- Compare your work with `solutions/` when done

## Estimated Time

~45-60 minutes for all labs (including experimentation)
