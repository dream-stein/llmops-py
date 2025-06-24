#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/24 21:58
#Author  :Emcikem
@File    :Ppenai.py
"""
import dotenv
import numpy as np
from numpy.linalg import norm
from langchain_openai import OpenAIEmbeddings
from fastembed import TextEmbedding

dotenv.load_dotenv()

def cosine_similarity(vec1: list, vec2: list) -> float:
    """计算传入两个向量的余弦相似度"""
    # 1.计算两个向量的点积
    dot_product = np.dot(vec1, vec2)

    # 2.计算向量的长度
    vec1_norm = norm(vec1)
    vec2_norm = norm(vec2)

    # 3.计算余弦相似度
    return dot_product / (vec1_norm * vec2_norm)

# 1.创建文本嵌入模型
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

# 2.嵌入文本
query_vector = list(model.embed("我叫慕小课，我喜欢打篮球"))

print(query_vector)
print(len(query_vector))

# 3.嵌入文档列表/字符串列表
documents_vector = list(model.embed([
    "我叫木小可",
    "我喜欢打篮球"
]))

print(len(documents_vector))

# print("相似度:", cosine_similarity(documents_vector[0], documents_vector[1]))