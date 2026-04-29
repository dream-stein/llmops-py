#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/28 16:27
@Author  : yps302@163.com
@File    : 1.configurable_fields使用技巧.py
"""
import dotenv
from langchain.schema.runnable import configurable
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("请生成一个小于{x}的随机整数")

llm=ChatOpenAI(model="LongCat-Flash-Chat").configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="大语言模型的温度",
        description="温度越低生成内容越确定 反则反之"
    )
)

chain=prompt|llm|StrOutputParser()

content=chain.invoke({"x":1000})

print(content)

print("=================")

# 将temperature修改为0调用
# with_config返回一个新的链 方便新建
with_config_chain=chain.with_config(configurable={"llm_temperature":0})
content=with_config_chain.invoke({"x":1000})
# content=chain.invoke(
#     {"x":1000},
#     config={"configurable":{"llm_temperature":0}}
# )
print(content)