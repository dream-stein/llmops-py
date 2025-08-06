#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/6 23:57
#Author  :Emcikem
@File    :start_node.py
"""
from typing import Optional, Any

from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output

from internal.core.workflow.nodes import BaseNode
from internal.exception import FailException
from .start_entity import StartNodeData
from ...entity.node_entity import NodeResult, NodeStatus
from ...entity.variable_entity import VariableDefaultVaultValueMap
from ...entity.workflow_entity import WorkflowState


class StartNode(BaseNode):
    """开始节点"""

    _node_data_cls = StartNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """开始节点执行函数，该函数会提取状态中的输入信息并生成节点结果"""
        # 1.提取节点数据中的数据
        inputs = self.node_data.inputs

        # 2.循环遍历输入数据，并提取需要的数据，同时检测必填的数据是否传递，如果无传递则直接报错
        outputs = {}
        for input in inputs:
            input_value = state["inputs"].get(input.name, None)

            # 3.检测字段是否必填，如果是则检测是否幅值
            if input_value is None:
                if input.required:
                    raise FailException(f"工作流参数生成出错，{input.name}为必填参数")
                else:
                    input_value = VariableDefaultVaultValueMap.get(input.type)

            # 4.提取出输出数据
            outputs[input.name] = input_value

        # 5.构建状态数据并返回
        return {
            "node_results": [
                NodeResult(
                    node_data=self.node_data,
                    status=NodeStatus.SUCCEEDED,
                    inputs=state["inputs"],
                    outputs=outputs,
                )
            ]
        }