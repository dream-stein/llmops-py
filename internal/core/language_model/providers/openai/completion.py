#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/19 23:50
#Author  :Emcikem
@File    :completion.py
"""
from langchain_openai import OpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class Completion(OpenAI, BaseLanguageModel):
    """OpenAI聊天模型基类"""
    pass