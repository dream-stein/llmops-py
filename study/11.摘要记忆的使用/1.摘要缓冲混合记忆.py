#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/18 15:23
@Author  : yps302@163.com
@File    : 1.摘要缓冲混合记忆.py
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.创建提示模板和记忆
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}")
])
# memory = ConversationBufferWindowMemory(
#     k=2,
#     return_messages=True,
# )

memory = ConversationSummaryBufferMemory(
    max_token_limit=300,
    return_messages=True,
    input_key="query",
    llm=ChatOpenAI(
        model="LongCat-Flash-Chat",
        # tiktoken_model_name 告诉 LangChain 本地计算 Token 时参考哪个标准
        tiktoken_model_name="gpt-3.5-turbo"
    ),
    # prompt=prompt,
)

# 2.创建大语言模型
llm = ChatOpenAI(model="LongCat-Flash-Chat")

# 3.构建链应用

chain = RunnablePassthrough.assign(
    history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
) | prompt | llm | StrOutputParser()

# 4.死循环构建对话命令
while True:
    query = input("Human:")

    if query == "q":
        exit(0)

    chain_input = {"query": query}

    response = chain.stream(chain_input)
    print("AI: ", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end='')
    memory.save_context(chain_input, {"output": output})
    print("")
    print("history: ", memory.load_memory_variables({}))
