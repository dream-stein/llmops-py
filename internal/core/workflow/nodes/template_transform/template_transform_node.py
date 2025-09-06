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

from internal.core.workflow.entities.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entities.variable_entity import VariableValueType, VARIABLE_TYPE_DEFAULT_VALUE_MAP
from internal.core.workflow.entities.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.template_transform.template_transform_entity import TemplateTransformNodeData
from internal.core.workflow.utils.helper import extract_variables_from_state


class TemplateTransformNode(BaseNode):
    """模板转换节点，将多个变量信息合并成一个"""

    _node_data_cls = TemplateTransformNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """模板转换节点执行函数，将传递的多个变量合并成字符串后返回"""
        # 1.循环遍历输入数据，并提取需要的数据
        inputs_dict = extract_variables_from_state(self.node_data.inputs, state)

        # 2.使用jinja2格式模板消息
        template = Template(self.node_data.template)
        template_value = template.render(**inputs_dict)

        # 3.提取并构建输出数据结构
        outputs = {"outputs": template_value}

        # 4.构建响应状态并返回
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