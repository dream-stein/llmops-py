#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/17 22:31
#Author  :Emcikem
@File    :3.消息表示.py
"""
from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAPI开发的聊天机器人，请根据用户的提问回复，我叫{username}")
])
human_chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}")
])

chat_prompt = system_chat_prompt + human_chat_prompt

print(chat_prompt.invoke({
    "username": "母校可",
    "query": "你好"
}))