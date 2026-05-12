#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/5 17:02
@Author  : yps302@163.com
@File    : 3.递归JSON分割器.py
"""
import json

import requests
from langchain_text_splitters import RecursiveJsonSplitter

# 1.获取并加载JSON
url="https://api.smith.langchain.com/openapi.json"
json_data=requests.get(url).json()
print(len(json.dumps(json_data)))

# 2.递归JSON分割器
text_splitter=RecursiveJsonSplitter(max_chunk_size=300)

# 3.分割JSON数据
json_chunks=text_splitter.split_json(json_data)
chunks=text_splitter.create_documents(json_chunks)

# 4.输出内容
count=0
for chunk in chunks:
    count+=len(chunk.page_content)

print(count)
