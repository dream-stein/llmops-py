#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/28 15:12
@Author  : yps302@163.com
@File    : 1.bind函数.py
"""

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你正在执行一项测试，请重复用户传递的内容，除了重复其它均不要操作"
    ),
    ("human","{query}")
])

llm=ChatOpenAI(model="LongCat-Flash-Chat")

chain=prompt|llm.bind(max_tokens=10)|StrOutputParser()

content=chain.invoke({"query":"hello world hello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello worldhello world"})

print(content)

