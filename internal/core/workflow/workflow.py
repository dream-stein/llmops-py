#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 22:08
#Author  :Emcikem
@File    :workflow.py
"""
from typing import Any, Optional, Iterator

from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langchain_core.tools import BaseTool
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import PrivateAttr

from .entity.workflow_entity import WorkflowConfig, WorkflowState

class Workflow(BaseTool):
    """工作流LangChain工具类"""
    _workflow_config: WorkflowConfig = PrivateAttr(None)
    _workflow: CompiledStateGraph = PrivateAttr(None)

    def __init__(self, workflow_config: WorkflowConfig, **kwargs: Any):
        """构造函数，完成工作流函数的初始化"""
        # 1.调用父类构造函数完成基础数据初始化
        super().__init__(
            name=workflow_config.name,
            description=workflow_config.description,
            **kwargs
        )

        # 2.完善工作流配置与工作流图结构层序的初始化
        self._workflow_config = workflow_config
        self._workflow = self._build_workflow()

    def _build_workflow(self) -> CompiledStateGraph:
        """构建编译后的工作流图程序"""
        # 1.创建graph层序结构
        graph = StateGraph(WorkflowState)

        # 2.提取nodes和edges信息
        # 3.循环遍历nodes节点信息添加节点
        # 4.循环遍历edges信息添加边
        # 5.构建图程序并编译
        return graph.compile()


    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """工作流组件基础run方法"""
        return self._workflow.invoke({"inputs", kwargs})

    def stream(
        self,
        input: Input,
        config: Optional[RunnableConfig] = None,
        **kwargs: Optional[Any],
    ) -> Iterator[Output]:
        """工作流流式输出每个节点对应的结果"""
        return self._workflow.stream({"input", input})