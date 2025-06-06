import { useState, useEffect } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { FileUpload } from './components/FileUpload';
import { DocumentList } from './components/DocumentList';
import { QueryChat } from './components/QueryChat';
import type { Document } from './types';
import { documentsApi } from './services/api';

// 创建 QueryClient 实例
const queryClient = new QueryClient();

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // 加载文档列表
  useEffect(() => {
    const fetchDocuments = async () => {
      try {
        setIsLoading(true);
        const docs = await documentsApi.getDocuments();
        setDocuments(docs);
        setError(null);
      } catch (err) {
        console.error('Error fetching documents:', err);
        setError('加载文档失败');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDocuments();
  }, []);

  // 处理文档上传成功
  const handleUploadSuccess = (document: Document) => {
    setDocuments([...documents, document]);
  };

  // 处理文档删除
  const handleDocumentDelete = (id: number) => {
    setDocuments(documents.filter(doc => doc.id !== id));
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-background">
        <header className="border-b">
          <div className="container mx-auto py-4">
            <h1 className="text-2xl font-bold">SimpleRAG</h1>
            <p className="text-muted-foreground">简单文件检索增强生成应用</p>
          </div>
        </header>
        
        <main className="container mx-auto py-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-8">
              <FileUpload onUploadSuccess={handleUploadSuccess} />
              
              {isLoading ? (
                <div className="text-center py-8">
                  <p className="text-muted-foreground">加载文档中...</p>
                </div>
              ) : error ? (
                <div className="text-center py-8">
                  <p className="text-destructive">{error}</p>
                </div>
              ) : (
                <DocumentList 
                  documents={documents} 
                  onDocumentDelete={handleDocumentDelete} 
                />
              )}
            </div>
            
            <div>
              <QueryChat />
            </div>
          </div>
        </main>
        
        <footer className="border-t mt-12">
          <div className="container mx-auto py-4 text-center text-sm text-muted-foreground">
            <p>SimpleRAG - 基于FastAPI+Llama-index+React+shadcn+pgvector实现</p>
          </div>
        </footer>
      </div>
    </QueryClientProvider>
  );
}

export default App;

