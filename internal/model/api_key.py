#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 23:01
#Author  :Emcikem
@File    :api_key.py
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    PrimaryKeyConstraint,
    Column,
    String,
    Boolean,
    DateTime
)

from internal.extension.database_extension import db


class ApiKey(db.Model):
    __tablename__ = 'api_key'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='api_key_pk'),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    api_key = Column(String(255), nullable=False, default="")
    is_active = Column(Boolean, nullable=False, default=False)
    remark = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
