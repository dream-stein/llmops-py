#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 13:51
#Author  :Emcikem
@File    :app_handler.py
"""
import json
import os
from queue import Queue
import uuid
from dataclasses import dataclass
from operator import itemgetter
from typing import Any

from injector import inject
from langchain_core.documents import Document
from langchain_core.memory import BaseMemory
from langchain_core.tracers import Run
from uuid import UUID

from internal.schema.app_schema import CompletionReq
from internal.service import AppService, BuiltinToolService, ConversationService
from pkg.response import success_json, validate_error_json, success_message
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableConfig
from internal.service import ApiToolService
from internal.task.demo_task import demo_task
from internal.core.tools.builtin_tools.providers import BuiltinProviderManager

@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService
    api_tool_service: ApiToolService
    builtin_provider_manager: BuiltinProviderManager
    conversation_service: ConversationService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经创建成功，id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是:{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id为:{app.id}")

    @classmethod
    def _load_memory_variables(cls, input: dict[str, Any], config: RunnableConfig) -> dict[str, Any]:
        """加载记忆变量信息"""
        # 1.从config中获取configurable
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            return configurable_memory.load_memory_variables(input)
        return {"history": []}

    @classmethod
    def _save_context(cls, run_obj: Run, config: RunnableConfig) -> None:
        """存储对应的上下文信息到记忆实体中"""
        configurable = config.get("configurable", {})
        configurable_memory = configurable.get("memory", None)
        if configurable_memory is not None and isinstance(configurable_memory, BaseMemory):
            configurable_memory.save_context(run_obj.inputs, run_obj.outputs)

    def debug(self, app_id: UUID):
        """应用会话调试聊天接口，该接口为流式事件输出"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建队列并读取query数据
        q = Queue()
        query = req.query.data

        # 3.创建graph图程序应用
        def graph_app() -> None:
            """创建Graph图程序应用并执行"""
            # 3.1创建tools工具列表
            tools = [
                self.builtin_provider_manager.get_tool("google", "google_serper")(),
                self.builtin_provider_manager.get_tool("gaode", "gaode_weather")(),
                self.builtin_provider_manager.get_tool("dalle", "dalle3")(),
            ]

            # # 3.2定义大语言模型/聊天机器人节点
            # def chatbot(state: MessagesState) -> MessagesState:
            #     """聊天机器人节点"""
            #     # 3.2.1创建LLM大语言模型
            #     llm = ChatOpenAI(model="deepseek-chat", temperature=0.7).bind_tools(tools)
            #
            #     # 3.2.2调用stream()函数获取流式输出内容，并判断生成内容是文本还是工具调用参数
            #     is_first_chunk = True
            #     is_tool_call = False
            #     gathered = None
            #     id = str(uuid.uuid4())
            #     for chunk in llm.stream(state["messages"]):
            #         # 3.2.3检测是不是第一个快，部分LLM的第一个块不会生成内容，需要抛弃掉
            #         if is_first_chunk and chunk.content == "" and not chunk.tool_calls:
            #             continue
            #
            #         # 3.2.4叠加相应的区块
            #         if is_first_chunk:
            #             gathered = chunk
            #             is_first_chunk = None
            #         else:
            #             gathered += chunk
            #
            #         # 3.2.5判断是工具调用还是文本生成，往队列中添加中添加不同的数据
            #         if chunk.tool_calls or is_tool_call:
            #             is_tool_call = True
            #             q.put({
            #                 "id": id,
            #                 "event": "agent_thought",
            #                 "data": json.dumps(chunk.tool_calls),
            #             })
            #         else:


    def _debug(self, app_id: UUID):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.创建prompt与记忆
        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能根据用户的提问回复对应的问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])
        memory = ConversationBufferWindowMemory(
            k=3,
            input_key="query",
            output_key="output",
            return_messages=True,
            chat_memory=FileChatMessageHistory("./storage/memory/chat_history.txt"),
        )

        # 3.创建llm
        llm = ChatOpenAI(model="deepseek-chat")

        # 4.创建链应用
        chain = (RunnablePassthrough.assign(
            history=RunnableLambda(self._load_memory_variables) | itemgetter("history")
        ) | prompt | llm | StrOutputParser()).with_listeners(on_end=self._save_context)

        # 5.调用链得到结果
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input, config={"configurable": {"memory": memory}})

        return success_json({"content": content})

    @classmethod
    def _combine_documents(cls, documents: list[Document]) -> str:
        """将传入的文档列表合并成字符串"""
        return "\n\n".join([document.page_content for document in documents])

    def ping(self):
        # human_message = "我叫木小可，你是？"
        # ai_message = "你好，我是ChatGPT，有什么可以帮到你的？"
        # old_summary = "人类询问AI关于LLM（大型语言模型）和Agent（智能体）的定义。AI解释称：  \n- **LLM**是基于海量文本训练的语言模型，擅长理解和生成自然语言（如GPT-4），但需明确指令且缺乏主动行动力；  \n- **Agent**是具备自主决策能力的智能系统，能规划任务、调用工具（如API），常以LLM为“大脑”但扩展了行动模块。  \nAI总结两者的区别为：LLM是“语言大脑”，Agent是“能动手执行的完整智能体”。"
        # summary = self.conversation_service.summary(human_message, ai_message, old_summary)
        # return success_json({"summary": summary})

        # human_message = "你好，我叫木小可，你是？"
        # conversation_name = self.conversation_service.generate_conversation_name(human_message)
        # return success_json({"conversation_name": conversation_name})

        # human_message = "你能简单介绍下什么是LLM么？LLM与Agent之间有什么关联？"
        # questions = self.conversation_service.generate_suggested_questions(human_message)
        # return success_json({"questions": questions})
        from internal.core.agent.agents import FunctionCallAgent
        from internal.core.agent.entities.agent_entity import AgentConfig
        from langchain_openai import ChatOpenAI

        agent = FunctionCallAgent(AgentConfig(
            llm=ChatOpenAI(model="deepseek-chat"),
            preset_prompt="你是一个拥有20年经验的诗人，请根据用户提供的主题来写一首诗"
        ))
        state = agent.run("程序员", [], "")
        content = state["content"][-1].content

        return success_json({"content": content})


