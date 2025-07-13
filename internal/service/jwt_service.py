#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 01:02
#Author  :Emcikem
@File    :jwt_service.py
"""
import os
from typing import Any
import jwt

from injector import inject
from dataclasses import dataclass

@inject
@dataclass
class JWTService:
    """jwt服务"""

    @classmethod
    def generate_token(cls, paylod: dict[str, Any]) -> str:
        """根据传递的载荷消息生成token消息"""
        secret_key = os.getenv("JWT_SECRET_KEY")
        return jwt.encode(paylod, secret_key, algorithm="HS256")

    @classmethod
    def parse_token(cls, token: str) -> dict[str, Any]:
        """解析传入的token消息"""
        secret_key = os.getenv("JWT_SECRET_KEY")
        try:
            return jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise ValueError("授权认证凭证已过期请重新登录")
        except jwt.InvalidTokenError:
            raise ValueError("解析token出错，请重新登录")
        except Exception as e:
            raise e