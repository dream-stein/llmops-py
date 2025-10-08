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
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

@inject
@dataclass
class EmbeddingsService:
    """文本嵌入模型服务"""
    _embeddings: Embeddings
    _cache_backed_embeddings: CacheBackedEmbeddings

    def __init__(self):
        """构造函数，初始化文本嵌入模型客户端、存储器、缓存客户端"""
        self._embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-zh-v1.5",
            cache_folder=os.path.join(os.getcwd(), "internal", "core", "embeddings"),
            model_kwargs={
                "trust_remote_code": True,
            }
        )
        # todo:改成远程模型

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
    def embeddings(self) -> Embeddings:
        return self._embeddings

    @property
    def cache_backed_embeddings(self) -> CacheBackedEmbeddings:
        return self._cache_backed_embeddings

