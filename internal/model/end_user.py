#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/28 22:40
#Author  :Emcikem
@File    :end_user.py
"""
import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import PrimaryKeyConstraint, Column, String, Boolean, DateTime

from internal.extension.database_extension import db


class EndUser(db.Model):
    """终端用户表模型"""
    __tablename__ = 'end_user'
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_end_user_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    tenant_id = Column(String(36), nullable=False)
    app_id = Column(String(36), nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)