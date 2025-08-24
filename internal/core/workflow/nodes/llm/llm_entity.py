#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/8 00:11
#Author  :Emcikem
@File    :llm_entity.py
"""
from typing import Any

from pydantic import Field

from internal.core.workflow.entities.node_entity import BaseNodeData
from internal.core.workflow.entities.variable_entity import VariableEntity, VariableValueType
from internal.entity.app_entity import DEFAULT_APP_CONFIG


class LLMNodeData(BaseNodeData):
    """大语言模型节点数据"""
    prompt: str  # 大语言模型节点提示词
    language_model_config: dict[str, Any] = Field(
        alias="model_config",
        default_factory=lambda: DEFAULT_APP_CONFIG["model_config"],
    )  # 大语言模型配置信息
    inputs: list[VariableEntity] = Field(default_factory=list)  # 输入列表信息
    outputs: list[VariableEntity] = Field(
        exclude=True,
        default_factory=lambda: [
            VariableEntity(name="output", value={"type": VariableValueType.GENERATED})
        ]
    )