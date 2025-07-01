#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/1 00:22
#Author  :Emcikem
@File    :自定义.py
"""
from typing import List
import jieba.analyse

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import TextSplitter


class CustomTextSplitter(TextSplitter):

    def __init__(self, seperator: str, top_k: int = 10, **kwargs):
        super().__init__(**kwargs)
        self._seperator = seperator
        self._top_k = top_k

    def split_text(self, text: str) -> List[str]:
        split_tests = text.split(self._seperator)

        text_keywords = []
        for split_test in split_tests:
            text_keywords.append(jieba.analyse.extract_tags(split_test, self._top_k))

        return [",".join(keywords) for keywords in text_keywords]

loader = UnstructuredFileLoader("./科幻短篇.txt")
text_splitter = CustomTextSplitter("\n\n", 10)

documents = loader.load()
chunks = text_splitter.split_documents(documents)

for chunk in chunks:
    print(chunk.page_content)