#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 23:40
#Author  :Emcikem
@File    :start_entity.py
"""
from internal.core.workflow.entity.node_entity import BaseNodeData
from internal.core.workflow.entity.variable_entity import VariableEntity
from pydantic import Field

class StartNodeData(BaseNodeData):
    """开始节点数据"""
    inputs: list[VariableEntity] = Field(default_factory=list) # 开始节点的输入变量信息