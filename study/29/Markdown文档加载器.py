#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/27 00:08
#Author  :Emcikem
@File    :Markdown文档加载器.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader

loader = UnstructuredMarkdownLoader("./项目API资料.md")
documents = loader.load()

print(documents)
print(len(documents))
print(documents[0].page_content)