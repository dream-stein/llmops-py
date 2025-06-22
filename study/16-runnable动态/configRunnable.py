#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/22 20:36
#Author  :Emcikem
@File    :configRunnable.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import ConfigurableField

dotenv.load_dotenv()

prompt = PromptTemplate.from_template("请生成一个小于{x}的随机数")

llm = ChatOpenAI(model="deepseek-chat").configurable_fields(
    temperature=ConfigurableField(
        id="llm_temperature",
        name="大语言模型的温度",
        description="温度越低，大语言模型生成内容越确定，温度越高，越随机",
    )
)

chain = prompt | llm | StrOutputParser()

content = chain.invoke({"x": 1000})

print(content)

print("====================")

content = chain.invoke(
    {"x": 1000},
    config={"configurable": {"llm_temperature": 0}},
)

print(content)

content = chain.with_config(configurable={"llm_temperature": 0}).invoke({"x": 1000})
print(content)