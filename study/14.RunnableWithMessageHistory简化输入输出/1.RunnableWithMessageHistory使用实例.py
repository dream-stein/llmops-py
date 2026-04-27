#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/18 15:23
@Author  : yps302@163.com
@File    : 1.缓冲窗口记忆.py
"""
from operator import itemgetter

import dotenv
from langchain.memory import ConversationTokenBufferMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

store={}

dotenv.load_dotenv()

def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=FileChatMessageHistory(f"./chat_history_{session_id}.txt")
    return store[session_id]


# 1.创建提示模板和记忆
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}")
])


# 2.创建大语言模型
llm = ChatOpenAI(model="LongCat-Flash-Chat")

# 3.构建链应用

chain =  prompt | llm | StrOutputParser()

# chain.with_listeners(on_end=) 也能实现RunnableWithMessageHistory的效果

# 包装链
with_message_chain=RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
)

# 4.死循环构建对话命令
while True:
    query = input("Human:")

    if query == "q":
        exit(0)


    response = with_message_chain.stream(
        {"query": query},
        config={"configurable": {"session_id": "muxiaoke"}},
    )
    print("AI: ", flush=True, end="")
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end='')
    print("")
