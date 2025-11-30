from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import uuid
import io
from datetime import datetime
from openai import OpenAI


from config import settings
from database import supabase
from storage import storage_manager
from models import QueryRequest, QueryResponse, Document
from auth import get_current_user
from processor import process_document, query_pinecone

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

app = FastAPI(title="RAG Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # TODO: Restrict to Vercel domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "RAG Agent API is running"}

async def background_process_document(file_content: bytes, filename: str, document_id: str, user_id: str):
    try:
        # Update status to processing
        supabase.table("documents").update({"status": "processing"}).eq("id", document_id).execute()
        
        # Process
        chunk_count = process_document(file_content, filename, document_id, user_id)
        
        # Update status to completed
        supabase.table("documents").update({
            "status": "completed",
            "chunk_count": chunk_count,
            "progress": 100
        }).eq("id", document_id).execute()
        
    except Exception as e:
        print(f"Background processing failed: {e}")
        supabase.table("documents").update({
            "status": "failed",
            "progress": 0
        }).eq("id", document_id).execute()

@app.post("/upload", response_model=Document)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):
    # 1. Validate file
    if not file.filename.endswith(('.pdf', '.docx', '.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # 2. Read file content
    content = await file.read()
    if len(content) > 10 * 1024 * 1024: # 10MB limit
        raise HTTPException(status_code=400, detail="File too large")

    # 3. Create DB record
    document_id = str(uuid.uuid4())
    file_path = f"{user_id}/{document_id}/{file.filename}"
    
    try:
        # Upload to MinIO
        storage_manager.upload_file(io.BytesIO(content), file_path)

        # Insert into Supabase - bypass RLS by using service role or admin client
        # For now, we'll disable RLS check by using the service key
        doc_data = {
            "id": document_id,
            "user_id": user_id,  # This is a string UUID from JWT
            "filename": file.filename,
            "storage_path": file_path,
            "status": "uploading",
            "created_at": datetime.utcnow().isoformat()
        }

        print(f"Attempting to insert document: {doc_data}")
        print(f"User ID type: {type(user_id)}, value: {user_id}")

        # The issue is RLS policies - we need to use service_role key or set the user context
        data = supabase.table("documents").insert(doc_data).execute()
        print(f"Insert successful: {data}")

        # Trigger background processing
        background_tasks.add_task(background_process_document, content, file.filename, document_id, user_id)

        return data.data[0]

    except Exception as e:
        print(f"Upload error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def query_document(
    request: QueryRequest,
    user_id: str = Depends(get_current_user)
):
    try:
        print(f"Query request: {request.query}, user_id: {user_id}")

        # Search Pinecone - retrieve relevant chunks
        results = query_pinecone(request.query, user_id, top_k=7)
        print(f"Pinecone results: {results}")

        sources = []
        context_text = ""

        for match in results['matches']:
            if request.document_ids and match['metadata']['document_id'] not in request.document_ids:
                continue

            sources.append(match['metadata']['text'])
            context_text += match['metadata']['text'] + "\n\n"

        print(f"Found {len(sources)} relevant chunks")

        # Generate Answer using OpenAI
        if not context_text:
            return QueryResponse(
                answer="I couldn't find any relevant information in your documents to answer this question.",
                sources=[]
            )

        # Create messages for OpenAI
        messages = [
            {
                "role": "system",
                "content": """You are an expert assistant that provides comprehensive, well-formatted answers based on the provided document context.

Guidelines:
1. Analyze all provided context carefully
2. Synthesize information from multiple chunks if needed
3. Provide detailed, well-structured answers using clear formatting:
   - Use **bold** for key terms and important concepts
   - Use bullet points (•) or numbered lists for clarity
   - Use headings (###) only when truly necessary for organization
   - Do NOT use horizontal rules (---) or excessive separators
4. If the exact answer isn't in the context, use related information to provide the best possible response
5. Only say information is missing if truly no relevant context exists
6. Keep formatting clean and professional"""
            },
            {
                "role": "user",
                "content": f"""Based on the following document excerpts, please answer the question thoroughly:

Context:
{context_text}

Question: {request.query}

Provide a clear, well-formatted answer:"""
            }
        ]

        print("Calling OpenAI GPT-4.1...")
        # Call OpenAI
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000  # Increased for longer responses
        )

        answer = response.choices[0].message.content
        print(f"OpenAI response received, length: {len(answer)}")

        # Check if response was truncated
        if response.choices[0].finish_reason == 'length':
            print("WARNING: Response was truncated due to max_tokens limit")

        return QueryResponse(answer=answer, sources=sources)

    except Exception as e:
        print(f"Query error details: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents", response_model=List[Document])
async def list_documents(user_id: str = Depends(get_current_user)):
    try:
        data = supabase.table("documents").select("*").eq("user_id", user_id).execute()
        return data.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{document_id}")
async def delete_document(document_id: str, user_id: str = Depends(get_current_user)):
    try:
        # Get document to find storage path
        doc = supabase.table("documents").select("*").eq("id", document_id).eq("user_id", user_id).execute()
        if not doc.data:
            raise HTTPException(status_code=404, detail="Document not found")
            
        storage_path = doc.data[0]['storage_path']
        
        # Delete from MinIO
        storage_manager.delete_file(storage_path)
        
        # Delete from Supabase (Cascade should handle Pinecone if we had a webhook, but we don't)
        # So we should ideally delete from Pinecone too. 
        # For MVP, we'll just delete the DB record.
        supabase.table("documents").delete().eq("id", document_id).execute()
        
        return {"status": "deleted"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
