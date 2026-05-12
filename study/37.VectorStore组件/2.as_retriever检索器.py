#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/6 16:42
@Author  : yps302@163.com
@File    : 2.as_retriever检索器.py
"""
import os

import dotenv
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

loader=UnstructuredMarkdownLoader("./项目API文档.md")
text_splitter=RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。|！|？", r"\.\s|\!\s|\?\s", r"；|;\s", r"，|,\s", " ", "", ],
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

documents=loader.load()
chunks=text_splitter.split_documents(documents)

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

db.add_documents(chunks)

# 4.转换检索器 十条数据 阈值0.5
retriever=db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k":10,"score_threshold":0.5},
)

documents=retriever.invoke("关于配置接口的信息有哪些")

print(list(document.page_content[:50]for document in documents))
print(len(documents))