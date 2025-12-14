import os
from typing import List
import io
from pypdf import PdfReader
from docx import Document as DocxDocument
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from config import settings

# Initialize Pinecone
pc = Pinecone(api_key=settings.PINECONE_API_KEY)
index = pc.Index(settings.PINECONE_INDEX_NAME)

# Initialize Embedding Model
# using a small, fast model for MVP
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_from_pdf(file_content: bytes) -> str:
    pdf_file = io.BytesIO(file_content)
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_content: bytes) -> str:
    docx_file = io.BytesIO(file_content)
    doc = DocxDocument(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def generate_embeddings(chunks: List[str]) -> List[List[float]]:
    embeddings = model.encode(chunks)
    return embeddings.tolist()

def process_document(file_content: bytes, filename: str, document_id: str, user_id: str):
    try:
        # 1. Extract Text
        if filename.endswith('.pdf'):
            text = extract_text_from_pdf(file_content)
        elif filename.endswith('.docx'):
            text = extract_text_from_docx(file_content)
        else:
            text = file_content.decode('utf-8') # Assume txt

        # 2. Chunk Text
        chunks = chunk_text(text)

        # 3. Generate Embeddings
        embeddings = generate_embeddings(chunks)

        # 4. Upsert to Pinecone
        vectors = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{document_id}_{i}"
            metadata = {
                "text": chunk,
                "document_id": document_id,
                "user_id": user_id,
                "filename": filename
            }
            vectors.append({
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            })
        
        # Batch upsert
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch, namespace=user_id)

        return len(chunks)

    except Exception as e:
        print(f"Error processing document: {e}")
        raise e

def query_pinecone(query: str, user_id: str, top_k: int = 5):
    query_embedding = model.encode([query])[0].tolist()
    results = index.query(
        namespace=user_id,
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results
