#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 00:04
#Author  :Emcikem
@File    :api_key_service.py
"""
import uuid
import secrets
from injector import inject
from dataclasses import dataclass
from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from ..schema.api_key_schema import CreateApiKeyReq


@inject
@dataclass
class ApiKeyService(BaseService):
    """API秘钥服务"""
    db: SQLAlchemy

    # def create_api_key(self, req: CreateApiKeyReq, account: ):

    @classmethod
    def generate_api_key(cls, api_key_prefix: str = "llmops-v1/") -> str:
        """生成一个长度为48的API秘钥，并携带前缀"""
        return api_key_prefix + secrets.token_urlsafe(48)