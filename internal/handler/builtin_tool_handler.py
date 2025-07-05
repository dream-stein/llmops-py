#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/5 20:10
#Author  :Emcikem
@File    :builtin_tool_handler.py
"""
from injector import inject
from dataclasses import dataclass



@inject
@dataclass
class BuiltinToolHandler:
    """内置工具处理器"""

    def get_builtin_tools(self):
        """获取LLMOps所有内置工具信息+提供商信息"""

        pass

    def get_provider_tool(self, provider: str, tool: str):
        """根据传递的提供商名字+工具名字获取指定工具的信息"""
        pass