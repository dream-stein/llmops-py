#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/9 18:37
#Author  :Emcikem
@File    :template_transform_node.py
"""
from typing import Optional, Any

from jinja2 import Template
from langchain_core.runnables import RunnableConfig

from internal.core.workflow.entity.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entity.variable_entity import VariableValueType, VariableDefaultVaultMap
from internal.core.workflow.entity.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.template_transform.template_transform_entity import TemplateTransformNodeData


class TemplateTransformNode(BaseNode):
    """模板转换节点，将多个变量信息合并成一个"""

    _node_data_cls = TemplateTransformNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """模板转换节点执行函数，将传递的多个变量合并成字符串后返回"""
        # 1.提取节点中的输入数据
        inputs = self.node_data.inputs

        # 2.循环遍历输入数据，并提取需要的数据
        inputs_dict = {}
        for input in inputs:
            # 3.判断数据是引用还是直接输入
            if input.value.type == VariableValueType.LITERAL:
                inputs_dict[input.name] = input.value.content
            else:
                # 4.引用的类型，遍历节点获取数据
                for node_result in state["node_results"]:
                    if node_result.node_data.id == input.value.content.ref_node_id:
                        inputs_dict[input.name] = node_result.outputs.get(
                            input.value.content.ref_var_name,
                            VariableDefaultVaultMap.get(input.type)
                        )

        # 5.使用jinja2格式模板消息
        template = Template(self.node_data.template)
        template_value = template.render(**inputs_dict)

        # 6.提取并构建输出数据结构
        outputs = {}
        if self.node_data.outputs:
            outputs[self.node_data.outputs[0].name] = template_value
        else:
            outputs["output"] = template_value

        # 7.构建响应状态并返回
        return {
            "node_results": [
                NodeResult(
                    node_data=self.node_data,
                    status=NodeStatus.SUCCEEDED,
                    inputs=inputs_dict,
                    outputs=outputs,
                )
            ]
        }