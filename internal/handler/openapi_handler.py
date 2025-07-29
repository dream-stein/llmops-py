#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/29 21:40
#Author  :Emcikem
@File    :openapi_handler.py
"""
from injector import inject
from dataclasses import dataclass

from pkg.response import success_message


@inject
@dataclass
class OpenAPIHandler:
    """开发API处理器"""

    def chat(self):
        """开发Chat对话接口"""
        return success_message("开放Chat对话接口")