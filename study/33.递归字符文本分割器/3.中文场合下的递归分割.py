#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/5 11:42
@Author  : yps302@163.com
@File    : 3.中文场合下的递归分割.py
"""
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader=UnstructuredMarkdownLoader("./项目API文档.md")
separators = [
    "\n\n",
    "\n",
    "。|！|？",
    r"\.\s|\!\s|\?\s",  # 英文标点符号后面通常需要加空格
    r"；|;\s",
    r"，|,\s",
    " ",
    ""
]
text_splitter=RecursiveCharacterTextSplitter(
    separators=separators,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)


documents=loader.load()

chunks=text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"块大小：{len(chunk.page_content)},元数据：{chunk.metadata}")

print(chunks[2].page_content)
