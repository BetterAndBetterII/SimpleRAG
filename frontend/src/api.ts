export async function uploadFile(file: File) {
  const form = new FormData();
  form.append('file', file);
  await fetch('http://localhost:8000/upload', { method: 'POST', body: form });
}

export async function query(q: string) {
  const form = new FormData();
  form.append('q', q);
  const res = await fetch('http://localhost:8000/query', {
    method: 'POST',
    body: form,
  });
  return res.json();
}
