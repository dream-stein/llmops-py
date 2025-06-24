#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/24 23:25
#Author  :Emcikem
@File    :HuggingFace.py
"""
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    cache_folder="./embeddings/",
)

query_vector = embeddings.embed("你好，我是木小可，我喜欢打篮球游泳")

print(query_vector)
print(len(query_vector))