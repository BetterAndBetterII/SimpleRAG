# SimpleRAG

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/BetterAndBetterII/SimpleRAG/backend-tests.yml?label=backend)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/BetterAndBetterII/SimpleRAG/frontend-tests.yml?label=frontend)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/BetterAndBetterII/SimpleRAG/integration-tests.yml?label=integration)
![License](https://img.shields.io/github/license/BetterAndBetterII/SimpleRAG)

一个基于FastAPI+Llama-index+React+shadcn+pnpm+lucide-react+tailwind3+pgvector实现的简单文件RAG（检索增强生成）应用。

## 功能特点

- **文件上传与处理**：支持上传文件，使用Markitdown解析markdown文件
- **文档索引**：使用Llama-index进行文档解析和存储
- **向量检索**：基于pgvector实现高效的向量检索
- **重排序**：优化检索结果的相关性
- **简单问答**：基于检索结果进行问答交互

## 技术栈

### 后端
- **FastAPI**：高性能的Python Web框架
- **Llama-index**：文档索引和检索框架
- **pgvector**：PostgreSQL的向量扩展

### 前端
- **React**：用户界面库
- **shadcn**：UI组件库
- **pnpm**：包管理工具
- **lucide-react**：图标库
- **Tailwind CSS 3**：实用优先的CSS框架

## 快速开始

### 使用Docker Compose（推荐）

1. 克隆仓库
   ```bash
   git clone https://github.com/BetterAndBetterII/SimpleRAG.git
   cd SimpleRAG
   ```

2. 启动应用
   ```bash
   docker-compose up -d
   ```

3. 访问应用
   - 前端：http://localhost:3000
   - 后端API：http://localhost:8000/api
   - API文档：http://localhost:8000/api/docs

### 手动安装

#### 后端

1. 进入后端目录
   ```bash
   cd backend
   ```

2. 创建并激活虚拟环境
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或
   venv\Scripts\activate  # Windows
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑.env文件，设置数据库连接等
   ```

5. 启动后端服务
   ```bash
   uvicorn app.main:app --reload
   ```

#### 前端

1. 进入前端目录
   ```bash
   cd frontend
   ```

2. 安装依赖
   ```bash
   pnpm install
   ```

3. 配置环境变量
   ```bash
   cp .env.example .env
   # 编辑.env文件，设置API URL等
   ```

4. 启动前端服务
   ```bash
   pnpm dev
   ```

## 项目结构

```
SimpleRAG/
├── backend/                # 后端FastAPI应用
│   ├── app/                # 应用代码
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库模型和会话
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic模式
│   │   ├── services/       # 业务逻辑服务
│   │   └── utils/          # 工具函数
│   ├── tests/              # 后端测试
│   └── requirements.txt    # 依赖列表
│
├── frontend/               # 前端React应用
│   ├── public/             # 静态资源
│   ├── src/                # 源代码
│   │   ├── components/     # React组件
│   │   ├── services/       # API服务
│   │   ├── types/          # TypeScript类型定义
│   │   └── lib/            # 工具函数
│   └── package.json        # 依赖配置
│
├── docs/                   # 项目文档
│   ├── api.md              # API文档
│   ├── deployment.md       # 部署指南
│   └── development.md      # 开发指南
│
├── tests/                  # 集成测试
│   └── integration/        # 集成测试代码
│
├── .github/                # GitHub配置
│   └── workflows/          # GitHub Actions工作流
│
├── docker-compose.yml      # Docker Compose配置
└── README.md               # 项目说明
```

## 文档

- [API文档](./docs/api.md)
- [部署指南](./docs/deployment.md)
- [开发指南](./docs/development.md)

## 测试

### 后端测试

```bash
cd backend
pytest
```

### 前端测试

```bash
cd frontend
pnpm test
```

### 集成测试

```bash
cd tests/integration
./run_tests.sh
```

## CI/CD

项目使用GitHub Actions进行持续集成和部署：

- **后端测试**：每次提交时运行后端单元测试
- **前端测试**：每次提交时运行前端单元测试
- **集成测试**：后端和前端测试通过后运行集成测试
- **Docker构建**：构建并发布Docker镜像到GitHub Container Registry
- **自动部署**：发布新版本时自动部署到生产环境

## 贡献

欢迎贡献代码、报告问题或提出新功能建议。请遵循以下步骤：

1. Fork仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

[MIT](LICENSE)

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [Llama-index](https://www.llamaindex.ai/)
- [React](https://reactjs.org/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [pgvector](https://github.com/pgvector/pgvector)

