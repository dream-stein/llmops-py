#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/22 17:23
#Author  :Emcikem
@File    :1.RunnableWithMessage.py
"""

import dotenv
from flask_migrate import history
from operator import itemgetter

from langchain.schema import storage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from  langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory, ConversationTokenBufferMemory
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import FileChatMessageHistory

dotenv.load_dotenv()

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = FileChatMessageHistory("./chat_history_{session_id}.txt")
    return store[session_id]

# 1.创建提示模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAi开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}"),
])

# 2.创建大语言模型
llm = ChatOpenAI(model="deepseek-chat")

# 3.构建链
chain = prompt | llm | StrOutputParser()

with_message_chain = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="query",
    history_messages_key="history",
)

# 4.构建对话命令行
while True:
    query = input("Human: ")

    if query == 'q':
        exit(0)

    response = with_message_chain.stream(
        {"query": query},
        config={"configurable": {"session_id": "muxiaoke"}}
    )
    print("AI: ", flush=True, end="")
    for chunk in response:
        print(chunk, flush=True, end="")
    print("")
