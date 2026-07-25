# Session 4: LangChain Fundamentals — Hands-on Labs

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
| 08 | Challenge: Technical Knowledge Assistant | Combine everything into a working application |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-4/
├── lab01_hello_langchain.ipynb          ← Start here
├── lab02_message_types.ipynb
├── lab03_prompt_templates.ipynb
├── lab04_first_chain.ipynb
├── lab05_output_parsers.ipynb
├── lab06_streaming_and_batch.ipynb
├── lab07_chain_composition.ipynb
├── lab08_challenge.ipynb
└── solutions/                           ← Completed versions
    ├── lab01_hello_langchain.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- **Read the markdown cells** — each lab explains what's happening step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change prompts, try different inputs, break things on purpose

## Estimated Time

~45-60 minutes for all labs (including experimentation)
