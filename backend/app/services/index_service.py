from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from llama_index import ServiceContext, VectorStoreIndex, StorageContext
from llama_index.node_parser import SentenceSplitter
from llama_index.schema import Document as LlamaDocument, NodeWithScore
from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

from app.core.config import settings
from app.models.document import Document


class IndexService:
    def __init__(self, db: Session):
        self.db = db
        self.vector_store = self._create_vector_store()
        self.service_context = self._create_service_context()
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = self._get_or_create_index()

    def _create_vector_store(self) -> PGVectorStore:
        """创建PostgreSQL向量存储"""
        return PGVectorStore.from_params(
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            password=settings.POSTGRES_PASSWORD,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            table_name="document_embeddings",
            embed_dim=1536,  # OpenAI embedding dimension
        )

    def _create_service_context(self) -> ServiceContext:
        """创建LlamaIndex服务上下文"""
        embed_model = OpenAIEmbedding(model=settings.EMBEDDING_MODEL)
        node_parser = SentenceSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        return ServiceContext.from_defaults(
            embed_model=embed_model,
            node_parser=node_parser
        )

    def _get_or_create_index(self) -> VectorStoreIndex:
        """获取或创建向量索引"""
        return VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            service_context=self.service_context
        )

    def add_document(self, document: Document) -> None:
        """将文档添加到索引中"""
        llama_document = LlamaDocument(
            text=document.content,
            metadata={
                "document_id": document.id,
                "filename": document.filename,
                **document._metadata
            }
        )
        self.index.insert(llama_document)

    def delete_document(self, document_id: int) -> None:
        """从索引中删除文档"""
        # 实现从向量存储中删除文档的逻辑
        # 注意：这需要根据PGVectorStore的具体实现来调整
        # 这里是一个简化的示例
        self.vector_store.delete(f"document_id = {document_id}")

    def query(self, query_text: str, top_k: int = 5, rerank: bool = True) -> Dict[str, Any]:
        """执行查询并返回结果"""
        # 创建查询引擎
        query_engine = self.index.as_query_engine(
            similarity_top_k=top_k,
            service_context=self.service_context
        )
        
        # 执行查询
        response = query_engine.query(query_text)
        
        # 如果需要重排序
        if rerank:
            # 这里可以实现自定义的重排序逻辑
            # 例如，基于BM25或其他相关性算法
            pass
        
        # 提取源节点
        source_nodes = []
        if hasattr(response, 'source_nodes'):
            source_nodes = response.source_nodes
        
        # 构建响应
        result = {
            "query": query_text,
            "answer": str(response),
            "sources": [self._format_source_node(node) for node in source_nodes]
        }
        
        return result

    def _format_source_node(self, node: NodeWithScore) -> Dict[str, Any]:
        """格式化源节点"""
        return {
            "text": node.node.text,
            "document_id": node.node.metadata.get("document_id"),
            "score": node.score,
            "metadata": node.node.metadata
        }

