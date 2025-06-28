#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 14:54
#Author  :Emcikem
@File    :Blob解析器.py
"""
from typing import Iterator

from langchain_core.document_loaders.base import BaseBlobParser
from langchain_core.documents import Document
from langchain_core.documents.base import Blob


class CustomParser(BaseBlobParser):
    """自定义解析器，用于将传入的二进制数据的每一行解析成Document组件"""

    def lazy_parse(self, blob: Blob) -> Iterator[Document]:
        line_number = 0
        with blob.as_bytes_io() as f:
            for line in f:
                yield Document(
                    page_content=line,
                    metadata={"score": blob.source, "line_number": line_number},
                )
                line_number += 1

# 1.加载blob数据
blob = Blob.from_path("./喵喵.txt")
parser = CustomParser()

# 2.解析得到文档数据
documents = list(parser.lazy_parse(blob))

# 3.输出
print(documents)
print(len(documents))
print(documents[0].metadata)