#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/5 20:29
#Author  :Emcikem
@File    :builtin_tool_service.py
"""
from injector import inject
from dataclasses import dataclass
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
            for tool_entity in provider.get_tool_entities():
                tool_dict = {
                    **tool_entity.model_dump(),
                    "inputs": []
                }
        # 3.除了工具实体，还需要提取工具的inputs代表大语言模型的输入参数信息
        # 4.组装提取所有的信息为list，并返回

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        """根据传递的提供者名字+工具名字获取指定工具信息"""
        pass