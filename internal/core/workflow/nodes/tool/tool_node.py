#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/11 23:57
#Author  :Emcikem
@File    :tool_node.py
"""
import json
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig
from langchain_core.runnables.utils import Input, Output

from langchain_core.tools import BaseTool
from pydantic import PrivateAttr
from unstructured_client.models.shared import WorkflowNode

from internal.core.tools.api_tools.entities import ToolEntity
from internal.core.workflow.entity.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entity.variable_entity import VariableValueType, VariableDefaultVaultMap
from internal.core.workflow.entity.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.tool.tool_entity import ToolNodeData
from internal.exception import NotFoundException, FailException
from internal.model import ApiTool


class ToolNode(BaseNode):
    """扩展插件节点"""
    node_data: ToolNodeData
    _tool: BaseTool = PrivateAttr(None)

    def __init__(self, *args: Any, **kwargs: Any):
        """构造函数，完成对内置工具的初始化"""
        # 1.调用父类构造函数完成数据初始化
        super().__init__(*args, **kwargs)

        # 2.导入依赖注入及工具提供者
        from app.http.module import injector

        # 3.判断是内置插件还是API插件，执行不太的操作
        if self.node_data.tool_type == "builtin_tool":
            from internal.core.tools.builtin_tools.providers import BuiltinProviderManager
            builtin_provider_manager = injector.get(BuiltinProviderManager)

            # 4.调用内置提供者获取内置插件
            _tool = builtin_provider_manager.get_tool(self.node_data.provider_id, self.node_data.tool_id)
            if not _tool:
                raise NotFoundException("该内置插件扩展不存在，请核实后重试")

            self._tool = _tool(**self.node_data.params)
        else:
            # 5.API插件，调用数据库查询记录并创建API插件
            from pkg.sqlalchemy import SQLAlchemy
            db = injector.get(SQLAlchemy)

            # 6.提供传递的提供者名字+工具名字查询工具
            api_tool = db.session.query(ApiTool).filter(
                ApiTool.provider_id == self.node_data.provider_id,
                ApiTool.name == self.node_data.tool_id
            ).one_or_none()
            if not api_tool:
                raise NotFoundException("该API扩展插件不存在，请核实重试")

            # 7.导入API插件提供者
            from internal.core.tools.api_tools.providers import ApiProviderManager
            api_provider_manager = injector.get(ApiProviderManager)

            # 8.创建API工具提供者并赋值
            self._tool = api_provider_manager.get_tool(ToolEntity(
                id=str(api_tool.id),
                name=api_tool.name,
                url=api_tool.url,
                method=api_tool.method,
                description=api_tool.description,
                headers=api_tool.headers,
                parameters=api_tool.parameters,
            ))

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """扩展插件执行节点，根据传递的信息调用预设的插件，涵盖内置插件及API插件"""
        # 1.提取节点中的输入数据
        inputs = self.node_data.inputs

        # 2.循环遍历输入数据，并提取需要的数据
        inputs_dict = {}
        for input in inputs:
            # 3.判断数据是引用还是直接输入
            if input.value.type == VariableValueType.LITERAL:
                inputs_dict[input.name] = input.value.content
            else:
                # 4.引用的数据类型，遍历节点获取数据
                for node_result in state["node_results"]:
                    if node_result.node_data.id == input.value.content.ref_node_id:
                        inputs_dict[input.name] = node_result.outputs.get(
                            input.value.content.ref_var_name,
                            VariableDefaultVaultMap.get(input.type)
                        )

        # 5.调用插件并获取结果
        try:
            result = self._tool.invoke(inputs_dict)
        except Exception as e:
            raise FailException("扩展插件执行失败，请稍后尝试")

        # 6.检测result是否为字符串，如果不是则转换
        if not isinstance(result, str):
            result = json.dumps(result)

        # 7.提取并构建输出数据结构
        outputs = {}
        if self.node_data.outputs:
            outputs[self.node_data.outputs[0].name] = result
        else:
            outputs["text"] = result

        # 8.构建响应状态并返回
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

