#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/3 22:25
@Author  : yps302@163.com
@File    : 1.markdown文档加载器.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./项目API资料.md")
documents=loader.load()

print(documents)
print(len(documents))
print(documents[0].metadata)