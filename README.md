# RAG Agent MVP - Cloud Deployment

A full-stack RAG (Retrieval-Augmented Generation) application with free-tier cloud deployment.

## Architecture

- **Backend**: FastAPI (Python) on Render
- **Frontend**: Next.js (TypeScript) on Vercel
- **Database**: Supabase (PostgreSQL + Auth + Realtime)
- **Vector Store**: Pinecone
- **File Storage**: Cloudflare R2

## Features

- User authentication (Supabase Auth)
- Document upload (PDF, DOCX, TXT)
- Real-time processing status updates
- Vector-based semantic search
- Chat interface for querying documents
- User data isolation with Row Level Security

## Local Development

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
   Then fill in your Supabase keys and backend URL.

4. Run the development server:
   ```bash
   npm run dev
   ```

5. Open [http://localhost:3000](http://localhost:3000)

## Deployment

See [DEPLOY.md](./DEPLOY.md) for detailed deployment instructions.

## Project Structure

```
rag_agent/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── auth.py           # JWT authentication
│   ├── database.py       # Supabase client
│   ├── storage.py        # R2 storage manager
│   ├── processor.py      # Document processing & embeddings
│   ├── models.py         # Pydantic models
│   ├── config.py         # Configuration
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx          # Login page
│   │   │   ├── dashboard/        # Document dashboard
│   │   │   ├── upload/           # Upload interface
│   │   │   └── chat/             # Chat interface
│   │   └── lib/
│   │       ├── supabase.ts       # Supabase client
│   │       └── api.ts            # Backend API client
│   └── package.json
└── DEPLOY.md
```

## License

MIT
