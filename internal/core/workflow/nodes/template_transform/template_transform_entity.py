#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/9 18:30
#Author  :Emcikem
@File    :template_transform_entity.py
"""
from pydantic import Field

from internal.core.workflow.entity.node_entity import BaseNodeData
from internal.core.workflow.entity.variable_entity import VariableEntity, VariableValueType


class TemplateTransformNodeData(BaseNodeData):
    """模板转换节点数据"""
    template: str = "" # 需要拼接转换的字符模板
    inputs: list[VariableEntity] = Field(default_factory=list) # 输入列表信息
    outputs: list[VariableEntity] = Field(
        exclude=True,
        default_factory=lambda :[
            VariableEntity(name="output", value={"type": VariableValueType.GENERATED}),
        ]
    )