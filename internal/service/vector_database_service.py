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
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_weaviate import WeaviateVectorStore
from mako.compat import win32
from weaviate import WeaviateClient
from weaviate.auth import Auth
from weaviate.collections import Collection

# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"

@inject
@dataclass
class VectorDatabaseService:
    """向量数据库服务"""
    client: WeaviateClient
    vector_store: WeaviateVectorStore

    def __init__(self):
        """构造函数，完成向量数据库服务的客户端+Langchain向量数据库实例的创建"""
        # 1.创建/连接weaviate向量数据库
        # self.client = weaviate.connect_to_local(
        #     host=os.getenv("WEAVIATE_HOST"),
        #     port=int(os.getenv("WEAVIATE_PORT")),
        # )
        self.client = weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("WEAVIATE_URL"),
            auth_credentials=Auth.api_key(os.getenv("WEAVIATE_API_KEY")),
        )


        # 2.创建Langchain向量数据库
        # self.vector_store = WeaviateVectorStore(
        #     client=self.client,
        #     index_name=COLLECTION_NAME,
        #     text_key="text",
        #     embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        # )
        self.vector_store = None

    def get_retriever(self) -> VectorStoreRetriever:
        """获取检索器"""
        return self.vector_store.as_retriever()

    @classmethod
    def combine_documents(cls, documents: list[Document]) -> str:
        return "\n\n".join([document.page_content for document in documents])

    @property
    def collection(self) -> Collection:
        return self.client.collections.get(COLLECTION_NAME)