#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/6 15:22
#Author  :Emcikem
@File    :api_tool_handler.py
"""
from uuid import UUID
from injector import inject
from dataclasses import dataclass
from internal.schema.api_tool_schema import (
    ValidateOpenAPISchemaReq,
    CreateApiToolReq,
    GetApiToolProviderResp,
)
from pkg.response import validate_error_json, success_message, success_json
from internal.service import ApiToolService


@inject
@dataclass
class ApiToolHandler:
    """自定义API插件处理器"""
    api_tool_service: ApiToolService

    def create_api_tool(self):
        """创建自定义API"""
        # 1.提取请求的数据并校验
        req = CreateApiToolReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建API工具
        self.api_tool_service.create_api_tool(req)

        return success_message("创建自定义API插件成功")

    def get_api_tool_provider(self, provider_id: UUID):
        """根据传递的provider_id获取工具提供者的原始信息"""
        api_tool_provider = self.api_tool_service.get_api_tool_provider(provider_id)

        resp = GetApiToolProviderResp()

        return success_json(resp.dump(api_tool_provider))

    def validate_openapi_schema(self):
        """校验传递的openapi_schema字符串是否正确"""
        # 1.提取前端的数据并校验
        req = ValidateOpenAPISchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务并解析传递的数据
        self.api_tool_service.parse_openapi_schema(req.openapi_schema)

        return success_message("数据校验成功")