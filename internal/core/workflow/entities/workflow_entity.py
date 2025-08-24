#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 22:10
#Author  :Emcikem
@File    :workflow_entity.py
"""
from collections import defaultdict
from typing import Any, TypedDict, Annotated
from uuid import UUID

from pydantic import BaseModel, Field, root_validator
from .node_entity import NodeResult, BaseNodeData

# 工作流配置校验信息
WORKFLOW_CONFIG_NAME_PATTERN = r'^[A-Za-z_][A-Za-z0-9_]*$'
WORKFLOW_CONFIG_DESCRIPTION_MAX_LENGTH = 1024

def _process_dict(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """工作流状态字典归纳函数"""
    # 1.处理left和right出现空的情况
    left = left or {}
    right = right or {}

    # 2.合并更新字典并返回
    return {**left, **right}

def _process_node_results(left: list[NodeResult], right: list[NodeResult]) -> list[NodeResult]:
    """工作流状态节点结果列表归纳函数"""
    # 1.处理left和right
    left = left or []
    right = right or []

    # 2.合并列表更新后返回
    return left + right

class WorkflowConfig(BaseModel):
    """工作流配置信息"""
    account_id: UUID # 用户的唯一标识数据
    name: str = "" # 工作流名称，必须是英文
    description: str = "" # 工作流描述信息，用于告知LLM什么时候需要调用工作流
    nodes: list[dict[str, Any]] = Field(default_factory=list) # 工作流对应的节点
    edges: list[dict[str, Any]] = Field(default_factory=list) # 工作流对应的边

    @root_validator(pre=True)
    def validate_workflow_config(cls, values: dict[str, Any]):
        """自定义校验函数，用于校验尬住了配置中的所有参数信息"""
        pass

    @classmethod
    def _is_connected(cls, adj_list: defaultdict[Any, list], start_node_id: UUID) -> bool:
        """根据传递的邻接表+开始节点id，使用BFS广度优先搜索遍历，检查图是否流通"""
        pass

    @classmethod
    def _is_cycle(
            cls,
            nodes: list[BaseNodeData],
            adj_list: defaultdict[Any, list],
            in_degree: defaultdict[Any, int],
    ) -> bool:
        """根据传递的节点列表、邻接表、入度数据，使用拓扑排序(Kahn算法)检测图中是否存在环，如果存在则返回True，不存在则返回False"""
        pass

    @classmethod
    def _validate_inputs_ref(
            cls,
            node_data_dict: dict[UUID, BaseNodeData],
            reverse_adj_list: defaultdict[Any, list],
    ) -> None:
        """校验输入数据引用是否正确，如果出错则直接抛出异常"""
        pass


class WorkflowState(TypedDict):
    """工作流图程序状态字典"""
    inputs: Annotated[dict[str, Any], _process_dict] # 工作流的最初始输入，也就是工具输入
    outputs: Annotated[dict[str, Any], _process_dict] # 工作流的最终输出结果，也就是工具输出
    node_results: Annotated[list[NodeResult], _process_node_results] # 各节点的运行结果