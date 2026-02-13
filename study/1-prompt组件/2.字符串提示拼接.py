#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/8 16:41
@Author  : yps302@163.com
@File    : 2.字符串提示拼接.py
"""
from langchain_core.prompts import PromptTemplate

prompt = (
        PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
        + "，让我开心下"
        + "\n使用{language}语言"
)
print(prompt.invoke({"subject": "程序员", "language": "中文"}).to_string())
