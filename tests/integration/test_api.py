import os
import pytest
import tempfile
import time

# 测试文档上传API
def test_document_upload(api_client, backend_api):
    """测试文档上传API"""
    # 创建临时Markdown文件
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp:
        temp.write(b"# Test Document\n\nThis is a test document for API integration testing.")
        temp_path = temp.name
    
    try:
        # 上传文件
        with open(temp_path, "rb") as f:
            files = {"file": (os.path.basename(temp_path), f, "text/markdown")}
            response = api_client.post(f"{backend_api}/documents/upload", files=files)
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["filename"] == os.path.basename(temp_path)
        assert "# Test Document" in data["content"]
        
        # 保存文档ID用于后续测试
        document_id = data["id"]
        
        # 获取文档列表
        response = api_client.get(f"{backend_api}/documents")
        assert response.status_code == 200
        documents = response.json()
        assert len(documents) > 0
        assert any(doc["id"] == document_id for doc in documents)
        
        # 获取单个文档
        response = api_client.get(f"{backend_api}/documents/{document_id}")
        assert response.status_code == 200
        assert response.json()["id"] == document_id
        
        # 删除文档
        response = api_client.delete(f"{backend_api}/documents/{document_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "文档已删除"}
        
        # 确认文档已删除
        response = api_client.get(f"{backend_api}/documents/{document_id}")
        assert response.status_code == 404
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


# 测试查询API
def test_query_api(api_client, backend_api):
    """测试查询API"""
    # 创建临时Markdown文件
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp:
        temp.write(b"# Test Document\n\nThis is a test document for query testing. It contains information about Python programming.")
        temp_path = temp.name
    
    try:
        # 上传文件
        with open(temp_path, "rb") as f:
            files = {"file": (os.path.basename(temp_path), f, "text/markdown")}
            response = api_client.post(f"{backend_api}/documents/upload", files=files)
        
        document_id = response.json()["id"]
        
        # 等待索引建立
        time.sleep(2)
        
        # 执行查询
        query_data = {
            "query": "What is this document about?",
            "top_k": 3,
            "rerank": True
        }
        
        response = api_client.post(f"{backend_api}/query", json=query_data)
        
        # 验证响应
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "answer" in data
        assert "sources" in data
        assert len(data["sources"]) > 0
        
        # 清理
        api_client.delete(f"{backend_api}/documents/{document_id}")
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

