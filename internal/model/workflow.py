#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/28 23:40
#Author  :Emcikem
@File    :workflow.py
"""
import uuid
from datetime import datetime

from sqlalchemy import PrimaryKeyConstraint, Index, Column, String, Integer, DateTime, Text, JSON, Boolean, Float

from internal.extension.database_extension import db


class Workflow(db.Model):
    """工作流模型"""
    __tablename__ = 'workflow'
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_workflow_id"),
        Index("workflow_account_id_idx", "account_id"),
        Index("workflow_tool_call_name_idx", "tool_call_name"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    tool_call_name = Column(String(255), nullable=False, default="")
    icon = Column(String(255), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    graph = Column(JSON, nullable=False, default={})
    draft_graph = Column(JSON, nullable=False, default={})
    is_debug_passed = Column(Boolean, nullable=False, default=False)
    status = Column(String(255), nullable=False, default="")
    published_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

class WorkflowResult(db.Model):
    """工作流存储结果模型"""
    __tablename__ = 'workflow_result'
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_workflow_result_id"),
        Index("workflow_result_app_id_idx", "app_id"),
        Index("workflow_result_account_id_idx", "account_id"),
        Index("workflow_result_workflow_id_idx", "workflow_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    app_id = Column(String(36), nullable=True)
    account_id = Column(String(36), nullable=False)
    workflow_id = Column(String(36), nullable=False)
    graph = Column(JSON, nullable=False, default={})
    state = Column(JSON, nullable=False, default={})  # 工作流最终状态
    latency = Column(Float, nullable=False, default=0.0)
    status = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

