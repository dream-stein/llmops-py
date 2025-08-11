#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/11 23:57
#Author  :Emcikem
@File    :tool_entity.py
"""
from typing import Any

from pydantic import Field

from internal.core.workflow.entity.node_entity import BaseNodeData
from internal.core.workflow.entity.variable_entity import VariableEntity, VariableValueType


class ToolNodeData(BaseNodeData):
    """工具节点数据"""
    tool_type: str = Field(alias="type") # 工具类型
    provider_id: str # 工具提供者id
    tool_id: str # 工具id
    params: dict[str, Any] = Field(default_factory=dict) # 内置工具设置参数
    inputs: list[VariableEntity] = Field(default_factory=list) # 输入变量列表
    outputs: list[VariableEntity] = Field(
        exclude=True,
        default_factory=lambda :[
            VariableEntity(name="text", value={"type": VariableValueType.GENERATED})
        ]
    ) # 输出字段列表信息