# #!/usr/bin/eny python
# # -*- coding: utf-8 -*-
# """
# @Time    :2025/7/6 14:23
# #Author  :Emcikem
# @File    :api_tool.py
# """
import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, Text, DateTime, PrimaryKeyConstraint, JSON
)
from internal.extension.database_extension import db
#
class ApiToolProvider(db.Model):
    """API工具提供者模型"""
    __tablename__ = "api_tool_provider"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_provider_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    icon = Column(String(255), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    openapi_schema = Column(JSON, nullable=False, default="")
    headers = Column(JSON, nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def tools(self) -> list["ApiTool"]:
        return db.session.query(ApiTool).filter_by(provider_id=self.id).all()

class ApiTool(db.Model):
    """API工具表"""
    __tablename__ = "api_tool"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_api_tool_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    provider_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    url = Column(String(255), nullable=False, default="")
    method = Column(String(255), nullable=False, default="")
    parameters = Column(JSON, nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


    @property
    def provider(self) -> "ApiToolProvider":
        """只读属性，返回当前工具关联/归属的工具提供者信息"""
        return db.session.query(ApiToolProvider).get(self.provider_id)