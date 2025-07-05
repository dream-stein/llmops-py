#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/5 20:29
#Author  :Emcikem
@File    :builtin_tool_service.py
"""
from injector import inject
from dataclasses import dataclass

from pydantic import BaseModel

from internal.core.tools.builtin_tools.providers import BuiltinProviderManager

@inject
@dataclass
class BuiltinToolService:
    """内置工具服务"""
    builtin_provider_manager: BuiltinProviderManager

    def get_builtin_tools(self) -> list:
        """获取LLMOps项目中的所有内置提供商+工具对应的信息"""
        # 1.获取所有的提供商
        providers = self.builtin_provider_manager.get_providers()

        # 2.遍历所有的提供商并提取工具信息
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude={"icon"}),
                "tools": [],
            }
            # 3.循环遍历提取提供者的所有工具实体
            for tool_entity in provider.get_tool_entities():
                # 4.构建工具实体信息
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": []
                }
                # 5.从提供者中获取工具函数
                tool = provider.get_tool(tool_entity.name)

                # 6.检测下工具是否有args_schema这个属性，并且是BaseModel的子类
                if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
                    inputs = []
                    # todo: 啥意思
                    for field_name, model_field in tool.args_schema.__fields__.items():
                        inputs.append({
                            "name": field_name,
                            "description": model_field.field_info.description or "",
                            "required": model_field.required,
                            "type": model_field.outer_type_.__name__,
                        })
                    tool_dict["inputs"] = inputs
                builtin_tool["tools"].append(tool_dict)

            builtin_tools.append(builtin_tool)

        return builtin_tools

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """根据传递的提供者名字+工具名字获取指定工具信息"""
        pass