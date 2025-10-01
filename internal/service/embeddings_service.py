#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 22:12
#Author  :Emcikem
@File    :embeddings_service.py
"""
import os
from dataclasses import dataclass

import tiktoken
from injector import inject
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.storage import RedisStore
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from redis import Redis

@inject
@dataclass
class EmbeddingsService:
    """文本嵌入模型服务"""
    _store: RedisStore
    _embeddings: Embeddings
    _cache_backed_embeddings: CacheBackedEmbeddings

    def __init__(self, redis: Redis):
        """构造函数，初始化文本嵌入模型客户端、存储器、缓存客户端"""
        self._store = RedisStore(client=redis)
        # self._embeddings = HuggingFaceEmbeddings(
        #     model_name="Alibaba-NLP/gte-multilingual-base",
        #     cache_folder=os.path.join(os.getcwd(), "internal", "core", "embeddings"),
        #     model_kwargs={
        #         "trust_remote_code": True,
        #     }
        # )
        # todo:改成远程模型
        local_model_path = os.path.join(
            os.getcwd(),
            "internal",
            "core",
            "embeddings",
            "models--Alibaba-NLP--gte-multilingual-base",
            "snapshots",
            "7fc06782350c1a83f88b15dd4b38ef853d3b8503"
        )
        self._embeddings = HuggingFaceEmbeddings(
            model_name=local_model_path,  # 指向最终的哈希文件夹
            model_kwargs={
                "trust_remote_code": True,  # 必须：gte模型需要加载自定义modeling.py
                "device": "cpu"  # 可选：指定设备（cpu/gpu），避免自动检测时的额外请求
            },
            cache_folder=None  # 禁用缓存（已用本地路径，无需再缓存）
        )
        # self._embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # self._cache_backed_embeddings = CacheBackedEmbeddings.from_bytes_store(
        #     self._embeddings,
        #     self._store,
        #     namespace="embeddings",
        # )


    @classmethod
    def calculate_token_count(cls, query: str) -> int:
        """计算传入文本的token数"""
        encoding = tiktoken.encoding_for_model("gpt-3.5")
        return len(encoding.encode(query))

    @property
    def store(self) -> RedisStore:
        return self._store

    @property
    def embeddings(self) -> Embeddings:
        return self._embeddings

    @property
    def cache_backed_embeddings(self) -> CacheBackedEmbeddings:
        return self._cache_backed_embeddings

