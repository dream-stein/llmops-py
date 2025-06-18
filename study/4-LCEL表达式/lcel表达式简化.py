#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/18 21:47
#Author  :Emcikem
@File    :lcel表达式简化.py
"""
from typing import Any

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

dotenv.load_dotenv()

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-chat")
parser = StrOutputParser()

chain = prompt | llm | parser

print(chain.invoke({"query": "请讲一个外贸员的冷笑话"}))