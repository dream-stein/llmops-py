#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 23:36
#Author  :Emcikem
@File    :base_node.py
"""
from abc import ABC
from typing import Any

from langchain_core.runnables import RunnableSerializable

from internal.core.workflow.entity.node_entity import BaseNodeData


class BaseNode(RunnableSerializable, ABC):
    """工作流节点基类"""
    _node_data_cls: type[BaseNodeData]
    node_data: BaseNodeData

    def __init__(self, *args: Any, node_data: dict[str, Any], **kwargs: Any):
        super().__init__(*args, node_data=self._node_data_cls(**node_data), **kwargs)