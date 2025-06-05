import { useState } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { Button } from './ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Textarea } from './ui/textarea';
import { queryApi } from '../services/api';
import { QueryResponse } from '../types';

export function QueryChat() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversation, setConversation] = useState<{
    query: string;
    response: QueryResponse;
  }[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) return;
    
    try {
      setIsLoading(true);
      setError(null);
      
      const response = await queryApi.query(query);
      
      setConversation([
        ...conversation,
        { query, response }
      ]);
      
      setQuery('');
    } catch (err) {
      console.error('Query error:', err);
      setError('查询失败，请重试');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>问答交互</CardTitle>
      </CardHeader>
      <CardContent className="p-4">
        <div className="space-y-4 max-h-[500px] overflow-y-auto mb-4">
          {conversation.length === 0 ? (
            <div className="text-center py-8 text-muted-foreground">
              <p>开始提问以获取基于文档的回答</p>
            </div>
          ) : (
            conversation.map((item, index) => (
              <div key={index} className="space-y-4">
                <div className="flex gap-2">
                  <div className="bg-primary text-primary-foreground rounded-full p-2 h-8 w-8 flex items-center justify-center">
                    <span className="text-xs font-bold">我</span>
                  </div>
                  <div className="bg-muted p-3 rounded-lg flex-1">
                    <p>{item.query}</p>
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <div className="bg-secondary text-secondary-foreground rounded-full p-2 h-8 w-8 flex items-center justify-center">
                    <span className="text-xs font-bold">AI</span>
                  </div>
                  <div className="flex-1 space-y-2">
                    <div className="bg-secondary p-3 rounded-lg">
                      <p>{item.response.answer}</p>
                    </div>
                    
                    {item.response.sources.length > 0 && (
                      <div className="text-sm text-muted-foreground">
                        <p className="font-medium mb-1">来源:</p>
                        <div className="space-y-2">
                          {item.response.sources.map((source, idx) => (
                            <div key={idx} className="bg-muted/50 p-2 rounded">
                              <p className="text-xs mb-1">
                                文档 ID: {source.document_id} (相关度: {source.score.toFixed(2)})
                              </p>
                              <p className="text-sm">{source.text}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
        
        {error && (
          <div className="text-destructive text-sm mb-2">{error}</div>
        )}
      </CardContent>
      <CardFooter>
        <form onSubmit={handleSubmit} className="w-full flex gap-2">
          <Textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="输入您的问题..."
            className="flex-1 min-h-[60px] resize-none"
            disabled={isLoading}
          />
          <Button type="submit" disabled={isLoading || !query.trim()}>
            {isLoading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Send className="h-4 w-4" />
            )}
          </Button>
        </form>
      </CardFooter>
    </Card>
  );
}

