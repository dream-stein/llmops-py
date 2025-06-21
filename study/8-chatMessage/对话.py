#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/20 23:43
#Author  :Emcikem
@File    :对话.py
"""
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

chat_history = InMemoryChatMessageHistory()

chat_history.add_user_message("你好，我是木小可，你是谁")

chat_history.add_ai_message("你好，我是chatgpt")

print(chat_history)