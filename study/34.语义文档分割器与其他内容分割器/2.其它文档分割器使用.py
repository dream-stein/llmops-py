#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/5 15:30
@Author  : yps302@163.com
@File    : 2.其它文档分割器使用.py
"""
from langchain_text_splitters import TextSplitter, HTMLHeaderTextSplitter

html_string = """
<!DOCTYPE html>
<html>
<body>
    <div>
        <h1>标题1</h1>
        <p>关于标题1的一些介绍文本。</p>
        <div>
            <h2>子标题1</h2>
            <p>关于子标题1的一些介绍文本。</p>
            <h3>子子标题1</h3>
            <p>关于子子标题1的一些文本。</p>
            <h3>子子标题2</h3>
            <p>关于子子标题2的一些文本。</p>
        </div>
        <div>
            <h3>子标题2</h2>
            <p>关于子标题2的一些文本。</p>
        </div>
        <br>
        <p>关于标题1的一些结束文本。</p>
    </div>
</body>
</html>
"""
headers_to_split_on = [
    ("h1", "一级标题"),
    ("h2", "二级标题"),
    ("h3", "三级标题"),
]


text_splitter = HTMLHeaderTextSplitter(headers_to_split_on)
chunks=text_splitter.split_text(html_string)

for chunk in chunks:
    print(chunk)


