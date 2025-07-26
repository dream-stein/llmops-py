#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 00:55
#Author  :Emcikem
@File    :account.py
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    PrimaryKeyConstraint,
    Column,
    String,
    DateTime
)

from flask_login import UserMixin
from internal.extension.database_extension import db

class Account(UserMixin, db.Model):
    """账号模型"""
    __tablename__ = "account"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_account_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    api_key = Column(String(255), nullable=False, default="")
    email = Column(String(255), nullable=False, default="")
    avatar = Column(String(255), nullable=False, default="")
    password = Column(String(255), nullable=True, default="")
    password_salt = Column(String(255), nullable=True, default="")
    last_login_at = Column(DateTime, nullable=False, default=datetime.now)
    last_login_ip = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def is_password_set(self) -> bool:
        """只读属性，获取当前账号密码是否设置"""
        return self.password is not None and self.password != ""

class AccountOAuth(db.Model):
    """账号与第三放授权认证记录表"""
    __tablename__ = "account_oauth"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_account_oauth_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False, default="")
    provider = Column(String(36), nullable=False, default="")
    openid = Column(String(255), nullable=False, default="")
    encrypted_token = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)