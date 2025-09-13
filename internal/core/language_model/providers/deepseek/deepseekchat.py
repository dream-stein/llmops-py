#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/13 15:59
#Author  :Emcikem
@File    :chat.py
"""
from typing import Optional, Sequence, Union, Any, Callable

from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI

from internal.core.language_model.entities.model_entity import BaseLanguageModel


class DeepSeekChat(ChatOpenAI, BaseLanguageModel):

    def get_num_tokens_from_messages(self, messages: list[BaseMessage], tools: Optional[
        Sequence[Union[dict[str, Any], type, Callable, BaseTool]]
    ] = None) -> int:
        return sum(len(message.content) for message in messages)