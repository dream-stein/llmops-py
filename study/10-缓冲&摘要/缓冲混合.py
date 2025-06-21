#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/21 14:13
#Author  :Emcikem
@File    :缓冲混合.py
"""
import dotenv
from flask_migrate import history
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from  langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationBufferMemory, ConversationTokenBufferMemory, ConversationSummaryBufferMemory
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

dotenv.load_dotenv()

# 1.创建提示模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAi开发的聊天机器人，请根据对应的上下文回复用户问题"),
    MessagesPlaceholder("history"),
    ("human", "{query}"),
])
memory = ConversationSummaryBufferMemory(
    max_token_limit=500,
    return_messages=True,
    input_key="query",
    llm=ChatOpenAI(model="deepseek-chat"),
)

# 2.创建大语言模型
llm = ChatOpenAI(model="deepseek-chat")

# 3.构建链
chain = RunnablePassthrough.assign(
    history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
)| prompt | llm | StrOutputParser()

# 4.构建对话命令行
while True:
    query = input("Human: ")

    if query == 'q':
        exit(0)

    chain_input = {"query": query}

    response = chain.stream(chain_input)
    print("AI: ", flush=True, end="")
    output = ""
    for chunk in response:
        print(chunk, flush=True, end="")
        output += chunk
    memory.save_context(chain_input, {"output": output})
    print("")
    print("history: ", memory.load_memory_variables({}))