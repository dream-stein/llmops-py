#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/11 23:08
#Author  :Emcikem
@File    :code_entity.py
"""
from pydantic import Field

from internal.core.workflow.entities.node_entity import BaseNodeData
from internal.core.workflow.entities.variable_entity import VariableEntity

# 默认的code代码
DefaultCode = """
def main(params):
    return params
"""

class CodeNodeData(BaseNodeData):
    """Python代码执行节点数据"""
    code: str = DefaultCode # 需要执行的Python代码
    inputs: list[VariableEntity] = Field(default_factory=list) # 输入变量列表
    outputs: list[VariableEntity] = Field(default_factory=list) # 输出变量列表