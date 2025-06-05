import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.document_service import DocumentService

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    上传文档文件并处理
    """
    # 创建临时文件
    temp_file_path = f"/tmp/{file.filename}"
    try:
        # 保存上传的文件
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 创建文档服务
        document_service = DocumentService(db)
        
        # 根据文件类型处理文档
        filename = file.filename
        if filename.endswith(".md"):
            document = document_service.process_markdown_file(temp_file_path, filename)
        else:
            document = document_service.process_text_file(temp_file_path, filename)
        
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")
    finally:
        # 删除临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有文档
    """
    document_service = DocumentService(db)
    documents = document_service.get_documents(skip=skip, limit=limit)
    return documents


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    通过ID获取文档
    """
    document_service = DocumentService(db)
    document = document_service.get_document(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="文档未找到")
    return document


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    删除文档
    """
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id)
    if not success:
        raise HTTPException(status_code=404, detail="文档未找到")
    return {"message": "文档已删除"}

