# SimpleRAG 开发指南

本文档提供了SimpleRAG项目的开发指南，包括环境设置、代码规范、架构概述和常见开发任务的说明。

## 目录

- [开发环境设置](#开发环境设置)
- [项目架构](#项目架构)
- [开发工作流](#开发工作流)
- [代码规范](#代码规范)
- [测试指南](#测试指南)
- [常见开发任务](#常见开发任务)
- [故障排除](#故障排除)

## 开发环境设置

### 后端开发环境

1. **安装Python 3.11+**

   确保您的系统已安装Python 3.11或更高版本。

2. **创建虚拟环境**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

4. **设置PostgreSQL和pgvector**

   安装PostgreSQL数据库和pgvector扩展。可以使用Docker简化此过程：

   ```bash
   docker run -d \
     --name postgres-pgvector \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=simplerag \
     -p 5432:5432 \
     ankane/pgvector:latest
   ```

5. **配置环境变量**

   复制示例环境文件并根据需要修改：

   ```bash
   cp .env.example .env
   # 编辑.env文件
   ```

6. **启动开发服务器**

   ```bash
   uvicorn app.main:app --reload
   ```

### 前端开发环境

1. **安装Node.js 20+**

   确保您的系统已安装Node.js 20或更高版本。

2. **安装pnpm**

   ```bash
   npm install -g pnpm
   ```

3. **安装依赖**

   ```bash
   cd frontend
   pnpm install
   ```

4. **配置环境变量**

   ```bash
   cp .env.example .env
   # 编辑.env文件
   ```

5. **启动开发服务器**

   ```bash
   pnpm dev
   ```

## 项目架构

### 后端架构

SimpleRAG后端采用分层架构：

1. **API层**：处理HTTP请求和响应
   - `app/api/`: 包含所有API路由和端点

2. **服务层**：实现业务逻辑
   - `app/services/`: 包含业务逻辑服务

3. **数据访问层**：处理数据库操作
   - `app/db/`: 数据库会话和连接管理
   - `app/models/`: SQLAlchemy ORM模型

4. **核心和工具**：
   - `app/core/`: 核心配置和设置
   - `app/utils/`: 工具函数和辅助方法

### 前端架构

前端采用组件化架构：

1. **组件**：
   - `src/components/ui/`: 基础UI组件
   - `src/components/`: 业务组件

2. **服务**：
   - `src/services/`: API服务和数据获取

3. **类型**：
   - `src/types/`: TypeScript类型定义

4. **工具**：
   - `src/lib/`: 工具函数和辅助方法

## 开发工作流

### 分支策略

- `main`: 主分支，包含稳定代码
- `develop`: 开发分支，用于集成功能
- `feature/*`: 功能分支，用于开发新功能
- `bugfix/*`: 修复分支，用于修复bug
- `release/*`: 发布分支，用于准备新版本

### 开发流程

1. 从`develop`分支创建新的功能分支
   ```bash
   git checkout develop
   git pull
   git checkout -b feature/new-feature
   ```

2. 开发新功能并提交更改
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

3. 推送分支并创建Pull Request
   ```bash
   git push origin feature/new-feature
   # 在GitHub上创建PR到develop分支
   ```

4. 代码审查和CI测试通过后合并

### 版本发布

1. 从`develop`分支创建发布分支
   ```bash
   git checkout develop
   git checkout -b release/v1.0.0
   ```

2. 更新版本号和CHANGELOG

3. 创建Pull Request到`main`分支

4. 合并后，在`main`分支上创建版本标签
   ```bash
   git checkout main
   git pull
   git tag v1.0.0
   git push origin v1.0.0
   ```

## 代码规范

### Python代码规范

- 遵循PEP 8风格指南
- 使用类型注解
- 使用docstring记录函数和类
- 最大行长度为88个字符
- 使用`black`格式化代码
- 使用`isort`排序导入

### TypeScript/React代码规范

- 使用ESLint和Prettier
- 使用函数组件和React Hooks
- 使用TypeScript类型定义
- 组件文件使用PascalCase命名
- 工具函数使用camelCase命名
- 使用模块化CSS或Tailwind CSS

## 测试指南

### 后端测试

1. **运行单元测试**

   ```bash
   cd backend
   pytest
   ```

2. **运行特定测试**

   ```bash
   pytest tests/test_documents.py
   ```

3. **生成测试覆盖率报告**

   ```bash
   pytest --cov=app tests/
   ```

### 前端测试

1. **运行单元测试**

   ```bash
   cd frontend
   pnpm test
   ```

2. **运行特定测试**

   ```bash
   pnpm test Button
   ```

3. **生成测试覆盖率报告**

   ```bash
   pnpm test:coverage
   ```

### 集成测试

1. **运行集成测试**

   ```bash
   cd tests/integration
   ./run_tests.sh
   ```

## 常见开发任务

### 添加新的API端点

1. 在`app/schemas/`中定义请求和响应模型
2. 在`app/services/`中实现业务逻辑
3. 在`app/api/endpoints/`中创建新的路由处理函数
4. 在`app/api/api.py`中注册新路由
5. 添加测试用例

### 添加新的前端组件

1. 在`src/components/`中创建新组件文件
2. 实现组件逻辑和样式
3. 在需要的地方导入和使用组件
4. 添加测试用例

### 添加新的数据库模型

1. 在`app/models/`中定义新的SQLAlchemy模型
2. 在`app/schemas/`中创建对应的Pydantic模型
3. 在`alembic/env.py`中导入新模型
4. 创建数据库迁移
   ```bash
   cd backend
   alembic revision --autogenerate -m "Add new model"
   alembic upgrade head
   ```

### 更新前端API服务

1. 在`src/types/`中更新或添加类型定义
2. 在`src/services/api.ts`中添加新的API调用函数

## 故障排除

### 常见问题

1. **数据库连接错误**

   检查`.env`文件中的数据库配置是否正确，以及PostgreSQL服务是否正在运行。

2. **pgvector扩展问题**

   确保PostgreSQL数据库已安装pgvector扩展：

   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

3. **前端API连接问题**

   检查`.env`文件中的`VITE_API_URL`是否正确设置，以及CORS配置是否允许前端域。

4. **依赖冲突**

   如果遇到依赖冲突，尝试清除缓存并重新安装：

   ```bash
   # 后端
   pip uninstall -r requirements.txt
   pip install -r requirements.txt

   # 前端
   rm -rf node_modules
   pnpm install
   ```

### 调试技巧

1. **后端调试**

   - 使用`print()`或Python的`logging`模块
   - 在开发模式下设置`DEBUG=True`
   - 使用Python调试器：`import pdb; pdb.set_trace()`

2. **前端调试**

   - 使用浏览器开发者工具
   - 使用React开发者工具扩展
   - 使用`console.log()`或`debugger`语句

3. **API调试**

   - 使用Swagger UI：访问`http://localhost:8000/api/docs`
   - 使用Postman或Insomnia测试API端点

## 贡献指南

1. 确保代码通过所有测试
2. 遵循代码规范
3. 为新功能添加测试
4. 更新相关文档
5. 提交有意义的提交消息

