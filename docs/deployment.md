# SimpleRAG 部署指南

本文档提供了部署 SimpleRAG 应用的详细步骤，包括本地开发环境和生产环境的部署方法。

## 目录

- [前提条件](#前提条件)
- [本地开发环境部署](#本地开发环境部署)
- [生产环境部署](#生产环境部署)
- [环境变量配置](#环境变量配置)
- [SSL 证书配置](#ssl-证书配置)
- [故障排除](#故障排除)

## 前提条件

部署 SimpleRAG 应用需要以下软件和工具：

- Docker 和 Docker Compose
- Git
- 对于生产环境：域名和 SSL 证书

## 本地开发环境部署

### 1. 克隆仓库

```bash
git clone https://github.com/BetterAndBetterII/SimpleRAG.git
cd SimpleRAG
```

### 2. 配置环境变量

复制示例环境变量文件：

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

根据需要修改环境变量。

### 3. 使用 Docker Compose 启动应用

```bash
docker-compose up -d
```

或者使用部署脚本：

```bash
./deploy-local.sh
```

### 4. 访问应用

- 前端：http://localhost:3000
- 后端 API：http://localhost:8000/api
- API 文档：http://localhost:8000/api/docs

## 生产环境部署

### 1. 准备服务器

确保服务器已安装 Docker 和 Docker Compose。

### 2. 配置环境变量

创建 `.env` 文件，包含以下环境变量：

```
POSTGRES_PASSWORD=your_secure_password
DOMAIN=your-domain.com
GITHUB_REPOSITORY=BetterAndBetterII/SimpleRAG
```

### 3. 配置 SSL 证书

将 SSL 证书文件放置在 `nginx/ssl` 目录中：

```bash
mkdir -p nginx/ssl
# 复制证书文件
cp /path/to/fullchain.pem nginx/ssl/
cp /path/to/privkey.pem nginx/ssl/
```

### 4. 部署应用

使用 Docker Compose 部署：

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. 配置 CI/CD

如果使用 GitHub Actions 进行自动部署，需要在 GitHub 仓库中配置以下 Secrets：

- `DEPLOY_SSH_KEY`：用于 SSH 连接到服务器的私钥
- `DEPLOY_HOST`：服务器主机名或 IP 地址
- `DEPLOY_USER`：SSH 用户名

## 环境变量配置

### 后端环境变量

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| DATABASE_URL | PostgreSQL 数据库连接 URL | postgresql://postgres:postgres@db:5432/simplerag |
| POSTGRES_USER | PostgreSQL 用户名 | postgres |
| POSTGRES_PASSWORD | PostgreSQL 密码 | postgres |
| POSTGRES_DB | PostgreSQL 数据库名 | simplerag |
| POSTGRES_HOST | PostgreSQL 主机名 | db |
| POSTGRES_PORT | PostgreSQL 端口 | 5432 |
| DEBUG | 是否启用调试模式 | True/False |
| API_PREFIX | API 路径前缀 | /api |
| BACKEND_CORS_ORIGINS | 允许的 CORS 来源 | ["http://localhost:3000"] |
| EMBEDDING_MODEL | 使用的嵌入模型 | text-embedding-ada-002 |

### 前端环境变量

| 变量名 | 描述 | 示例值 |
|--------|------|--------|
| VITE_API_URL | 后端 API URL | http://localhost:8000/api |

## SSL 证书配置

对于生产环境，建议使用 Let's Encrypt 获取免费的 SSL 证书：

```bash
certbot certonly --standalone -d your-domain.com
```

然后将证书文件复制到 `nginx/ssl` 目录：

```bash
cp /etc/letsencrypt/live/your-domain.com/fullchain.pem nginx/ssl/
cp /etc/letsencrypt/live/your-domain.com/privkey.pem nginx/ssl/
```

## 故障排除

### 常见问题

1. **数据库连接失败**

   检查数据库环境变量是否正确配置，以及数据库容器是否正常运行。

   ```bash
   docker-compose logs db
   ```

2. **前端无法连接后端 API**

   检查 CORS 配置和 API URL 是否正确。

   ```bash
   docker-compose logs frontend
   docker-compose logs backend
   ```

3. **SSL 证书问题**

   确保证书文件路径正确，并且 Nginx 配置正确引用了这些文件。

   ```bash
   docker-compose logs nginx
   ```

如果遇到其他问题，请查看各个服务的日志：

```bash
docker-compose logs [service_name]
```

