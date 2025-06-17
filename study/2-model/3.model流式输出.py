#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/17 23:34
#Author  :Emcikem
@File    :3.model流式输出.py
"""

from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是ai，现在时间{now}"),
    ("human", "{query}")
]).partial(now=datetime.now())

llm = ChatOpenAI(model="deepseek-chat")

response = llm.stream(
    prompt.invoke({"query", "你能简单介绍下llm和LLMOps吗"})
)

for chunk in response:
    print(chunk.content, flush=True, end="")