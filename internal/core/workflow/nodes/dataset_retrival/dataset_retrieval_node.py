#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/11 22:25
#Author  :Emcikem
@File    :dataset_retrieval_node.py
"""
from typing import Optional, Any
from uuid import UUID

from flask import Flask
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from pydantic import PrivateAttr

from internal.core.workflow.entity.node_entity import NodeResult, NodeStatus
from internal.core.workflow.entity.variable_entity import VariableValueType, VariableDefaultVaultMap
from internal.core.workflow.entity.workflow_entity import WorkflowState
from internal.core.workflow.nodes import BaseNode
from internal.core.workflow.nodes.dataset_retrival.dataset_retrieval_entity import DatasetRetrievalNodeData


class DatasetRetrievalNode(BaseNode):
    """知识库检索节点"""
    node_data = DatasetRetrievalNodeData
    _retrieval_tool: BaseTool = PrivateAttr(None)

    def __init__(
            self,
            *args: Any,
            flask_app: Flask,
            account_id: UUID,
            **kwargs: Any
    ):
        """构造函数，完成知识库检索节点的初始化"""
        # 1.调用父类构造函数完成数据初始化
        super().__init__(*args, **kwargs)

        # 2.导入依赖注入及检索服务
        from app.http.module import injector
        from internal.service import RetrievalService

        retrieval_service = injector.get(RetrievalService)

        # 3.构建检索服务工具
        self._retrieval_tool = retrieval_service.create_langchain_tool_from_search(
            flask_app=flask_app,
            dataset_ids=self.node_data.dataset_ids,
            account_id=account_id,
            **self.node_data.retrieval_config.model_dump(),
        )

    def invoke(self, state: WorkflowState, config: Optional[RunnableConfig] = None) -> WorkflowState:
        """知识库检索节点调用函数，执行响应的知识库检索后返回"""
        # 1.提取检索query输入变量
        query_input = self.node_data.inputs[0]

        # 2.提取query输入变量关联的值
        inputs_dict = {}
        if query_input.value.type == VariableValueType.LITERAL:
            # 3.数据直接输入
            inputs_dict[query_input.name] = query_input.value.content
        else:
            # 4.引用数据，需要循环遍历当前节点之前的节点执行结果
            for node_result in state["node_results"]:
                if node_result.node_data.id == query_input.value.content.ref_node_id:
                    inputs_dict[query_input.name] = node_result.outputs.get(
                        query_input.value.content.ref_var_name,
                        VariableDefaultVaultMap.get(query_input.type)
                    )

        # 5.调用知识库检索工具
        combine_documents = self._retrieval_tool.invoke(inputs_dict)

        # 6.提取并构建输出数据结构
        outputs = {}
        if self.node_data.outputs:
            outputs[self.node_data.outputs[0].name] = combine_documents
        else:
            outputs["combine_documents"] = combine_documents

        # 7.返回响应状态
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

