#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/7 00:12
#Author  :Emcikem
@File    :end_node.py
"""
from typing import Optional, Any

from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output

from internal.core.workflow.entity.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entity.variable_entity import VariableValueType, VariableDefaultVaultValueMap
from internal.core.workflow.entity.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.end.end_entity import EndNodeData


class EndNode(BaseNode):
    """结束节点"""

    _node_data_cls = EndNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """结束节点执行函数，提取出状态中需要展示的数据，并更新outputs"""
        # 1.提取节点中需要输出的数据
        outputs = self.node_data.outputs

        # 2.循环遍历所有需要输出的数据
        outputs_dict = {}
        for output in outputs:
            # 3.判断输出字段是引用还是直接输入
            if output.value.type == VariableValueType.LITERAL:
                outputs_dict[output.name] = output.value.content
            else:
                # 4.引用数据类型，遍历节点并提取
                for node_result in state["node_results"]:
                    if node_result.node_data.id == output.value.content.ref_node_id:
                        outputs_dict[output.name] = node_result.outputs.get(
                            outputs.value.content.ref_var_name,
                            VariableDefaultVaultValueMap.get(output.type)
                        )

        # 5.组装状态并返回
        return {
            "outputs": outputs_dict,
            "node_results": [
                NodeResult(
                    node_data=self.node_data,
                    status=NodeStatus.SUCCEEDED,
                    inputs={},
                    outputs=outputs_dict,
                )
            ]
        }