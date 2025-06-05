import os
import io
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from markitdown import MarkItDown

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    embedding = Column(Vector(1536))

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use OpenAI embedding if API key is set, otherwise fall back to a mock embedder
if os.getenv("OPENAI_API_KEY"):
    embed_model: BaseEmbedding = OpenAIEmbedding()
else:
    from llama_index.core.embeddings.mock_embed_model import MockEmbedding
    embed_model = MockEmbedding(embed_dim=1536)

md_converter = MarkItDown()

def embed(text: str):
    return embed_model.get_text_embedding(text)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content_bytes = await file.read()
    result = md_converter.convert_stream(io.BytesIO(content_bytes))
    text = result.text_content
    vector = embed(text)
    with SessionLocal() as session:
        doc = Document(content=text, embedding=vector)
        session.add(doc)
        session.commit()
    return {"message": "uploaded"}

@app.post("/query")
async def query(q: str = Form(...)):
    vector = embed(q)
    with SessionLocal() as session:
        docs = session.query(Document).all()
    # compute distances in Python for compatibility with SQLite
    def distance(v1, v2):
        return sum((a - b) ** 2 for a, b in zip(v1, v2))

    docs.sort(key=lambda d: distance(d.embedding, vector))
    top = docs[:5]
    return {"results": [d.content for d in top]}

