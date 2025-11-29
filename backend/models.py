from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentBase(BaseModel):
    filename: str
    status: str
    progress: int = 0

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: str
    user_id: str
    created_at: datetime
    chunk_count: int = 0

    class Config:
        from_attributes = True

class QueryRequest(BaseModel):
    query: str
    document_ids: Optional[List[str]] = None

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
