from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.query import QueryRequest, QueryResponse
from app.services.index_service import IndexService

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def query_documents(
    query_request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    查询文档并返回答案
    """
    try:
        index_service = IndexService(db)
        result = index_service.query(
            query_text=query_request.query,
            top_k=query_request.top_k,
            rerank=query_request.rerank
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

