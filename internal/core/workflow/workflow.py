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
from pydantic import PrivateAttr, BaseModel, Field, create_model

from .entity.node_entity import NodeType
from .entity.variable_entity import VariableTypeMap
from .entity.workflow_entity import WorkflowConfig, WorkflowState
from .nodes import StartNode, EndNode

# 节点类映射
NodeClasses = {
    NodeType.START: StartNode,
    NodeType.END: EndNode,
}

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
            args_schema=self._build_args_schema,
            **kwargs
        )

        # 2.完善工作流配置与工作流图结构层序的初始化
        self._workflow_config = workflow_config
        self._workflow = self._build_workflow()

    @classmethod
    def _build_args_schema(cls, workflow_config: WorkflowConfig) -> type[BaseModel]:
        """构建输入参数结构体"""
        # 1.提取开始节点的输入参数信息
        fields = {}
        inputs = next(
            (node.get("inputs", []) for node in workflow_config.nodes if node.get("node_type") == NodeType.START),
            []
        )

        # 2.循环遍历所有输入信息并创建字段映射
        for input in inputs:
            field_name = input.get("name")
            field_type = VariableTypeMap.get(input.get("type"), str)
            field_required = input.get("required", True)
            field_description = input.get("description", "")

            fields[field_name] = (
                field_type if field_required else Optional[field_type],
                Field(description=field_description),
            )

        # 3.调用create_model创建一个BaseModel类，并使用上述分析好的字段
        return create_model("DynamicModel", **fields)

    def _build_workflow(self) -> CompiledStateGraph:
        """构建编译后的工作流图程序"""
        # 1.创建graph层序结构
        graph = StateGraph(WorkflowState)

        # 2.提取nodes和edges信息
        nodes = self._workflow_config.nodes
        edges = self._workflow_config.edges

        # 3.循环遍历nodes节点信息添加节点
        for node in nodes:
            if node.get("node_type") == NodeType.START:
                graph.add_node(
                    f"{NodeType.START.value}_{node.get('id')}",
                    NodeClasses[NodeType.START](node_data=node),
                )
                pass
            elif node.get("node_type") == NodeType.END:
                graph.add_node(
                    f"{NodeType.END.value}_{node.get('id')}",
                    NodeClasses[NodeType.END](node_data=node),
                )
                pass

        # 4.循环遍历edges信息添加边
        for edge in edges:
            # 5.添加边映射关系
            graph.add_edge(
                f"{edge.get('source_type')}_{edge.get('source')}",
                f"{edge.get('target_type')}_{edge.get('target')}",
            )

            # 6.检测特殊节点（开始节点、结束节点）
            if edge.get("source_type") == NodeType.START:
                graph.set_entry_point(f"{edge.get('source_type')}_{edge.get('source')}")
            elif edge.get("target_type") == NodeType.END:
                graph.set_finish_point(f"{edge.get('target_type')}_{edge.get('target')}")

        # 7.构建图程序并编译
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