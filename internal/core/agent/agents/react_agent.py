#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/24 20:07
#Author  :Emcikem
@File    :react_agent.py
"""
import time
import uuid

from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage, messages_to_dict, AIMessage
from langchain_core.tools import render_text_description_and_args

from internal.exception import FailException
from .function_call_agent import FunctionCallAgent
from ..entities.agent_entity import AgentState, AGENT_SYSTEM_PROMPT_TEMPLATE, REACT_AGENT_SYSTEM_PROMPT_TEMPLATE, \
    MAX_ITERATION_RESPONSE
from ..entities.queue_entity import AgentThought, QueueEvent
from ...language_model.entities.model_entity import ModelFeature


class ReACTAgent(FunctionCallAgent):
    """基于ReAct推理的智能体，继承FunctionCallAgent，并重写long_term_memory_node和llm_node两个节点"""

    def _long_term_memory_recall_node(self, state: AgentState) -> AgentState:
        """重写长期记忆召回节点，使用prompt实现工具调用及规范数据生成"""
        # 1.判断是否支持工具调用，如果支持工具调用，则可以直接使用工具智能体的长期记忆召回节点
        if ModelFeature.TOOL_CALL in self.llm.features:
            return super()._long_term_memory_recall_node(state)

        # 2.根据传递的智能体配置判断是否需要召回长期记忆
        long_term_memory = ""
        if self.agent_config.enable_long_term_memory:
            long_term_memory = state["long_term_memory"]
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.LONG_TERM_MEMORY_RECALL,
                observation=long_term_memory,
            ))

        # 3.检测是否支持AGENT_THOUGHT，如果不支持，则使用没有工具描述的prompt
        if ModelFeature.AGENT_THOUGHT not in self.llm.features:
            preset_messages = [
                SystemMessage(AGENT_SYSTEM_PROMPT_TEMPLATE.format(
                preset_prompt=self.agent_config.preset_prompt,
                long_term_memory=long_term_memory,
                ))
            ]
        else:
            # 4.支持智能体推理，则使用REACT_AGENT_SYSTEM_PROMPT_TEMPLATE并添加工具描述
            preset_messages = [
                SystemMessage(REACT_AGENT_SYSTEM_PROMPT_TEMPLATE.format(
                    preset_prompt=self.agent_config.preset_prompt,
                    long_term_memory=long_term_memory,
                    tool_description=render_text_description_and_args(self.agent_config.tools),
                ))
            ]

        # 5.将短期历史消息添加到消息列表中
        history = state["history"]
        if isinstance(history, list) and len(history) > 0:
            # 66.校验历史消息是不是复数形式，也就是[人类消息, AI消息, 人类消息, AI消息, ...]
            if len(history) % 2 != 0:
                self.agent_queue_manager.publish_error(state["task_id"], "智能体历史消息列表格式错误")
                raise FailException("智能体历史消息列表格式错误")
            # 7.拼接历史消息
            preset_messages.extend(history)

        # 8.拼接当前用户的提问消息
        human_message = state["messages"][-1]
        preset_messages.append(HumanMessage(human_message.content))

        # 9.处理预设消息，将预设消息添加到用户消息前，先去删除用户的原始消息，然后补充一个新的代替
        return {
            "messages": [RemoveMessage(id=human_message.id), *preset_messages],
        }

    def _llm_node(self, state: AgentState) -> AgentState:
        """重写工具调用智能体的LLM节点"""
        # 1.判断当前LLM是否支持tool_call，如果是则使用FunctionCallAgent的llm_node
        if ModelFeature.TOOL_CALL in self.llm.features:
            return super()._llm_node(state)

        # 2.检测当前Agent迭代次数是否符合需求
        if state["iteration_count"] > self.agent_config.MAX_ITERATION_COUNT:
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.AGENT_MESSAGE,
                thought=MAX_ITERATION_RESPONSE,
                message=messages_to_dict(state["messages"]),
                answer=MAX_ITERATION_RESPONSE,
                latency=0,
            ))
            self.agent_queue_manager.publish(state["task_id"], AgentThought(
                id=uuid.uuid4(),
                task_id=state["task_id"],
                event=QueueEvent.AGENT_END,
            ))
            return {"messages": [AIMessage(MAX_ITERATION_RESPONSE)]}

        # 3.从智能体配置中提取大语言模型
        id = uuid.uuid4()
        start_at = time.perf_counter()
        llm = self.llm

        # 4.定义变量存储流式输出内容
        gathered = None
        is_first_chunk = True
        generation_type = ""

        # 5.流式输出调用LLM，并判断输出内容是否以"```json"为开头，用于区分工具调用和文本生成
        for chunk in  llm.stream(state["messages"]):
            # 6.处理流式输出内容块叠加
            if is_first_chunk:
                gathered = chunk
                is_first_chunk = False
            else:
                gathered += chunk

            # 7.如果生成的是消息则提交智能体消息事件
            if generation_type == 'messages':
                pass
