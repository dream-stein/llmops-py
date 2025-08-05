#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/29 21:40
#Author  :Emcikem
@File    :openapi_handler.py
"""
from flask_login import current_user
from injector import inject
from dataclasses import dataclass

from internal.schema.openapi_schema import OpenAPIChatReq
from pkg.response import validate_error_json, compact_generate_response
from internal.service.openapi_service import OpenAPIService

@inject
@dataclass
class OpenAPIHandler:
    """开发API处理器"""
    openapi_service: OpenAPIService

    def chat(self):
        """开发Chat对话接口"""
        # 1.提取请求并校验
        req = OpenAPIChatReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建会话
        resp = self.openapi_service.chat(req, current_user)

        return compact_generate_response(resp)