#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/30 15:21
@Author  : yps302@163.com
@File    : 1.OpenAI嵌入模型.py
"""
import os

import dotenv
import numpy as np
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

def cosine_similarity(vec1:list,vec2:list)->float:
    """计算传入两个向量的余弦相似度"""
    # 1.计算两个向量的点积
    dot_product = np.dot(vec1,vec2)

    # 2.计算向量的长度
    vec1_norm = np.linalg.norm(vec1)
    vec2_norm = np.linalg.norm(vec2)

    # 3.计算余弦相似度
    return dot_product / (vec1_norm * vec2_norm)

# 1.创建文本嵌入模型
embeddings = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    # 使用 os.getenv 读取，即使源码要求 SecretStr，这里直接传字符串即可
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL")
)

# 2.嵌入文本
query_vector=embeddings.embed_query("我叫小明 我喜欢打篮球")

print(query_vector)
print(len(query_vector))

# 3.嵌入文档列表/字符串列表

document_vector = embeddings.embed_documents([
    "我叫野兽先辈，我喜欢健身",
    "这个喜欢健身的人叫野兽先辈",
    "求知若渴，虚心若愚"
])

print(len(document_vector))

# 4.计算余弦相似度
print("向量1和2的相似度：",cosine_similarity(document_vector[0],document_vector[1]))
print("向量1和3的相似度：",cosine_similarity(document_vector[0],document_vector[2]))