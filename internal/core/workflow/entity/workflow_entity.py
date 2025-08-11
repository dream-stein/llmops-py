#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 22:10
#Author  :Emcikem
@File    :workflow_entity.py
"""
from typing import Any, TypedDict, Annotated
from uuid import UUID

from pydantic import BaseModel, Field
from .node_entity import NodeResult

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

class WorkflowState(TypedDict):
    """工作流图程序状态字典"""
    inputs: Annotated[dict[str, Any], _process_dict] # 工作流的最初始输入，也就是工具输入
    outputs: Annotated[dict[str, Any], _process_dict] # 工作流的最终输出结果，也就是工具输出
    node_results: Annotated[list[NodeResult], _process_node_results] # 各节点的运行结果