#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/10 16:57
@Author  : yps302@163.com
@File    : 1.少量实例策略.py
"""
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.构建示例模板与示例
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}"),
    ("ai", "{answer}"),
])
examples = [
    {"question": "帮我计算下2+2等于多少？", "answer": "哈哈哈是4"},
    {"question": "帮我计算下2+3等于多少？", "answer": "哈哈哈是5"},
    {"question": "帮我计算下20*15等于多少？", "answer": "哈哈哈是300"},
]

# 2.构建少量示例提示模板
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
print("少量示例模板:", few_shot_prompt.format())

# 3.构建最终提示模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个可以计算复杂数学问题的聊天机器人,你必须严格模仿示例的回答格式."),
    few_shot_prompt,
    ("human", "{question}"),
])

# 4.创建大语言模型与链
llm = ChatOpenAI(model="LongCat-Flash-Chat", temperature=0)
chain = prompt | llm | StrOutputParser()

# 5.调用链获取结果
print(chain.invoke("帮我计算下14*15等于多少"))
