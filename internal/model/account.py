#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 00:55
#Author  :Emcikem
@File    :account.py
"""
import uuid
from datetime import datetime

from flask import current_app
from sqlalchemy import (
    PrimaryKeyConstraint,
    Column,
    String,
    DateTime
)

from flask_login import UserMixin

from internal.entity.conversation_entity import InvokeFrom
from internal.extension.database_extension import db
from internal.model.conversation import Conversation


class Account(UserMixin, db.Model):
    """账号模型"""
    __tablename__ = "account"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_account_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    name = Column(String(255), nullable=False, default="")
    email = Column(String(255), nullable=False, default="")
    avatar = Column(String(255), nullable=False, default="")
    password = Column(String(255), nullable=True, default="")
    password_salt = Column(String(255), nullable=True, default="")
    assistant_agent_conversation_id = Column(String(36), nullable=True)
    last_login_at = Column(DateTime, nullable=False, default=datetime.now)
    last_login_ip = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def is_password_set(self) -> bool:
        """只读属性，获取当前账号密码是否设置"""
        return self.password is not None and self.password != ""

    @property
    def assistant_agent_conversation(self) -> "Conversation":
        """只读属性，返回当前账号的辅助Agent会话"""
        # 1.获取辅助Agent应用id
        assistant_agent_id = current_app.config.get("ASSISTANT_AGENT_ID")
        conversation = db.session.get(Conversation,
            self.assistant_agent_conversation_id
        ) if self.assistant_agent_conversation_id else None

        # 2.判断会话信息是否存在，如果不存在则创建一个空会话
        if not self.assistant_agent_conversation_id or not conversation:
            # 3.开启自动提交上下文
            with db.auto_commit():
                # 4.创建辅助Agent会话
                conversation = Conversation(
                    app_id=assistant_agent_id,
                    name="New Conversation",
                    invoke_from=InvokeFrom.ASSISTANT_AGENT,
                    created_by=self.id,
                )
                db.session.add(conversation)
                db.session.flush()

                # 5.更新当前账号的辅助Agent会话id
                self.assistant_agent_conversation_id = conversation.id

        return conversation

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