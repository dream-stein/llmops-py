#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/22 18:39
#Author  :Emcikem
@File    :1.bind.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "你正在执行一项测试，请重复用户传递的内容，除了重复其他均不要操作"
    ),
    ("human", "{query}")
])
llm = ChatOpenAI(model="deepseek-chat")

chain = prompt | llm.bind(stop="World") | StrOutputParser()

content = chain.invoke({"query": "Hello World"})

print(content)