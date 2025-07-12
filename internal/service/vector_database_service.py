#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 21:06
#Author  :Emcikem
@File    :vector_database_service.py
"""
import os
from dataclasses import dataclass

from injector import inject
import weaviate
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from weaviate import WeaviateClient



@inject
@dataclass
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """构造函数，完成向量数据库服务的客户端+Langchain向量数据库实例的创建"""
        # 1.创建/连接weaviate向量数据库
        self.client = weaviate.connect_to_local(
            host=os.getenv("WEAVIATE_HOST"),
            port=int(os.getenv("WEAVIATE_PORT")),
        )

        # 2.创建Langchain向量数据库
        self.vector_store = WeaviateVectorStore(
            client=self.client,
            index_name="Dataset",
            text_key="text",
            embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        )

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()