import { useState } from 'react';
import { Trash2, FileText, ChevronDown, ChevronUp } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Document } from '../types';
import { documentsApi } from '../services/api';

interface DocumentListProps {
  documents: Document[];
  onDocumentDelete: (id: number) => void;
}

export function DocumentList({ documents, onDocumentDelete }: DocumentListProps) {
  const [expandedDocId, setExpandedDocId] = useState<number | null>(null);

  const handleDelete = async (id: number) => {
    try {
      await documentsApi.deleteDocument(id);
      onDocumentDelete(id);
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  const toggleExpand = (id: number) => {
    setExpandedDocId(expandedDocId === id ? null : id);
  };

  if (documents.length === 0) {
    return (
      <Card className="w-full">
        <CardContent className="p-6 text-center">
          <p className="text-muted-foreground">暂无文档，请上传文件</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>文档列表</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y">
          {documents.map((doc) => (
            <div key={doc.id} className="p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <h4 className="font-medium">{doc.filename}</h4>
                    <p className="text-sm text-muted-foreground">
                      上传于 {new Date(doc.created_at).toLocaleString()}
                    </p>
                  </div>
                </div>
                <div className="flex space-x-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => toggleExpand(doc.id)}
                  >
                    {expandedDocId === doc.id ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(doc.id)}
                  >
                    <Trash2 className="h-4 w-4 text-destructive" />
                  </Button>
                </div>
              </div>
              
              {expandedDocId === doc.id && (
                <div className="mt-4 p-3 bg-muted/50 rounded-md">
                  <pre className="text-sm whitespace-pre-wrap overflow-auto max-h-60">
                    {doc.content}
                  </pre>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

