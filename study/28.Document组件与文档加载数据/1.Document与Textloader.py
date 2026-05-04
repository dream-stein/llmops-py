#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/3 16:53
@Author  : yps302@163.com
@File    : 1.Document与Textloader.py
"""
from langchain_community.document_loaders import TextLoader

# 1.构建加载器
loader = TextLoader("./电商数据.txt",encoding="utf-8")

# 2.加载数据
documents= loader.load()
print(documents)
print(len(documents))
print(documents[0].metadata)

