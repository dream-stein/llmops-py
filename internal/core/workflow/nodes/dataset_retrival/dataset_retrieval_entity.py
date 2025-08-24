#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/11 21:55
#Author  :Emcikem
@File    :dataset_retrieval_entity.py
"""
from uuid import UUID

from internal.core.workflow.entities.node_entity import BaseNodeData
from pydantic import BaseModel, Field, model_validator

from internal.core.workflow.entities.variable_entity import VariableEntity, VariableType, VariableValueType
from internal.entity.dataset_entity import RetrievalStrategy
from internal.exception import FailException


class RetrievalConfig(BaseModel):
    """检索配置"""
    retrieval_strategy: RetrievalStrategy = RetrievalStrategy.SEMANTIC # 检索策略
    k: int = 4 # 最大召回数量
    score: float = 0 # 得分阈值


class DatasetRetrievalNodeData(BaseNodeData):
    """知识库检索节点数据"""
    dataset_ids: list[UUID] # 关联的知识库id列表
    retrieval_config: RetrievalConfig = RetrievalConfig() # 检索配置
    inputs: list[VariableEntity] = Field(default_factory=list) # 输入变量信息
    outputs: list[VariableEntity] = Field(
        exclude=True,
        default_factory=lambda: [
            VariableEntity(name="combine_documents", value={"type": VariableValueType.GENERATED})
        ]
    )

    @classmethod
    @model_validator(mode="before")
    def validate_inputs(cls, values):
        """校验输入变量信息"""
        # 1.提取inputs对应的信息
        inputs = values.get("inputs", [])

        # 2.判断是否只有一个输入变量，如果有多个则抛出错误
        if len(inputs) != 1:
            raise FailException("知识库节点输入变量信息出错")

        # 3.判断输入遍历的类型及字段名名称是否出错
        query_input: VariableEntity = inputs[0]
        if query_input.name != "query" or query_input.type != VariableType.STRING or query_input.required is False:
            raise FailException("知识库节点输入变量名字/变量类型/必填属性出错")

        return values