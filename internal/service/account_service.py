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

from internal.model import Account
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