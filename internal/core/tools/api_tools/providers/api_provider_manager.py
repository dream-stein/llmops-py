#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/9 00:12
#Author  :Emcikem
@File    :api_provider_manager.py
"""
from typing import Type, Optional

from injector import inject
from dataclasses import dataclass
from pydantic import BaseModel, create_model, Field
from langchain_core.tools import BaseTool, StructuredTool
from internal.core.tools.api_tools.entities import ToolEntity, ParameterTypeMap


@inject
@dataclass()
class ApiProviderManager(BaseModel):
    """API根据提供者管理器，能根据传递的工具配置信息生成自定义langchain工具"""

    def _create_model_from_parameters(self, parameters: list[dict]) -> Type[BaseModel]:
        """工具传递的parameter参数创建BaseModel子类"""
        fields = {}
        for parameter in parameters:
            field_name = parameter.get("name")
            field_type = ParameterTypeMap.get(parameter.get("type"), str)
            field_required = parameter.get("required")
            field_description = parameter.get("description", "")

            fields[field_name] = {
                field_type if field_required else Optional[field_type],
                Field(description=field_description),
            }
        return create_model("DynamicModel", )

    def get_tool(self, tool_entity: ToolEntity) -> BaseTool:
        """根据传递的配置获取自定义API工具"""
        return StructuredTool.from_function(
            func=None,
            name=f"{tool_entity.id}_{tool_entity.name}",
            description=tool_entity.description,
            args_schema=None,
        )
