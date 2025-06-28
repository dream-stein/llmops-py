#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 12:34
#Author  :Emcikem
@File    :URL网页加载器.py
"""
from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://imooc.com")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)