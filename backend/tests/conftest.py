import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.ext.declarative import declarative_base

from app.main import app
from app.db.session import Base, get_db

# 测试数据库URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/test_simplerag"


@pytest.fixture(scope="session")
def test_db_engine():
    """创建测试数据库引擎"""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db_engine):
    """创建测试数据库会话"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """创建测试客户端"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

