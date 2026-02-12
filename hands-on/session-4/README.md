# Session 4: LangChain Fundamentals — Hands-on Labs

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

# Verify LangChain is installed
python -c "import langchain; print(f'LangChain {langchain.__version__}')"
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Hello LangChain | Connect to Ollama, first `.invoke()`, explore the response object |
| 02 | Message Types | SystemMessage, HumanMessage — control LLM behavior |
| 03 | Prompt Templates | ChatPromptTemplate — reusable prompts with variables |
| 04 | Your First Chain | LCEL pipe syntax — `prompt \| llm \| parser` |
| 05 | Output Parsers | StrOutputParser, JsonOutputParser, PydanticOutputParser |
| 06 | Streaming & Batch | `.stream()` for real-time output, `.batch()` for bulk processing |
| 07 | Chain Composition | Connect multiple chains — output of one feeds into the next |
| 08 | Challenge: Build a Mini App | Combine everything into a working application |

## How to Run

```bash
cd hands-on/session-4

# Run any lab
python lab01_hello_langchain.py

# Run with solutions to compare
python solutions/lab01_hello_langchain.py
```

## Tips

- **Read the comments** — each lab file explains what's happening step by step
- **Look for `# TODO` markers** — these are the parts you need to fill in
- **Run frequently** — don't wait until you've written everything; run after each TODO
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change prompts, try different inputs, break things on purpose

## Estimated Time

~45-60 minutes for all labs (including experimentation)
