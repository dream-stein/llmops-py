#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/11 17:13
@Author  : yps302@163.com
@File    : app_handler.py
"""
import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Dict, Any

from injector import inject
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from langchain_core.tracers import Run
from langchain_openai import ChatOpenAI

from internal.excepiton import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class APPHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用成功创建,id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"成功获取应用，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，ID为{app.id}")

    def ping(self):
        raise FailException("114514")
        # return {"ping": "pong"}

    @classmethod
    def _load_memroy_variables(cls,input:Dict[str,Any],config:RunnableConfig)->Dict[str,Any]:
        """加载记忆变量信息"""
        # 1.从config获取configurable
        configurable=config.get("configurable",{})
        configurable_memory=configurable.get("memory",None)
        if configurable_memory is not None and isinstance(configurable_memory,BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history":[] }

    @classmethod
    def _save_context(cls,run_obj:Run,config:RunnableConfig)->None:
        """存储对应上下文到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs,run_obj.outputs)

    def debug(self, app_id: uuid.UUID):
        """聊天接口"""

        # 1.提取从接口中获取的输入，POST
        # 声明式验证校验输入
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # query = request.json.get("query")
        # 2.创建prompt与记忆
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问回复对应问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}")
        ])
        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        )

        # 3.创建llm
        llm = ChatOpenAI(model="LongCat-Flash-Chat")

        # 4.创建链应用
        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memroy_variables) | itemgetter("history")
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # 5.调用链生成内容

        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input,config={"configurable":{"memory":memory}})

        # # 2.构建组件
        # prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="LongCat-Flash-Lite")
        # parser = StrOutputParser()
        #
        # # 3.构建链
        # chain = prompt | llm | parser
        #
        # # 4.调用链得到结果
        # content = chain.invoke({"query": req.query.data})

        return success_json({"content": content})
