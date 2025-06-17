#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/18 00:04
#Author  :Emcikem
@File    :1.StrOutputParser.py
"""
import dotenv
from click import prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI(model="deepseek-chat")

parser = StrOutputParser()

content = parser.invoke(llm.invoke(prompt.invoke({"query", "你好"})))

print(llm.invoke(prompt.invoke({"query", "你好"})))
print(content)