#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 09:45
#Author  :Emcikem
@File    :middleware.py
"""
from typing import Optional
from flask import Request
from injector import inject
from dataclasses import dataclass

from internal.exception import UnauthorizedException
from internal.model import Account
from internal.service import JWTService, AccountService

@inject
@dataclass
class Middleware:
    """应用中间件，可以重写request_loader与unauthorized_handler"""
    jwt_service: JWTService
    account_service: AccountService

    def request_loader(self, request: Request) -> Optional[Request]:
        """登录管理器的请求加载器"""
        # 1.单独为llmops路由蓝图创建请求加载器
        # TODO: 改成 if request.blueprint == "llmops":
        if request.blueprint == "llmops":
            # 2.提取请求体headers中的信息
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise UnauthorizedException("该接口需要授权才能访问，请登录后尝试")

            # 3.请求信息中没用空格分隔符，则验证失败，Authorization：Bearer access_token
            if " " not in auth_header:
                raise UnauthorizedException("该接口需要授权才能访问，验证格式失败")

            # 4.分割授权信息，必须符合Bearer access_token
            auth_schema, access_token = auth_header.split(None, 1)
            if auth_schema.lower() != "bearer":
                raise UnauthorizedException("该接口需要授权才能访问，验证格式失败")

            # 5.解析token信息得到用户信息并返回
            payload = self.jwt_service.parse_token(access_token)
            account_id = payload.get("sub")
            return self.account_service.get_account(account_id)
        else:
            return None