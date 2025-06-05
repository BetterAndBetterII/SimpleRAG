# SimpleRAG API 文档

本文档详细描述了SimpleRAG应用的API接口，包括端点、请求参数、响应格式和示例。

## 基本信息

- **基础URL**: `http://localhost:8000/api` (本地开发环境)
- **内容类型**: `application/json`，除非另有说明
- **认证**: 当前版本不需要认证

## API端点

### 文档管理

#### 获取所有文档

获取系统中的所有文档列表。

- **URL**: `/documents/`
- **方法**: `GET`
- **URL参数**:
  - `skip` (可选): 跳过的记录数，默认为0
  - `limit` (可选): 返回的最大记录数，默认为100

**响应**:

```json
[
  {
    "id": 1,
    "filename": "example.md",
    "content": "# Example Document\n\nThis is an example document.",
    "metadata": {
      "parsed_content": {...}
    },
    "created_at": "2025-06-05T10:30:00.000Z",
    "updated_at": "2025-06-05T10:30:00.000Z"
  },
  ...
]
```

**状态码**:
- `200 OK`: 成功返回文档列表

#### 获取单个文档

通过ID获取特定文档的详细信息。

- **URL**: `/documents/{document_id}`
- **方法**: `GET`
- **URL参数**:
  - `document_id`: 文档ID

**响应**:

```json
{
  "id": 1,
  "filename": "example.md",
  "content": "# Example Document\n\nThis is an example document.",
  "metadata": {
    "parsed_content": {...}
  },
  "created_at": "2025-06-05T10:30:00.000Z",
  "updated_at": "2025-06-05T10:30:00.000Z"
}
```

**状态码**:
- `200 OK`: 成功返回文档
- `404 Not Found`: 文档不存在

#### 上传文档

上传新文档到系统。

- **URL**: `/documents/upload`
- **方法**: `POST`
- **内容类型**: `multipart/form-data`
- **表单参数**:
  - `file`: 要上传的文件（支持.md和.txt格式）

**响应**:

```json
{
  "id": 1,
  "filename": "example.md",
  "content": "# Example Document\n\nThis is an example document.",
  "metadata": {
    "parsed_content": {...}
  },
  "created_at": "2025-06-05T10:30:00.000Z",
  "updated_at": "2025-06-05T10:30:00.000Z"
}
```

**状态码**:
- `200 OK`: 文件上传成功
- `400 Bad Request`: 请求格式错误
- `500 Internal Server Error`: 服务器处理文件时出错

#### 删除文档

删除系统中的特定文档。

- **URL**: `/documents/{document_id}`
- **方法**: `DELETE`
- **URL参数**:
  - `document_id`: 要删除的文档ID

**响应**:

```json
{
  "message": "文档已删除"
}
```

**状态码**:
- `200 OK`: 文档删除成功
- `404 Not Found`: 文档不存在

### 查询

#### 执行查询

基于已上传的文档执行查询。

- **URL**: `/query/`
- **方法**: `POST`
- **请求体**:

```json
{
  "query": "什么是Python?",
  "top_k": 5,
  "rerank": true
}
```

参数说明:
- `query`: 查询文本
- `top_k` (可选): 返回的最大相关文档数，默认为5
- `rerank` (可选): 是否对结果进行重排序，默认为true

**响应**:

```json
{
  "query": "什么是Python?",
  "answer": "Python是一种高级编程语言，由Guido van Rossum于1991年首次发布...",
  "sources": [
    {
      "text": "Python是一种高级编程语言，由Guido van Rossum创建...",
      "document_id": 1,
      "score": 0.95,
      "metadata": {
        "filename": "python_intro.md"
      }
    },
    ...
  ]
}
```

**状态码**:
- `200 OK`: 查询成功
- `400 Bad Request`: 请求格式错误
- `500 Internal Server Error`: 服务器处理查询时出错

## 错误处理

所有API错误响应都遵循以下格式:

```json
{
  "detail": "错误描述信息"
}
```

常见错误状态码:
- `400 Bad Request`: 请求参数错误
- `404 Not Found`: 请求的资源不存在
- `500 Internal Server Error`: 服务器内部错误

## 示例

### 上传文档示例

使用curl上传文档:

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/document.md"
```

### 查询示例

使用curl执行查询:

```bash
curl -X POST "http://localhost:8000/api/query/" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"query": "什么是Python?", "top_k": 3, "rerank": true}'
```

## 限制

- 文件上传大小限制: 10MB
- 查询长度限制: 1000字符
- 返回结果数量限制: 最多20个相关文档

