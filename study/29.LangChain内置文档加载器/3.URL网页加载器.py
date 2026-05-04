#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/3 22:53
@Author  : yps302@163.com
@File    : 3.URL网页加载器.py
"""
from langchain_community.document_loaders import WebBaseLoader

loader=WebBaseLoader("https://www.cnblogs.com",)
documents=loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)