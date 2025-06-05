import os
import pytest
import requests
from playwright.sync_api import sync_playwright

# 测试环境配置
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:3000")


@pytest.fixture(scope="session")
def backend_api():
    """后端API基础URL"""
    return f"{BACKEND_URL}/api"


@pytest.fixture(scope="session")
def frontend_url():
    """前端URL"""
    return FRONTEND_URL


@pytest.fixture(scope="session")
def api_client():
    """API客户端会话"""
    session = requests.Session()
    yield session
    session.close()


@pytest.fixture(scope="function")
def browser():
    """Playwright浏览器实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    """Playwright页面实例"""
    page = browser.new_page()
    yield page
    page.close()

