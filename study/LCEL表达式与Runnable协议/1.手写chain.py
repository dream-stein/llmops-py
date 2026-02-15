#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/15 10:28
@Author  : yps302@163.com
@File    : 1.手写chain.py
"""
from typing import Any

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="LongCat-Flash-Lite", )
parser = StrOutputParser()


# 2.定义一个链
class Chain:
    steps: list = []

    def __init__(self, steps: list):
        self.steps = steps

    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print("步骤：", step)
            print("输出：", input)
            print("===========")
        return input


# 3.编排链
chain = Chain(steps=[prompt, llm, parser])

# 4.执行链
print(chain.invoke({"query": "你好，你是？"}))
