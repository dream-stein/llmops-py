#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/26 23:14
#Author  :Emcikem
@File    :DOcumentTextLoader.py
"""
from langchain_community.document_loaders import TextLoader

# 1.构建加载器
loader = TextLoader("./电商产品数据.txt", encoding="utf-8", autodetect_encoding=True)

# 2.记载数据
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
