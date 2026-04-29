#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/29 15:09
@Author  : yps302@163.com
@File    : 1.多LLM链选择.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI
from openai.resources.containers.files import content

dotenv.load_dotenv()

prompt=ChatPromptTemplate.from_template("{query}")
llm=ChatOpenAI(model="LongCat-Flash-Chat").configurable_alternatives(
    ConfigurableField(id="llm",name="",description="",),
    default_key="chat", #默认键值 对应上面本身声明的值
    lite=ChatOpenAI(model="LongCat-Flash-Chat-Lite"), #可选值
    think=ChatOpenAI(model="LongCat-Flash-Thinking"),
)

chain=prompt|llm|StrOutputParser()

content =chain.invoke(
    {"query":"你好，你是什么模型"},
    config={"configurable":{"llm":"think"}}
)

print(content)