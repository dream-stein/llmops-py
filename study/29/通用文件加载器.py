#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 12:41
#Author  :Emcikem
@File    :通用文件加载器.py
"""
from langchain_community.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader("./项目API资料.md")

documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
