#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/24 20:07
#Author  :Emcikem
@File    :react_agent.py
"""
import uuid

from .function_call_agent import FunctionCallAgent
from ..entities.agent_entity import AgentState
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

        # 3.