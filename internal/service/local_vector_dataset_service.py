#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/30 20:30
#Author  :Emcikem
@File    :local_vector_dataset_service.py
"""
import uuid
from typing import Iterable, Any, List, Optional

from injector import inject
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from internal.service import EmbeddingsService


@inject
class LocalVectorDatabaseService:
    """基于内存+欧几里得距离的向量数据库"""
    store: dict = {} # 存储向量的临时变量
    _embedding: Embeddings

    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_services: EmbeddingsService):
        """构造函数，完成向量数据库服务的客户端+LangChain向量数据库实例的创建"""
        self.embeddings_service = embeddings_services
        self._embedding = embeddings_services.embeddings

    def add_texts(self, texts: Iterable[str], metadatas: Optional[List[dict]] = None, **kwargs: Any) -> List[str]:
        """将数据添加到向量数据库中"""
        # 1.检测metadata的数据格式
        if metadatas is not None and len(metadatas) != len(texts):
            raise ValueError("metadatas格式错误")

        # 2.将数据转换成文本嵌入/向量和ids
        embeddings = self._embedding.embed_documents(texts)
        ids = [str(uuid.uuid4()) for _ in texts]

        # 3.通过for循环组装数据记录
        for idx, text in enumerate(texts):
            self.store[ids[idx]] = {
                "id": ids[idx],
                "text": text,
                "vector": embeddings[idx],
                "metadata": metadatas[idx] if metadatas is not None else {},
            }

        return ids

    def add_documents(self, lcDocuments: list[Document], ids: list[uuid.UUID]) -> None:
        """将数据添加到向量数据库中"""
        # 1.将数据转换成文本嵌入/向量
        texts = [document.page_content for document in lcDocuments]
        embeddings = self._embedding.embed_documents(texts)

        for idx, document in enumerate(lcDocuments):
            self.store[ids[idx]] = {
                "id": ids[idx],
                "text": document.page_content,
                "vector": embeddings[idx],
                "metadata": document.metadata,
            }

    def similarity_search(self, query: str, k: int = 4, **kwargs: Any) -> List[Document]:
        """传入对应的query执行相似性搜索"""
        # 1.将query转换成向量
        embedding = self._embedding.embed_query(query)

        # 2.循环和store中的每一个向量进行比较，计算欧几里得距离
        result = []
        for key, record in self.store.items():
            distance = self._euclidean_distance(embedding, record["vector"])
            result.append({"distance": distance, **record})

        # 3.排序，欧几里得距离越小越靠前
        sorted_result = sorted(result, key=lambda x: x["distance"])

        # 4.取数据，取k条数据
        result_k = sorted_result[:k]

        return [
            Document(page_content=item["text"], metadata={**item["metadata"], "score": item["distance"]})
            for item in result_k
        ]
