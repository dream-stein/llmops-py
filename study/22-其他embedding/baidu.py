#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/24 23:54
#Author  :Emcikem
@File    :baidu.py
"""
import dotenv
from langchain_community.embeddings.baidu_qianfan_endpoint import QianfanEmbeddingsEndpoint

dotenv.load_dotenv()

embeddings = QianfanEmbeddingsEndpoint()

query_vector = embeddings.embed_query("你好啊")
print(query_vector)
print(len(query_vector))