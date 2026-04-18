#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/18 14:51
@Author  : yps302@163.com
@File    : 1.BaseChatMemory.py
"""
from langchain.memory.chat_memory import BaseChatMemory

memory = BaseChatMemory(
    input_key="query",
    output_key="output",
    return_messages=True,
    # chat_history 假设
)

memory_variable = memory.load_memory_variables({})
# content=chain.invoke(xxx)
# memory.save_context(xxx)
