#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/17 23:30
#Author  :Emcikem
@File    :2.modle批处理.py
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

ai_messages = llm.batch([
    prompt.invoke({"query", "你好,讲个笑话"}),
    prompt.invoke({"query", "你好"})
    ]
)

for ai_message in ai_messages:
    print(ai_message.content)
    print("=========")