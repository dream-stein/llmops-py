#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/12 00:32
#Author  :Emcikem
@File    :1Prmpt.py
"""
from datetime import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder

prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
print(prompt.format(subject="喜剧演员"))
print(prompt.invoke({"subject": "超协议"}))

print("==========================")

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAPI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为:{now}"),
    MessagesPlaceholder("chat_history"),
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
]).partial(now=datetime.now)

chat_prompt_value = chat_prompt.invoke({
    "chat_history": [
        ("human", "我叫慕小课"),
        AIMessage("你好，我是chatGPT，有什么可以帮到您")
    ],
    "subject": "程序员",
})

print(chat_prompt_value.to_string())