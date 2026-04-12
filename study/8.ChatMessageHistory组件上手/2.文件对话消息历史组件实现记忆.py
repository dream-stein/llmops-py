#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/12 17:20
@Author  : yps302@163.com
@File    : 2.文件对话消息历史组件实现记忆.py
"""
import dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from openai import OpenAI

dotenv.load_dotenv()
# 1.创建openai客户端
client = OpenAI(base_url="https://api.longcat.chat/openai/v1")
chat_history = FileChatMessageHistory("./memory.txt")

# 2.创建一个死循环人机对话
while True:
    # 3.获取人类的输入
    query = input('Human:')

    # 4.判断下输入是否为q 如果是退出
    if query == 'q':
        break

    # 5.向接口发起请求
    system_prompt = (
        "你是OpenAI开发的ChatGPT聊天机器人，可以根据响应的上下文回复用户消息，上下文里存放的是人类与你对话的信息列表。\n\n"
        f"<context>{chat_history}</context>\n\n"
    )

    response = client.chat.completions.create(
        model="LongCat-Flash-Lite",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
        stream=True,
    )
    # 6.循环读取流式内容
    print("AI: ", flush=True, end="")
    ai_content = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        ai_content += content
        print(content, flush=True, end="")
    chat_history.add_user_message(query)
    chat_history.add_ai_message(ai_content)
    print("")
