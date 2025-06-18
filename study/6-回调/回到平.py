#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/19 00:23
#Author  :Emcikem
@File    :回到平.py
"""
from typing import Any, Optional
from uuid import UUID

import dotenv
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler

dotenv.load_dotenv()

class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义LLMOps回调处理器"""
    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行")
        print("serialized", serialized)
        print("messages", messages)

# 1.构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-chat")

chain = {"query": RunnablePassthrough()} | prompt | llm | StrOutputParser()

content = chain.invoke(
    "你好，你是？" ,
    config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]},
)

print(content)