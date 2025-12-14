# CompreRAG 🎓

> *A vibe-coded RAG agent built during exam season to turn course materials into your personal study assistant*

## Overview

CompreRAG is an educational tool that ingests course materials (lecture slides, past exams, notes) to predict potential exam questions and provide tailored answers. Born out of necessity during a tight comprehensive exam schedule, this project was rapidly prototyped in a day to help students study smarter, not harder.

**⚠️ Disclaimer**: This was a fun, experimental project "vibe-coded" during exam prep—not a production-grade application. Use it as a learning tool or starting point for your own RAG implementations!

### Architecture Modes

This project has **two implementations**:

1. **🏠 Standalone Local Mode** (Recommended for privacy & zero cost)
   - Simple Python scripts (`main.py`, `query.py`)
   - Uses: **Ollama** (LLM) + **ChromaDB** (vector store)
   - No API keys, no cloud, no costs
   - Perfect for personal study materials

2. **☁️ Full-Stack Mode** (Experimental cloud MVP)
   - FastAPI backend + Next.js frontend
   - Uses: **OpenAI** (LLM) + **Pinecone** (vectors) + **Supabase** (DB) + **MinIO** (storage)
   - Requires API keys and local/cloud deployment
   - Multi-user support with authentication

## 🏗️ Architecture

### Mode 1: Standalone Local (Recommended)

| Component | Technology | Notes |
|-----------|-----------|-------|
| **LLM** | Ollama (Llama 3.2) | localhost:11434 |
| **Vector Store** | ChromaDB | Persistent local storage |
| **Embeddings** | all-MiniLM-L6-v2 | Runs locally via sentence-transformers |
| **Interface** | CLI (Python scripts) | `main.py` or `query.py` |

**Data Flow:**
```
PDF/DOCX → Document Ingestor → Text Chunks → Embeddings → ChromaDB
                                                                ↓
User Query → Embedding → Vector Search → Context → Ollama → Answer
```

### Mode 2: Full-Stack Cloud MVP

| Component | Technology | Port/Location |
|-----------|-----------|---------------|
| **Backend** | FastAPI | localhost:8000 |
| **Frontend** | Next.js | localhost:3000 |
| **LLM** | OpenAI GPT-4 | API |
| **Vector Store** | Pinecone | Cloud/API |
| **Database** | Supabase PostgreSQL | Cloud/Local |
| **Storage** | MinIO (S3) | localhost:9000 |
| **Auth** | Supabase Auth | Included |

**Data Flow:**
```
Browser → Next.js API → FastAPI → MinIO (file storage)
                           ↓
                       Pinecone (vectors) + OpenAI (LLM)
                           ↓
                       Supabase (metadata)

## ✨ Features

### Core Features (Both Modes)
- 📄 **Multi-Format Support**: Ingest PDFs, DOCX, and TXT files
- 🔍 **Semantic Search**: Vector-based retrieval for relevant context
- 💬 **Interactive Q&A**: Natural language queries about your materials
- 🎯 **Exam Prediction**: Analyzes patterns in past papers to predict questions
- 📚 **Course Summarization**: Get summaries of topics from lecture materials

### Standalone Mode Benefits
- � **100% Local**: No data leaves your computer
- 💰 **Zero Cost**: No API fees, ever
- 🔒 **Complete Privacy**: Perfect for sensitive course materials
- ⚡ **No Rate Limits**: Query as much as you want
- 🚀 **Simple Setup**: Just Python + Ollama, no complex config

### Full-Stack Mode Features
- 🔐 **User Authentication**: Multi-user support with Supabase Auth
- ⚡ **Real-time Updates**: Live processing status
- � **Data Isolation**: Row Level Security per user
- 🌐 **Web Interface**: Modern React/Next.js UI
- 🐳 **MinIO Storage**: S3-compatible object storage

## 🚀 Quick Start

Choose your adventure:

### Option A: Standalone Local Mode (Easiest!)

**Prerequisites:**
- Python 3.8+
- Ollama

**Setup:**

1. Install Ollama:
   ```bash
   # Linux/macOS
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Or download from: https://ollama.com/download
   ```

2. Pull a model:
   ```bash
   ollama pull llama3.2:1b  # Fast, lightweight (1.3GB)
   # or
   ollama pull llama3.2     # Better quality (2GB)
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your PDFs to `data/` folder:
   ```bash
   mkdir -p data/slides data/pyqs
   # Copy your lecture slides to data/slides/
   # Copy past exam papers to data/pyqs/
   ```

5. Run ingestion:
   ```bash
   python main.py
   ```

6. Query interactively:
   ```bash
   python query.py
   ```

**That's it!** 🎉 No API keys, no configuration files, zero cost.

---

### Option B: Full-Stack Mode (Advanced)

**Prerequisites:**
- Python 3.8+
- Node.js 18+
- Docker (for MinIO)
- API keys (OpenAI, Pinecone, Supabase)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from template:
   ```bash
   cp .env.example .env
   ```
   Then fill in your API keys.

5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file from template:
   ```bash
   cp .env.example .env.local
   ```
   Then fill in your Supabase keys. The `PYTHON_BACKEND_URL` defaults to `http://localhost:8000`.

5. Run the development server:
   ```bash
   npm run dev
   ```

6. Open [http://localhost:3000](http://localhost:3000)

### MinIO Setup (Full-Stack Mode Only)

1. Start MinIO container:
   ```bash
   docker run -d \
     -p 9000:9000 \
     -p 9001:9001 \
     --name minio \
     -e "MINIO_ROOT_USER=minioadmin" \
     -e "MINIO_ROOT_PASSWORD=minioadmin" \
     -v minio_data:/data \
     minio/minio server /data --console-address ":9001"
   ```

2. Access MinIO console at [http://localhost:9001](http://localhost:9001)

3. Create a bucket called `documents`

## 🌐 Deployment

### Standalone Mode (Default)
Runs entirely on your local machine:
- **LLM**: Ollama on localhost:11434
- **Vector Store**: ChromaDB in `./chroma_db/` directory
- **Storage**: Direct filesystem access

**Why go local?**
- 💰 Zero cost - no API fees
- 🔒 Complete privacy - data never leaves your machine
- ⚡ No network latency
- 🚫 No rate limits
- 📚 Perfect for sensitive course materials

### Full-Stack Mode
Can be deployed locally or to cloud:

**Local Development:**
- Backend: localhost:8000
- Frontend: localhost:3000
- MinIO: localhost:9000
- Supabase: Cloud or local instance
- Pinecone: Cloud API
- OpenAI: API

**Cloud Options (not implemented in current codebase):**
- Backend: Can deploy to Render, Railway, or similar
- Frontend: Can deploy to Vercel, Netlify
- See [DEPLOY.md](./DEPLOY.md) for cloud deployment ideas

## Project Structure

```
CompreRAG/
├── 🏠 Standalone Mode (Root Level)
│   ├── main.py                    # Ingest PDFs & build vector DB
│   ├── query.py                   # Interactive CLI query interface
│   ├── requirements.txt           # Minimal deps (Ollama, ChromaDB)
│   ├── data/
│   │   ├── slides/                # Lecture slides (PDFs)
│   │   └── pyqs/                  # Past year questions (PDFs)
│   ├── chroma_db/                 # ChromaDB persistent storage
│   └── src/
│       ├── ingestion/
│       │   ├── documents.py       # PDF/DOCX ingestion
│       │   └── pyq.py             # Past paper ingestion
│       ├── embeddings/
│       │   └── vector_store.py    # ChromaDB manager
│       ├── agent/
│       │   └── orchestrator.py    # Query routing & Ollama integration
│       └── feedback/
│           └── loop.py            # User feedback collection
│
├── ☁️ Full-Stack Mode
│   ├── backend/
│   │   ├── main.py                # FastAPI application
│   │   ├── auth.py                # JWT authentication
│   │   ├── database.py            # Supabase client
│   │   ├── storage.py             # MinIO S3 manager
│   │   ├── processor.py           # Doc processing + Pinecone
│   │   ├── models.py              # Pydantic models
│   │   ├── config.py              # Environment config
│   │   └── requirements.txt       # Backend deps
│   └── frontend/
│       ├── src/
│       │   ├── app/
│       │   │   ├── page.tsx       # Login page
│       │   │   ├── dashboard/     # Document dashboard
│       │   │   ├── upload/        # Upload interface
│       │   │   ├── chat/          # Chat interface
│       │   │   └── api/           # Next.js API routes
│       │   └── lib/
│       │       ├── supabase.ts    # Supabase client
│       │       └── api.ts         # API helper
│       └── package.json
│
└── 📚 Documentation
    ├── README.md                  # This file
    ├── SETUP.md                   # Ollama installation guide
    ├── USAGE.md                   # Usage instructions
    ├── DEPLOY.md                  # Cloud deployment guide
    └── QnA.md                     # Sample Q&A examples
```

## 🤝 Contributing

This was a quick experimental project, but contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Use it as inspiration for your own projects

## 📝 License

MIT

## 📚 Additional Resources

- **Usage Guide**: [USAGE.md](./USAGE.md) - How to use the application
- **Q&A Bank**: [QnA.md](./QnA.md) - Sample questions and answers
- **Cloud Setup**: [DEPLOY.md](./DEPLOY.md) - Full deployment guide
- **Local Setup (v1.0)**: [SETUP.md](./SETUP.md) - Ollama installation and local-only setup

## 💡 Project Origin Story

This project was born during a particularly stressful comprehensive exam period. With mountains of lecture slides, past papers, and notes to review, the idea struck: *"What if I could just ask my materials what's going to be on the exam?"*

In true developer fashion, I spent a day vibe-coding this RAG agent instead of studying traditionally. The irony? It actually helped. 

**The Build:**
- Started with a simple standalone script using Ollama + ChromaDB (fully local, zero cost)
- Got carried away and added a full-stack version with FastAPI, Next.js, and MinIO
- Ended up with two implementations because why not? 🤷

**The Stack:**
- 🧠 Document ingestion and chunking
- 🔍 Semantic search with vector embeddings
- 💬 Conversational AI via Ollama (local) or OpenAI (API)
- 🎯 Pattern analysis for exam prediction
- 🗄️ ChromaDB (local) or Pinecone (cloud) for vectors
- 🐳 MinIO for S3-compatible storage (full-stack mode only)

**Was it over-engineered for a study tool?** Absolutely.  
**Did it work?** Surprisingly well.  
**Would I recommend this approach during finals?** Probably not, but here we are.  
**Which mode should you use?** Start with standalone—it's simpler, private, and free.  
**Is your data safe?** In standalone mode, 100%—it never leaves your computer.

---

*Built with ☕, late nights, and the power of procrastination*

