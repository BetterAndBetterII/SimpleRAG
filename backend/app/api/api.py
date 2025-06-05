from fastapi import APIRouter

from app.api.endpoints import documents, query

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(query.router, prefix="/query", tags=["query"])

