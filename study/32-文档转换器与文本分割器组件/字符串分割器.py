#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 15:31
#Author  :Emcikem
@File    :字符串分割器.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import CharacterTextSplitter

# 1.加载对应的文档
loader = UnstructuredMarkdownLoader("ccc.md")
documents = loader.load()
print(documents)
print(len(documents))
print(len(documents[0].page_content))

# 2.创建文本分割器
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,
    chunk_overlap=50,
)

# 3.分割文本
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    # print(f"快大小:{len(chunk.page_content)},来源:{chunk.metadata}")
    print(chunk)
print(len(chunks))