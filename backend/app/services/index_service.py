import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from llama_index.core import Document as LlamaDocument, Settings, VectorStoreIndex, StorageContext
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import QueryBundle
from llama_index.core.indices.vector_store import VectorIndexRetriever
from llama_index.core.postprocessor import SimilarityPostprocessor
from llama_index.core.vector_stores.types import VectorStoreQueryMode
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.postprocessor.jinaai_rerank import JinaRerank

from app.core.config import settings
from app.models.document import Document


class IndexService:
    """文档索引服务，使用Redis作为文档存储，Milvus作为向量存储"""
    
    def __init__(self, db: Session, site_id: str = "default"):
        self.db = db
        self.site_id = self._sanitize_site_id(site_id)
        
        # 设置命名空间
        self.redis_namespace = f"simplerag:{self.site_id}:docs"
        self.milvus_collection = f"simplerag_{self.site_id}_vectors"
        
        # 初始化存储组件
        self.doc_store = self._create_doc_store()
        self.vector_store = self._create_vector_store()
        self.storage_context = StorageContext.from_defaults(
            docstore=self.doc_store,
            vector_store=self.vector_store,
        )
        
        # 初始化索引
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store,
            storage_context=self.storage_context,
        )
        
        # 初始化摄入管道
        self.pipeline = self._create_ingestion_pipeline()

    def _sanitize_site_id(self, site_id: str) -> str:
        """清理站点ID，确保符合命名规范"""
        if not re.match(r'^[a-zA-Z0-9_]+$', site_id):
            site_id = re.sub(r'[^a-zA-Z0-9_]', '_', site_id)
        return site_id

    def _create_doc_store(self) -> RedisDocumentStore:
        """创建Redis文档存储"""
        return RedisDocumentStore.from_host_and_port(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            namespace=self.redis_namespace,
        )

    def _create_vector_store(self) -> MilvusVectorStore:
        """创建Milvus向量存储"""
        return MilvusVectorStore(
            uri="",  # 设置为空字符串避免使用本地文件
            host=settings.MILVUS_HOST,
            port=settings.MILVUS_PORT,
            db_name=getattr(settings, 'MILVUS_DB', 'default'),
            collection_name=self.milvus_collection,
            dim=settings.EMBEDDING_DIM,
            similarity_metric="cosine",
            enable_sparse=getattr(settings, 'ENABLE_SPARSE_EMBEDDING', False),
            index_config={
                "metric_type": "COSINE",
                "index_type": "HNSW",
                "params": {"M": 32, "efConstruction": 200}
            },
            search_config={"ef": 512}
        )

    def _create_ingestion_pipeline(self) -> IngestionPipeline:
        """创建文档摄入管道"""
        embed_model = OpenAIEmbedding(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.EMBEDDING_API_KEY,
            api_base=settings.EMBEDDING_BASE_URL
        )
        
        return IngestionPipeline(
            transformations=[
                SentenceSplitter(
                    chunk_size=settings.CHUNK_SIZE,
                    chunk_overlap=settings.CHUNK_OVERLAP,
                ),
                embed_model,
            ],
            vector_store=self.vector_store,
            docstore=self.doc_store,
            disable_cache=True,
        )

    async def add_document(self, document: Document) -> str:
        """
        将文档添加到索引中
        
        Args:
            document: 数据库中的文档对象
            
        Returns:
            str: 文档ID
        """
        # 生成文档ID
        doc_id = f"{self.site_id}:{document.id}"
        
        # 创建LlamaIndex文档对象
        llama_document = LlamaDocument(
            text=document.content,
            id_=doc_id,
            metadata={
                "document_id": document.id,
                "filename": document.filename,
                "site_id": self.site_id,
                "created_at": document.created_at.isoformat() if document.created_at else None,
                **document._metadata
            }
        )
        
        # 执行文档摄入
        await self.pipeline.arun(documents=[llama_document])
        return doc_id

    async def add_documents(self, documents: List[Document]) -> List[str]:
        """
        批量添加文档到索引中
        
        Args:
            documents: 文档列表
            
        Returns:
            List[str]: 文档ID列表
        """
        docs = []
        doc_ids = []
        
        for document in documents:
            # 生成文档ID
            doc_id = f"{self.site_id}:{document.id}"
            doc_ids.append(doc_id)
            
            # 创建LlamaIndex文档对象
            llama_document = LlamaDocument(
                text=document.content,
                id_=doc_id,
                metadata={
                    "document_id": document.id,
                    "filename": document.filename,
                    "site_id": self.site_id,
                    "created_at": document.created_at.isoformat() if document.created_at else None,
                    **document._metadata
                }
            )
            docs.append(llama_document)
        
        # 执行批量文档摄入
        await self.pipeline.arun(documents=docs)
        return doc_ids

    async def delete_document(self, document_id: int) -> bool:
        """
        从索引中删除文档
        
        Args:
            document_id: 数据库中的文档ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            doc_id = f"{self.site_id}:{document_id}"
            await self.index.adelete_ref_doc(
                ref_doc_id=doc_id,
                delete_from_docstore=True
            )
            return True
        except Exception as e:
            print(f"删除文档失败: {e}")
            return False

    async def delete_documents(self, document_ids: List[int]) -> bool:
        """
        批量删除文档
        
        Args:
            document_ids: 数据库中的文档ID列表
            
        Returns:
            bool: 删除是否成功
        """
        try:
            for document_id in document_ids:
                doc_id = f"{self.site_id}:{document_id}"
                await self.index.adelete_ref_doc(
                    ref_doc_id=doc_id,
                    delete_from_docstore=True
                )
            return True
        except Exception as e:
            print(f"批量删除文档失败: {e}")
            return False

    async def update_document(self, document: Document) -> bool:
        """
        更新文档内容
        
        Args:
            document: 更新后的文档对象
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 先删除旧文档
            await self.delete_document(document.id)
            
            # 添加新文档
            await self.add_document(document)
            return True
        except Exception as e:
            print(f"更新文档失败: {e}")
            return False

    async def query(
        self, 
        query_text: str, 
        top_k: int = 5, 
        rerank: bool = True,
        rerank_top_k: int = 10,
        similarity_cutoff: float = 0.6,
        search_kwargs: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        执行查询并返回结果
        
        Args:
            query_text: 查询文本
            top_k: 返回的最大文档数量
            rerank: 是否进行重排序
            rerank_top_k: 重排序返回的最大文档数量
            similarity_cutoff: 相似度阈值
            search_kwargs: 搜索的额外参数
            
        Returns:
            Dict[str, Any]: 查询结果
        """
        # 合并默认参数和传入的搜索参数
        search_params = {}
        if search_kwargs:
            search_params.update(search_kwargs)
        
        # 创建检索器
        vector_retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=top_k,
            vector_store_query_mode=VectorStoreQueryMode.HYBRID,
            **search_params
        )
        
        # 执行检索
        qb = QueryBundle(query_text)
        nodes = await vector_retriever.aretrieve(qb)
        
        # 重排序处理
        if rerank and hasattr(settings, 'RERANKER_API_KEY'):
            try:
                reranker = JinaRerank(
                    base_url=getattr(settings, 'RERANKER_BASE_URL', None),
                    model=getattr(settings, 'RERANKER_MODEL', 'bge-reranker-v2-m3'),
                    api_key=settings.RERANKER_API_KEY,
                    top_n=rerank_top_k,
                )
                nodes = reranker.postprocess_nodes(nodes, qb)
            except Exception as e:
                print(f"重排序失败，使用原始结果: {e}")
        
        # 应用相似度阈值
        similarity_processor = SimilarityPostprocessor(
            similarity_cutoff=similarity_cutoff
        )
        nodes = similarity_processor.postprocess_nodes(nodes)
        
        # 格式化结果
        sources = []
        for node in nodes:
            sources.append({
                "text": node.node.text,
                "document_id": node.node.metadata.get("document_id"),
                "filename": node.node.metadata.get("filename"),
                "score": node.score if hasattr(node, 'score') else None,
                "metadata": node.node.metadata
            })
        
        # 构建响应
        result = {
            "query": query_text,
            "sources": sources,
            "total_results": len(sources)
        }
        
        return result

    async def get_document_by_id(self, document_id: int) -> Optional[LlamaDocument]:
        """
        获取指定文档
        
        Args:
            document_id: 数据库中的文档ID
            
        Returns:
            Optional[LlamaDocument]: 文档对象，如果不存在则返回None
        """
        try:
            doc_id = f"{self.site_id}:{document_id}"
            return await self.doc_store.aget_document(doc_id)
        except (KeyError, ValueError):
            return None

    async def list_documents(self) -> List[Dict[str, Any]]:
        """
        列出该站点的所有文档
        
        Returns:
            List[Dict[str, Any]]: 文档列表
        """
        all_docs = self.doc_store.docs
        site_docs = []
        
        for doc_id, doc in all_docs.items():
            if doc_id.startswith(f"{self.site_id}:"):
                site_docs.append({
                    "id": doc_id,
                    "document_id": doc.metadata.get("document_id"),
                    "filename": doc.metadata.get("filename"),
                    "metadata": doc.metadata,
                    "text_preview": doc.text[:200] + "..." if len(doc.text) > 200 else doc.text,
                })
        
        return site_docs

    async def get_stats(self) -> Dict[str, Any]:
        """
        获取索引统计信息
        
        Returns:
            Dict[str, Any]: 统计信息
        """
        all_docs = self.doc_store.docs
        site_docs = [
            doc for doc_id, doc in all_docs.items()
            if doc_id.startswith(f"{self.site_id}:")
        ]
        
        total_tokens = sum(len(doc.text.split()) for doc in site_docs)
        
        return {
            "site_id": self.site_id,
            "total_documents": len(site_docs),
            "total_tokens": total_tokens,
            "average_document_length": total_tokens / len(site_docs) if site_docs else 0,
            "redis_namespace": self.redis_namespace,
            "milvus_collection": self.milvus_collection,
        }

    async def clear_all_documents(self) -> bool:
        """
        清除该站点的所有文档
        
        Returns:
            bool: 清除是否成功
        """
        try:
            all_docs = self.doc_store.docs
            doc_ids_to_delete = [
                doc_id for doc_id in all_docs.keys()
                if doc_id.startswith(f"{self.site_id}:")
            ]
            
            for doc_id in doc_ids_to_delete:
                await self.index.adelete_ref_doc(
                    ref_doc_id=doc_id,
                    delete_from_docstore=True
                )
            
            return True
        except Exception as e:
            print(f"清除所有文档失败: {e}")
            return False


class IndexServiceFactory:
    """索引服务工厂，用于创建和管理站点索引实例"""
    
    _instances: Dict[str, IndexService] = {}
    
    @classmethod
    def get_instance(
        cls,
        db: Session,
        site_id: str = "default",
        use_cache: bool = True
    ) -> IndexService:
        """
        获取索引服务实例，如果不存在则创建新实例
        
        Args:
            db: 数据库会话
            site_id: 站点ID
            use_cache: 是否使用缓存的实例
            
        Returns:
            IndexService: 索引服务实例
        """
        # 如果使用缓存且实例已存在，则返回缓存的实例
        if use_cache and site_id in cls._instances:
            return cls._instances[site_id]
            
        # 创建新实例
        service = IndexService(db=db, site_id=site_id)
        
        # 如果使用缓存，则保存实例
        if use_cache:
            cls._instances[site_id] = service
            
        return service
        
    @classmethod
    def clear_cache(cls):
        """清除缓存的实例"""
        cls._instances.clear()

