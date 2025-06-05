#!/bin/bash

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 运行API测试
echo "Running API integration tests..."
pytest test_api.py -v

# 运行UI测试
echo "Running UI integration tests..."
pytest test_ui.py -v

