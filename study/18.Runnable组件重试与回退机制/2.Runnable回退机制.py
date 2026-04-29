#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/29 16:17
@Author  : yps302@163.com
@File    : 2.Runnable回退机制.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt=ChatPromptTemplate.from_template("{query}")
llm=ChatOpenAI(model="LongCat-Flash-Chat1").with_fallbacks(
    [ChatOpenAI(model="LongCat-Flash-Chat")]
)

chain=prompt|llm|StrOutputParser()

content =chain.invoke(
    {"query":"你好，你是什么模型"},
)

print(content)