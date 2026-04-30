#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/30 16:25
@Author  : yps302@163.com
@File    : 1.Hugging Face本地嵌入模型.py
"""
from langchain_huggingface import HuggingFaceEmbeddings

embeddings=HuggingFaceEmbeddings()

query_vector=embeddings.query_vector("你好我是野兽先辈我喜欢打篮球")

print(query_vector)
print(len(query_vector))