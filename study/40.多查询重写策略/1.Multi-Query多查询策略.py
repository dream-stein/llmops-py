#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/7 16:37
@Author  : yps302@163.com
@File    : 1.Multi-Query多查询策略.py
"""
import os

import dotenv
import weaviate
from langchain.retrievers import MultiQueryRetriever
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
    auth_credentials=AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
)

embedding = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    # 使用 os.getenv 读取，即使源码要求 SecretStr，这里直接传字符串即可
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL")
)

# 2.创建向量数据库实例
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemoQwen1",
    text_key="text",
    embedding=embedding,
)
retriever = db.as_retriever(search_type="mmr")

# 创建多查询检索器实例
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model="LongCat-Flash-Chat", temperature=0),
    include_original=True,
)

docs = multi_query_retriever.invoke("关于LLMOps应用配置的文档有哪些")
print(docs)
print(len(docs))
