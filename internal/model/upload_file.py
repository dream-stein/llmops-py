#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/11 00:42
#Author  :Emcikem
@File    :upload_file.py
"""
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, DateTime, PrimaryKeyConstraint, text, JSON, Integer
)
from internal.extension.database_extension import db


class UploadFile(db.Model):
    """上传文件模型"""
    __tablename__ = "upload_file"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_upload_file_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    key = Column(String(255), nullable=False, default="")
    size = Column(Integer, nullable=False, default=0)
    extension = Column(String(255), nullable=False, default="")
    mime_type = Column(String(255), nullable=False, default="")
    hash = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
