#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 16:09
#Author  :Emcikem
@File    :递归字符文本分割器.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = UnstructuredMarkdownLoader("./项目API资料.md")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

chunks = text_splitter.split_documents(documents)
for chunk in chunks:
    print(f"大小:{len(chunk.page_content)}，元数据{chunk.metadata}")