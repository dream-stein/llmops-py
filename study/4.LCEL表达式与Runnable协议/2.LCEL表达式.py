#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 11:07
@Author  : yps302@163.com
@File    : 2.LCEL表达式.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="LongCat-Flash-Lite", )
parser = StrOutputParser()

# 2.创建链
chain = prompt | llm | parser

# 3.调用链
print(chain.invoke({"query": "请讲一个程序员的冷笑话"}))
