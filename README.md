# Multi-Modal RAG Agentic System

## Overview
This project (currently ver 1.0) is an educational tool designed to ingest course materials (slides, past exams) to predict exam questions and provide tailored answers. It is designed to run **entirely locally** using Ollama for privacy and zero cost. This was 99% vibe-coded (Antigravity ftw) in 2 hrs to generate question banks similar to course material and PYQs (Check QnA.md as an ex. generated for Computer Architecture).

## Architecture
The system is built on the following pipelines:

### Phase 1: Data Ingestion ($D_2, D_3$)
- **Slides + Class Notes ($D_2$)**: Text extraction from PDFs.
- **PYQs ($D_3$)**: Text extraction for Past Year Questions (High Priority).
- **Audio/Video ($D_1$)**: *Experimental/Mock implementation included in codebase but currently disabled.*

### Phase 2: Embeddings & Storage
- **Vectorization**: `all-MiniLM-L6-v2` (Local, via ChromaDB).
- **Storage**: **ChromaDB** (Local persistent vector database).
- **Fusion**: Weighted retrieval (Higher weight for PYQs).

### Phase 3: AI Agent & Orchestrator
- **LLM**: **Ollama** (running locally, default: `llama3.2:1b`).
- **Framework**: Custom Python Orchestrator.
- **Context Management**: Context Window Compression.

### Phase 4: Prediction
- **Goal**: Generate "Probable Questions".
- **Method**: Semantic analysis and prompt engineering based on difficulty patterns.

## Quick Start

### Interactive Q&A
Ask questions directly to your course materials:
```bash
python query.py
```

### Generate Exam Q&A Bank
Create a comprehensive study guide with predicted questions:
```bash
python generate_qna_bank.py
```


## Setup
See [SETUP.md](./SETUP.md) for Ollama installation and setup instructions.



