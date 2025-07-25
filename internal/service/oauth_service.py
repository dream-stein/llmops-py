#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 13:09
#Author  :Emcikem
@File    :oauth_service.py
"""
import os
from datetime import datetime, timedelta
from typing import Any
from uuid import UUID

from injector import inject
from dataclasses import dataclass
from flask import request
from internal.service import BaseService
from pkg.oauth import OAuth, GithubOAuth
from pkg.sqlalchemy import SQLAlchemy

from internal.exception import NotFoundException
from .account_service import AccountService
from internal.model import AccountOAuth
from internal.service import JWTService

@inject
@dataclass
class OAuthService(BaseService):
    """第三方授权认证服务"""
    db: SQLAlchemy
    jwt_service: JWTService
    account_service: AccountService

    @classmethod
    def get_all_oauth(cls) -> dict[str, OAuth]:
        """获取LLMOps集成的第三方授权认证"""
        # 1.实例化集成的第三方授权认证OAuth
        github = GithubOAuth(
            client_id=os.getenv("GITHUB_CLIENT_ID"),
            client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
            redirect_uri=os.getenv("GITHUB_REDIRECT_URI"),
        )

        # 2.构建字典并返回
        return {
            "github": github,
        }

    def get_oauth_by_provider_name(self, provider_name: str) -> OAuth:
        """根据传递的访问提供商名字获取授权服务"""
        all_oauth = self.get_all_oauth()
        oauth = all_oauth.get(provider_name)

        if oauth is None:
            raise NotFoundException(f"该授权方式[{provider_name}]不存在")
        return oauth

    def oauth_login(self, provider_name: str, code: str) -> dict[str, Any]:
        """第三方OAuth授权认证登录，返回授权凭证以及过期时间"""
        # 1.根据传递的provider_name获取oauth
        oauth = self.get_oauth_by_provider_name(provider_name)

        # 2.根据code从第三方登录服务器中获取access_token
        oauth_access_token = oauth.get_access_token(code)

        # 3.根据获取到的token提取user_info信息
        oauth_user_info = oauth.get_user_info(oauth_access_token)

        # 4.根据provider_name+openid获取授权记录
        account_oauth = self.account_service.get_account_oauth_by_provider_name_and_openid(
            provider_name,
            oauth_user_info.id
        )
        if not account_oauth:
            # 5.该授权认证方式是第一次登录，查询邮箱是否存在
            account = self.account_service.get_account_by_email(oauth_user_info.email)
            if not account:
                # 6.账号不存在，注册账号
                account = self.account_service.create_account(
                    name=oauth_user_info.name,
                    email=oauth_user_info.email,
                )
            # 7.添加授权认证记录
            account_oauth = self.create(
                AccountOAuth,
                account_id=account.id,
                proivder=provider_name,
                openid=oauth_user_info.id,
                encryted_token=oauth_access_token,
            )
        else:
            # 8.查找账号信息
            account = self.account_service.get_account(UUID(account_oauth.account_id))

        # 9.更新账号信息，涵盖最后一次登录时间，以及ip地址
        self.update(
            account,
            last_login_at=datetime.now(),
            last_login_ip=request.remote_addr,
        )
        self.update(
            account_oauth,
            encryted_token=oauth_access_token,
        )

        # 10.生成授权凭证信息
        expire_at = int((datetime.now() + timedelta(days=30)).timestamp())
        payload = {
            "sub": str(account.id),
            "iss": "llmops",
            "exp": expire_at,
        }
        access_token = self.jwt_service.generate_token(payload)

        return {
            "expires_at": expire_at,
            "access_token": access_token,
        }