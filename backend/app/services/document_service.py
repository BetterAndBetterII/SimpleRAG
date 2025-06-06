import os
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import markitdown

from app.models.document import Document
from app.schemas.document import DocumentCreate
from app.services.index_service import IndexService


class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.index_service = IndexService(db)

    def create_document(self, document: DocumentCreate) -> Document:
        """创建文档记录并将其添加到索引中"""
        db_document = Document(
            filename=document.filename,
            content=document.content,
            _metadata=document.metadata or {}
        )
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        
        # 将文档添加到索引中
        self.index_service.add_document(db_document)
        
        return db_document

    def get_document(self, document_id: int) -> Optional[Document]:
        """通过ID获取文档"""
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_documents(self, skip: int = 0, limit: int = 100) -> List[Document]:
        """获取所有文档"""
        return self.db.query(Document).offset(skip).limit(limit).all()

    def delete_document(self, document_id: int) -> bool:
        """删除文档及其索引"""
        document = self.get_document(document_id)
        if not document:
            return False
        
        # 从索引中删除文档
        self.index_service.delete_document(document_id)
        
        # 从数据库中删除文档
        self.db.delete(document)
        self.db.commit()
        return True

    def process_markdown_file(self, file_path: str, filename: str) -> Document:
        """处理Markdown文件并创建文档"""
        # 使用Markitdown解析Markdown文件
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析Markdown内容
        parsed_content = markitdown.parse(content)
        
        # 创建文档
        document = DocumentCreate(
            filename=filename,
            content=content,
            metadata={"parsed_content": parsed_content}
        )
        
        return self.create_document(document)

    def process_text_file(self, file_path: str, filename: str) -> Document:
        """处理文本文件并创建文档"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 创建文档
        document = DocumentCreate(
            filename=filename,
            content=content,
            metadata={}
        )
        
        return self.create_document(document)

