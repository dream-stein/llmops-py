#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/12 16:46
@Author  : yps302@163.com
@File    : 1.对话消息历史组件基础.py
"""
from langchain_core.chat_history import InMemoryChatMessageHistory

chat_history = InMemoryChatMessageHistory()

chat_history.add_user_message("你好 我是野兽先辈 你是谁")
chat_history.add_ai_message("你好 我是ChatGPT 有什么可以帮你的")

print(chat_history)
