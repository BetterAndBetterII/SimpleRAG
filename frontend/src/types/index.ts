// 文档类型
export interface Document {
  id: number;
  filename: string;
  content: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  updated_at?: string;
}

// 查询源节点类型
export interface QuerySourceNode {
  text: string;
  document_id: number;
  score: number;
  metadata?: Record<string, unknown>;
}

// 查询响应类型
export interface QueryResponse {
  query: string;
  answer: string;
  sources: QuerySourceNode[];
}

// 查询请求类型
export interface QueryRequest {
  query: string;
  top_k?: number;
  rerank?: boolean;
}

