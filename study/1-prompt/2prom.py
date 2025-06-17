#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/13 00:03
#Author  :Emcikem
@File    :2prom.py
"""
from langchain_core.prompts import PromptTemplate

promt = PromptTemplate.from_template("请讲一个关于{subject}") + "让我开兴下" + "\n{language}语言"

print(promt.invoke({"subject": "程序员", "language": "中文"}).to_string())