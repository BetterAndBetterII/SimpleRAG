import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 文档相关API
export const documentsApi = {
  // 获取所有文档
  getDocuments: async () => {
    const response = await api.get('/documents');
    return response.data;
  },

  // 获取单个文档
  getDocument: async (id: number) => {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },

  // 上传文档
  uploadDocument: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // 删除文档
  deleteDocument: async (id: number) => {
    const response = await api.delete(`/documents/${id}`);
    return response.data;
  },
};

// 查询相关API
export const queryApi = {
  // 执行查询
  query: async (query: string, top_k: number = 5, rerank: boolean = true) => {
    const response = await api.post('/query', {
      query,
      top_k,
      rerank,
    });
    return response.data;
  },
};

export default api;

