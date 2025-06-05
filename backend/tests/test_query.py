import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.services.index_service import IndexService


@pytest.fixture
def mock_index_service():
    """模拟IndexService"""
    with patch("app.api.endpoints.query.IndexService") as mock:
        instance = mock.return_value
        instance.query.return_value = {
            "query": "test query",
            "answer": "This is a test answer.",
            "sources": [
                {
                    "text": "Test source text",
                    "document_id": 1,
                    "score": 0.95,
                    "metadata": {"filename": "test_document.md"}
                }
            ]
        }
        yield mock


def test_query_documents(client: TestClient, db_session: Session, mock_index_service):
    """测试查询文档"""
    # 发送查询请求
    response = client.post(
        "/api/query/",
        json={
            "query": "test query",
            "top_k": 5,
            "rerank": True
        }
    )
    
    # 检查响应
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test query"
    assert data["answer"] == "This is a test answer."
    assert len(data["sources"]) == 1
    assert data["sources"][0]["document_id"] == 1
    assert data["sources"][0]["score"] == 0.95
    
    # 验证IndexService.query被调用
    mock_index_service.return_value.query.assert_called_once_with(
        query_text="test query",
        top_k=5,
        rerank=True
    )


def test_query_error_handling(client: TestClient, db_session: Session, mock_index_service):
    """测试查询错误处理"""
    # 设置模拟异常
    mock_index_service.return_value.query.side_effect = Exception("Test error")
    
    # 发送查询请求
    response = client.post(
        "/api/query/",
        json={
            "query": "test query",
            "top_k": 5,
            "rerank": True
        }
    )
    
    # 检查响应
    assert response.status_code == 500
    assert response.json() == {"detail": "查询失败: Test error"}

