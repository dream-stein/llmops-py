#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 21:06
#Author  :Emcikem
@File    :vector_database_service.py
"""
import os
from dataclasses import dataclass
from typing import Any

from injector import inject

# 向量数据库的集合名字
COLLECTION_NAME = "Dataset"

@inject
@dataclass
class VectorDatabaseService:
    """向量数据库服务"""
    client: Any
    vector_store: Any

    def __init__(self):
        """构造函数，完成向量数据库服务的客户端+Langchain向量数据库实例的创建"""
        # 1.按需连接 weaviate 向量数据库，避免启动阶段强依赖 weaviate
        self.client = None
        weaviate_url = os.getenv("WEAVIATE_URL")
        weaviate_api_key = os.getenv("WEAVIATE_API_KEY")
        if weaviate_url and weaviate_api_key:
            try:
                import weaviate
                from weaviate.auth import Auth
                self.client = weaviate.connect_to_weaviate_cloud(
                    cluster_url=weaviate_url,
                    auth_credentials=Auth.api_key(weaviate_api_key),
                )
            except Exception:
                self.client = None


        # 2.延迟创建 LangChain 向量数据库
        self.vector_store = None

    def get_retriever(self):
        """获取检索器"""
        if self.vector_store is None:
            raise RuntimeError("Weaviate 向量数据库未初始化，请配置后重试")
        return self.vector_store.as_retriever()

    @property
    def collection(self):
        if self.client is None:
            raise RuntimeError("Weaviate 客户端未初始化，请配置 WEAVIATE_URL/WEAVIATE_API_KEY")
        return self.client.collections.get(COLLECTION_NAME)