#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/19 15:26
@Author  : yps302@163.com
@File    : 1.Calback使用.py
"""
import time
from typing import Dict, Any, List, Optional, Union
from uuid import UUID

import dotenv
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import GenerationChunk, ChatGenerationChunk, LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tracers import ConsoleCallbackHandler
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    """自定义llmops回调处理器"""
    start_at: float = 0

    def on_chat_model_start(
            self,
            serialized: Dict[str, Any],
            messages: List[List[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        print("聊天模型开始执行")
        print("serialized:", serialized)
        print("messages:", messages)
        self.start_at = time.time()

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        end_at: float = time.time()
        print("完整输出:", response)
        print("程序消耗:", end_at - self.start_at)

    def on_llm_new_token(
            self,
            token: str,
            *,
            chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        print("token生成了")
        print("token:", token)


# 1.编排prompt
prompt = ChatPromptTemplate.from_template("{query}")

# 2.创建llm
llm = ChatOpenAI(model="LongCat-Flash-Lite", )

# 3.创建输出解析器
parser = StrOutputParser()

# 4.编排链

chain = {"query": RunnablePassthrough()} | prompt | llm | parser

# 5.调用链
resp = chain.stream(
    "你好，你是？",
    config={"callbacks": [ConsoleCallbackHandler(), LLMOpsCallbackHandler()]},
)

for chunk in resp:
    pass
