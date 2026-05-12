#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/5 12:03
@Author  : yps302@163.com
@File    : 1.语义文本分割器使用.py
"""
import os

import dotenv
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

loader=UnstructuredFileLoader("./科幻短篇.txt")
text_splitter=SemanticChunker(
    embeddings=OpenAIEmbeddings(
        model="Qwen/Qwen3-Embedding-8B",
        # 使用 os.getenv 读取，即使源码要求 SecretStr，这里直接传字符串即可
        api_key=os.getenv("SILICONFLOW_API_KEY"),
        base_url=os.getenv("SILICONFLOW_BASE_URL")
        ),
    number_of_chunks=10,
    sentence_split_regex=r"(?<=[。？！.?!])",
    add_start_index=True,
)

documents=loader.load()
chunks=text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小：{len(chunk.page_content)},元数据：{chunk.metadata}")

print(chunks[2].page_content)

