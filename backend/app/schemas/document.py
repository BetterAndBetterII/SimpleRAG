from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel


class DocumentBase(BaseModel):
    filename: str
    content: Optional[str] = None
    _metadata: Optional[Dict[str, Any]] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

