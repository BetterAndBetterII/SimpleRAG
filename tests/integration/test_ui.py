import os
import pytest
import tempfile
import time
from playwright.sync_api import expect


def test_frontend_loads(page, frontend_url):
    """测试前端页面加载"""
    page.goto(frontend_url)
    
    # 验证页面标题
    expect(page).to_have_title("SimpleRAG")
    
    # 验证页面包含预期的元素
    expect(page.locator("text=SimpleRAG")).to_be_visible()
    expect(page.locator("text=简单文件检索增强生成应用")).to_be_visible()
    
    # 验证上传区域存在
    expect(page.locator("text=上传文件")).to_be_visible()
    expect(page.locator("text=拖放文件到此处或点击选择文件")).to_be_visible()
    
    # 验证问答区域存在
    expect(page.locator("text=问答交互")).to_be_visible()
    expect(page.locator("text=开始提问以获取基于文档的回答")).to_be_visible()


def test_file_upload_workflow(page, frontend_url):
    """测试文件上传工作流程"""
    # 创建临时Markdown文件
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp:
        temp.write(b"# Test Document\n\nThis is a test document for UI testing.")
        temp_path = temp.name
    
    try:
        # 导航到前端页面
        page.goto(frontend_url)
        
        # 等待页面加载
        page.wait_for_load_state("networkidle")
        
        # 点击选择文件按钮
        upload_button = page.locator("text=选择文件")
        expect(upload_button).to_be_visible()
        
        # 上传文件
        with page.expect_file_chooser() as fc_info:
            upload_button.click()
        file_chooser = fc_info.value
        file_chooser.set_files(temp_path)
        
        # 验证文件名显示
        expect(page.locator(f"text={os.path.basename(temp_path)}")).to_be_visible()
        
        # 点击上传文件按钮
        page.locator("text=上传文件").click()
        
        # 等待上传完成
        page.wait_for_load_state("networkidle")
        
        # 验证文档列表中显示了上传的文件
        expect(page.locator("text=文档列表")).to_be_visible()
        expect(page.locator(f"text={os.path.basename(temp_path)}")).to_be_visible()
        
        # 清理：删除文档
        page.locator("[aria-label='Delete document']").first.click()
        page.wait_for_load_state("networkidle")
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)


def test_query_workflow(page, frontend_url):
    """测试问答工作流程"""
    # 创建临时Markdown文件
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as temp:
        temp.write(b"# Python Programming\n\nPython is a high-level, interpreted programming language. It was created by Guido van Rossum and first released in 1991.")
        temp_path = temp.name
    
    try:
        # 导航到前端页面
        page.goto(frontend_url)
        
        # 等待页面加载
        page.wait_for_load_state("networkidle")
        
        # 上传文件
        with page.expect_file_chooser() as fc_info:
            page.locator("text=选择文件").click()
        file_chooser = fc_info.value
        file_chooser.set_files(temp_path)
        
        # 点击上传文件按钮
        page.locator("text=上传文件").click()
        
        # 等待上传完成
        page.wait_for_load_state("networkidle")
        
        # 输入查询
        query_input = page.locator("textarea[placeholder='输入您的问题...']")
        query_input.fill("Who created Python?")
        
        # 发送查询
        page.locator("button:has(svg)").click()
        
        # 等待响应
        page.wait_for_load_state("networkidle")
        
        # 验证响应包含预期信息
        expect(page.locator("text=Guido van Rossum")).to_be_visible()
        
        # 清理：删除文档
        page.locator("[aria-label='Delete document']").first.click()
        page.wait_for_load_state("networkidle")
    
    finally:
        # 清理临时文件
        if os.path.exists(temp_path):
            os.unlink(temp_path)

