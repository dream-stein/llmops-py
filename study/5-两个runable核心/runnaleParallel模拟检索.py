#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/18 23:35
#Author  :Emcikem
@File    :runnaleParallel模拟检索.py
"""
import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from operator import itemgetter

dotenv.load_dotenv()

def retrieval(query: str) -> str:
    print("检索器执行")
    return "我是木小可"

prompt = ChatPromptTemplate.from_template("""请根据用户的问题，可以参考对应的上下文

<context>
{context}
</context>

用户提问是：{query}""")

llm = ChatOpenAI(model="deepseek-chat")

parser = StrOutputParser()

chain = {
        "context": retrieval,
        "query": RunnablePassthrough(),
} | prompt | llm | parser

content = chain.invoke("你好")

print(content)