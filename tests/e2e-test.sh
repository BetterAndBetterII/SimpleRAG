#!/bin/bash

# 设置环境变量
export BACKEND_URL=http://localhost:8000
export FRONTEND_URL=http://localhost:3000

# 安装依赖
echo "Installing dependencies..."
cd integration
pip install -r requirements.txt
playwright install chromium

# 运行API测试
echo "Running API tests..."
pytest test_api.py -v

# 运行UI测试
echo "Running UI tests..."
pytest test_ui.py -v

# 检查测试结果
if [ $? -eq 0 ]; then
  echo "All tests passed!"
  exit 0
else
  echo "Tests failed!"
  exit 1
fi

