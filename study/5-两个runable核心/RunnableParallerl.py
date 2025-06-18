#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/18 23:25
#Author  :Emcikem
@File    :RunnableParallerl.py
"""
import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()

joke_prompt = ChatPromptTemplate.from_template("请讲一篇关于{subject}的冷笑话,短点")
poem_prompt = ChatPromptTemplate.from_template("请写一篇关于{subject}的诗，短点")


llm = ChatOpenAI(model="deepseek-chat")

parser = StrOutputParser()

joke_chain = joke_prompt | llm | parser
poem_chain = poem_prompt | llm | parser

map_chain = RunnableParallel(
    joke=joke_chain,
    poem= poem_chain,
)

res = map_chain.invoke({
    "subject": "程序员"
})

print(res)
