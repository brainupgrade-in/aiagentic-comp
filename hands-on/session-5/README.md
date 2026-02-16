# Session 5: Building RAG Applications — Hands-on Labs

## Prerequisites

- Day 1 cleanup is complete (`bash scripts/day1-cleanup.sh` — removes Ollama)
- Python virtual environment is activated
- **Groq API key** is set up (free at https://console.groq.com)

Verify your setup:
```bash
# Activate virtual environment (if not already)
source ~/.venv/bin/activate

# Set your Groq API key (get one at https://console.groq.com)
export GROQ_API_KEY="your-key-here"

# Or add it to your .env file
echo 'GROQ_API_KEY=your-key-here' >> .env

# Install sentence-transformers for embeddings (if not already installed)
pip install sentence-transformers

# Verify everything is ready
python -c "from langchain_groq import ChatGroq; print('Groq ready!')"
python -c "import chromadb; print(f'ChromaDB {chromadb.__version__}')"
python -c "from langchain_huggingface import HuggingFaceEmbeddings; print('Embeddings ready!')"
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Hello Groq | Switch from Ollama to Groq API, verify connection, compare model quality |
| 02 | Understanding Embeddings | Generate embeddings, measure similarity, see how meaning is captured |
| 03 | ChromaDB Basics | Create collections, add documents with metadata, run similarity searches |
| 04 | Document Loading & Splitting | Load text, split into chunks, understand chunk size and overlap |
| 05 | LangChain + ChromaDB | Use LangChain's Chroma wrapper, create retrievers, search documents |
| 06 | Your First RAG Chain | Build a RAG chain with LCEL — retriever + prompt + LLM |
| 07 | RAG with Citations | Add source citations, format documents, filter by metadata |
| 08 | Challenge: Company Q&A Bot | Build a complete RAG-powered knowledge base from scratch |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-5/
├── lab01_groq_setup.ipynb                 ← Start here
├── lab02_embeddings.ipynb
├── lab03_chromadb_basics.ipynb
├── lab04_document_loading.ipynb
├── lab05_vector_store_langchain.ipynb
├── lab06_rag_chain.ipynb
├── lab07_rag_citations.ipynb
├── lab08_challenge.ipynb
└── solutions/                             ← Completed versions
    ├── lab01_groq_setup.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the Python kernel (`~/.venv/bin/python`)
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Important: Groq API Key

Every lab in this session uses the Groq API (except Lab 02 which only uses local embeddings).
Make sure your `GROQ_API_KEY` environment variable is set before running labs.

```bash
# Quick check
echo $GROQ_API_KEY
```

## Tips

- **Read the markdown cells** — each lab explains what's happening step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck
- **Experiment!** — change queries, add your own documents, try different chunk sizes
- **No PDFs needed** — all labs use inline sample data so they're fully self-contained

## Estimated Time

~60-75 minutes for all labs (including experimentation)
