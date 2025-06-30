#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/29 23:03
#Author  :Emcikem
@File    :程序代码递归分割.py
"""
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

loader = UnstructuredFileLoader("./项目API资料.md")
separators = [
    "\n\n",
    "\n",
    "。|！|？",
    "",
    "\.\s|\!\s|\?\s",
    "；|;\s",
    "，|,\s"
    " ",
    ""
]

documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    separators=separators,
    is_separator_regex=True,
    chunk_size=500,
    chunk_overlap=50,
    add_start_index=True,
)

chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(f"大小:{len(chunk.page_content)}，元数据{chunk.metadata}")

print(chunks[2].page_content)