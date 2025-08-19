#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/19 23:48
#Author  :Emcikem
@File    :chat.py
"""
from langchain_openai import ChatOpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel

class Chat(ChatOpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    pass