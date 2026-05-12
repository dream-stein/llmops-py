#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/5 17:19
@Author  : yps302@163.com
@File    : 1.自定义分割器.py
"""
from typing import List

import jieba.analyse
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_text_splitters import TextSplitter


class CustomTextSplitter(TextSplitter):
    """自定义文本分割器"""
    def __init__(self, seperator: str, top_k: int = 10,**kwargs) -> None:
        """构造函数，传递分隔符以及需要提取的关键词数"""
        super().__init__(**kwargs)
        self._seperator = seperator
        self._top_k = top_k

    def split_text(self, text: str) -> List[str]:
        """传递对应的文本执行分割并提取分割数据的关键词，组成文档列表返回"""
        # 1.根据传递的分隔符分割传入的文本
        split_text=text.split(self._seperator)
        # 2.提取分割出来的每一段文本的关键词，数量为top_k个
        text_keywords=[]
        for text in split_text:
            text_keywords.append(jieba.analyse.extract_tags(text, self._top_k))
        # 3.将关键词使用逗号进行拼接组成字符串列表并返回
        return [",".join(keywords) for keywords in text_keywords]




loader=UnstructuredFileLoader("./科幻短篇.txt")
text_splitter=CustomTextSplitter("\n\n",10)

documents=loader.load()
chunks=text_splitter.split_documents(documents)

for chunk in chunks:
    print(chunk.page_content)
