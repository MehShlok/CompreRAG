# 🎓 How to Use Your RAG Agent

## Quick Start

Your RAG system is ready! You have **two ways** to use it:

---

## 1️. Interactive Mode (Recommended for Q&A)

```bash
python query.py
```

This opens an interactive session where you can ask **any question** about your course materials!

### Example Questions:
- "Explain pipeline hazards and how to resolve them"
- "What are the differences between direct-mapped and set-associative cache?"
- "Predict 5 probable questions about MIPS instruction set"
- "Summarize the topics covered in Module 2"
- "What is branch prediction and why is it important?"


---

## 2️. Batch Mode (For Testing/Demo)

```bash
python main.py
```

This runs the full pipeline:
1. Re-ingests all PDFs from `data/slides` and `data/pyqs`
2. Updates the vector database
3. Runs 2 example queries

**Use this when:**
- You've added new PDF files
- You want to re-process everything from scratch

---

### Vector Database
- **Location:** `./chroma_db/`
- **Contents:** All your course PDFs, embedded and searchable
- **Persistent:** Survives restarts, no need to re-process

### Model
- **LLM:** Ollama llama3.2 (running locally)
- **Embeddings:** ChromaDB's default (all-MiniLM-L6-v2)

---


---


**Want to add more PDFs?**
1. Put PDFs in `data/slides/` or `data/pyqs/`
2. Run `python main.py` to re-ingest
3. Continue using `python query.py` for questions

**Slow responses?**
- First query is always slower (loading)
- Use a smaller model: `ollama pull llama3.2:1b`
- Edit `src/agent/orchestrator.py` line 7 to change model

---

## File Structure

```
rag_agent/
├── query.py           ← Use this for interactive Q&A
├── main.py            ← Use this to re-process PDFs
├── data/
│   ├── slides/        ← Put lecture PDFs here
│   └── pyqs/          ← Put exam PDFs here
├── chroma_db/         ← Vector database (auto-created)
└── src/
    ├── agent/
    ├── embeddings/
    └── ingestion/
```

---
