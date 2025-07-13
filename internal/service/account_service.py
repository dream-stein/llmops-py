#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 10:16
#Author  :Emcikem
@File    :account_service.py
"""
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from internal.model import Account, AccountOAuth
from internal.service import BaseService
from pkg.sqlalchemy import SQLAlchemy


@inject
@dataclass
class AccountService(BaseService):
    """账号服务"""
    db: SQLAlchemy

    def get_account(self, account_id: UUID) -> Account:
        """根据id获取指定的账号模型"""
        return self.get(Account, account_id)

    def get_account_oauth_by_provider_name_and_openid(
            self,
            provider_name: str,
            openid: str
    ) -> AccountOAuth:
        """根据传递的提供者名字+openai获取第三方授权认证记录"""
        return self.db.session.query(AccountOAuth).filter(
            AccountOAuth.provider == provider_name,
            AccountOAuth.openid == openid
        ).one_or_none()

    def get_account_by_email(self, email: str) -> Account:
        """根据传递的邮箱查询账号信息"""
        return self.db.session.query(Account).filter(
            Account.email == email
        ).one_or_none()

    def create_account(self, **kwargs) -> Account:
        """根据传递的键值对创建账号信息"""
        return self.create(Account, **kwargs)