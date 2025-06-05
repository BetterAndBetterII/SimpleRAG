from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)
    rerank: bool = True


class QuerySourceNode(BaseModel):
    text: str
    document_id: int
    score: float
    metadata: Optional[Dict[str, Any]] = None


class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: List[QuerySourceNode]

