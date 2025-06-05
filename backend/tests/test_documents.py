import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.document import Document


def test_get_documents_empty(client: TestClient, db_session: Session):
    """测试获取空文档列表"""
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_document_not_found(client: TestClient, db_session: Session):
    """测试获取不存在的文档"""
    response = client.get("/api/documents/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "文档未找到"}


def test_create_and_get_document(client: TestClient, db_session: Session):
    """测试创建和获取文档"""
    # 创建测试文件
    test_file_path = "/tmp/test_document.md"
    with open(test_file_path, "w") as f:
        f.write("# Test Document\n\nThis is a test document.")
    
    # 上传文件
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("test_document.md", f, "text/markdown")}
        )
    
    # 检查响应
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test_document.md"
    assert "# Test Document" in data["content"]
    
    # 获取文档
    document_id = data["id"]
    response = client.get(f"/api/documents/{document_id}")
    assert response.status_code == 200
    assert response.json()["id"] == document_id
    
    # 获取所有文档
    response = client.get("/api/documents/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # 删除测试文件
    os.remove(test_file_path)


def test_delete_document(client: TestClient, db_session: Session):
    """测试删除文档"""
    # 创建测试文件
    test_file_path = "/tmp/test_document.md"
    with open(test_file_path, "w") as f:
        f.write("# Test Document\n\nThis is a test document.")
    
    # 上传文件
    with open(test_file_path, "rb") as f:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("test_document.md", f, "text/markdown")}
        )
    
    # 获取文档ID
    document_id = response.json()["id"]
    
    # 删除文档
    response = client.delete(f"/api/documents/{document_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "文档已删除"}
    
    # 确认文档已删除
    response = client.get(f"/api/documents/{document_id}")
    assert response.status_code == 404
    
    # 删除测试文件
    os.remove(test_file_path)

