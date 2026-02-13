#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/13 16:58
@Author  : yps302@163.com
@File    : 1.StrOutputParser.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.编排提示模板
prompt = ChatPromptTemplate.from_template("{query}")

# 2.构建大语言模型
llm = ChatOpenAI(model="LongCat-Flash-Lite", )

# 3.创建字符串解析器
parser = StrOutputParser()

# 4.调用llm生成结果和解析
content = parser.invoke(llm.invoke(prompt.invoke({"query": "你好，你是谁？"})))
print(content)
