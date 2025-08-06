#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 22:23
#Author  :Emcikem
@File    :node_entity.py
"""
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

class BaseNodeData(BaseModel):
    """基础节点数据"""
    id: UUID # 节点id，数值必须唯一
    title: str = "" # 节点标题，数据也必须唯一
    description: str = "" # 节点描述信息

class NodeStatus(str, Enum):
    """节点状态"""
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"

class NodeResult(BaseModel):
    """节点运行结果"""
    node_data: BaseNodeData # 节点基础数据
    status: NodeStatus = NodeStatus.RUNNING # 节点运行状态
    inputs: dict[str, Any] = Field(default_factory=dict) # 节点的输入数据
    outputs: dict[str, Any] = Field(default_factory=dict) # 节点的输出数据
    error: str = "" # 节点运行错误信息