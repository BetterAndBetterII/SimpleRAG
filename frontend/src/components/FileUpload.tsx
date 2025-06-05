import { useState } from 'react';
import { Upload, FileText, Check, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { documentsApi } from '../services/api';
import { Document } from '../types';

interface FileUploadProps {
  onUploadSuccess: (document: Document) => void;
}

export function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('请选择文件');
      return;
    }

    try {
      setIsUploading(true);
      setError(null);
      
      const uploadedDocument = await documentsApi.uploadDocument(file);
      onUploadSuccess(uploadedDocument);
      
      // 重置状态
      setFile(null);
      setIsUploading(false);
    } catch (err) {
      setError('上传失败，请重试');
      setIsUploading(false);
      console.error('Upload error:', err);
    }
  };

  return (
    <Card className="w-full">
      <CardContent className="p-6">
        <div
          className={`border-2 border-dashed rounded-lg p-6 text-center ${
            isDragOver ? 'border-primary bg-primary/5' : 'border-muted'
          }`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="rounded-full bg-primary/10 p-3">
              {file ? <FileText className="h-8 w-8 text-primary" /> : <Upload className="h-8 w-8 text-primary" />}
            </div>
            
            <div className="space-y-1">
              <h3 className="text-lg font-medium">
                {file ? '文件已选择' : '上传文件'}
              </h3>
              <p className="text-sm text-muted-foreground">
                {file 
                  ? file.name 
                  : '拖放文件到此处或点击选择文件'
                }
              </p>
            </div>

            <div className="flex gap-2">
              <label htmlFor="file-upload">
                <Button
                  variant="outline"
                  onClick={() => document.getElementById('file-upload')?.click()}
                  disabled={isUploading}
                >
                  选择文件
                </Button>
                <input
                  id="file-upload"
                  type="file"
                  className="hidden"
                  onChange={handleFileChange}
                  accept=".md,.txt"
                />
              </label>
              
              {file && (
                <Button 
                  onClick={handleUpload} 
                  disabled={isUploading}
                >
                  {isUploading ? '上传中...' : '上传文件'}
                  {!isUploading && <Check className="ml-2 h-4 w-4" />}
                </Button>
              )}
            </div>

            {error && (
              <div className="flex items-center text-destructive text-sm">
                <AlertCircle className="h-4 w-4 mr-1" />
                {error}
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

