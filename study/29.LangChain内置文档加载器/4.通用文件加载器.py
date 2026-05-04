#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/3 23:00
@Author  : yps302@163.com
@File    : 4.通用文件加载器.py
"""
from langchain_community.document_loaders import UnstructuredFileLoader

loader=UnstructuredFileLoader("./章节介绍.pptx")
documents=loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)
