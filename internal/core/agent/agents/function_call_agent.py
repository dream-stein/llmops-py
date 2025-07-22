#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/22 23:30
#Author  :Emcikem
@File    :function_call_agent.py
"""
from typing import Literal

from langchain_core.messages import AnyMessage, HumanMessage
from langgraph.constants import END
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph

from .base_agent import BaseAgent
from internal.core.agent.entities.agent_entity import AgentState

class FunctionCallAgent(BaseAgent):
    """基于函数/工具调用的智能体"""

    def run(
            self,
            query: str,  # 用户提问原始问题
            history: list[AnyMessage] = None,  # 短期记忆
            long_term_memory: str = "",  # 长期记忆
    ):
        """运行智能体应用，并使用yield关键词返回对应的数据"""
        # 1.预处理传递的消息
        if history is None:
            history = []

        # 2.调用函数构建智能体
        agent = self._build_graph()

        # 3.调用智能体获取数据
        return agent.invoke({
            "messages": [HumanMessage(content=query)],
            "history": history,
            "long_term_memory": long_term_memory,
        })

    def _build_graph(self) -> CompiledStateGraph:
        """构建langGraph图结构编译程序"""
        # 1.创建图
        graph = StateGraph(AgentState)

        # 2.添加节点
        graph.add_node("long_term_memory_recall", self._long_term_memory_recall_node)
        graph.add_node("llm", self._llm_node)
        graph.add_node("tools", self._tools_node)

        # 3.添加边，并设置起点和终点
        graph.set_entry_point("long_term_memory_recall")
        graph.add_edge("long_term_memory_recall", "llm")
        graph.add_conditional_edges("llm", self._tools_condition)
        graph.add_edge("tools", "llm")

        # 4.编译应用并返回
        agent = graph.compiled()

        return agent

    def _long_term_memory_recall_node(self, state: AgentState) -> AgentState:
        """长期记忆召回节点"""
        pass

    def _llm_node(self, state: AgentState) -> AgentState:
        """长期记忆召回节点"""
        pass

    def _tools_node(self, state: AgentState) -> AgentState:
        """工具执行节点"""

    @classmethod
    def _tools_condition(cls, state: AgentState) -> Literal["tools", "__end__"]:
        """检测下一步是执行tools节点，还是直接结束"""
        # 1.提起状态中的最后一条消息(AI消息)
        messages = state["messages"]
        ai_message = messages[-1]

        # 2.检测是否存在tools_call走光参数，如果存在则执行tools节点，否则结束
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"

        return END