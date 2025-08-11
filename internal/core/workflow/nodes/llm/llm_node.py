#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/8 00:19
#Author  :Emcikem
@File    :llm_node.py
"""
from typing import Optional, Any

from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output
from langchain_openai import ChatOpenAI

from internal.core.workflow.entity.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entity.variable_entity import VariableValueType, VariableDefaultVaultMap
from internal.core.workflow.entity.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.llm.llm_entity import LLMNodeData


class LLMNode(BaseNode):
    """大语言模型节点"""

    node_data: LLMNodeData

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """大语言模型节点调页根据，根据输入字段+预设prompt生成对应内容后输出"""
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
        template = Template(self.node_data.prompt)
        prompt_value = template.render(**inputs_dict)

        # ToDo：6.根据配置创建LLM实例，等待堕LLM接入时需要完善
        llm = ChatOpenAI(
            model=self.node_data.language_model_config.get("model", "deepseek-chat")
            **self.node_data.language_model_config.get("parameters", {}),
        )

        # 7.调用LLM并传递prompt后提取数据
        content = llm.invoke(prompt_value).content

        # 8.提取并构建输出数据结构
        outputs = {}
        if self.node_data.outputs:
            outputs[self.node_data.outputs[0].name] = content
        else:
            outputs["output"] = content

        # 9.构建响应状态并返回
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