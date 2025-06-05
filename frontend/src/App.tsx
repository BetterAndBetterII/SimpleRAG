import React, { useState } from 'react';
import { Upload } from 'lucide-react';
import { uploadFile, query } from './api';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState<string[]>([]);

  const handleUpload = async () => {
    if (!file) return;
    await uploadFile(file);
    setFile(null);
  };

  const handleAsk = async () => {
    const res = await query(question);
    setAnswer(res.results);
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center space-x-2">
        <input type="file" onChange={e => setFile(e.target.files?.[0] || null)} />
        <button className="px-2 py-1 bg-blue-500 text-white" onClick={handleUpload}>
          <Upload className="inline mr-1" size={16} /> Upload
        </button>
      </div>
      <div>
        <input
          className="border p-1 mr-2"
          value={question}
          onChange={e => setQuestion(e.target.value)}
        />
        <button className="px-2 py-1 bg-green-500 text-white" onClick={handleAsk}>
          Ask
        </button>
      </div>
      <ul className="list-disc pl-5">
        {answer.map((a, i) => (
          <li key={i}>{a}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
