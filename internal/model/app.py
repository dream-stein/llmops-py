#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/10 21:37
#Author  :Emcikem
@File    :app.py
"""
from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index, JSON, Integer,
)

from internal.entity.app_entity import AppConfigType, DEFAULT_APP_CONFIG
from internal.extension.database_extension import db

class App(db.Model):
    """AI应用基础模型类"""
    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_id"),
        Index("idx_app_account_id", "account_id"),
    )

    id = Column(String(36), default=uuid.uuid4, nullable=False)
    account_id = Column(String(36), nullable=False) # 创建账号id
    app_config_id = Column(String(36), nullable=True) # 发布配置id，当值为空时代表没用发布
    draft_app_config_id = Column(String(36), nullable=True) # 关联的草稿配置id
    debug_conversation_id = Column(String(36), nullable=True) # 应用调试会话id，为None则代表没用会话信息
    name = Column(String(255), default="", nullable=False)
    icon = Column(String(255), default="", nullable=False)
    description = Column(Text, default="", nullable=False)
    status = Column(String(255), default="", nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def app_config(self) -> "AppConfig":
        """只读属性，返回当前应用的运行配置"""
        if not self.app_config_id:
            return None
        return db.session.get(AppConfig, self.app_config_id)

    @property
    def draft_app_config(self) -> "AppConfigVersion":
        """只读属性，返回当前应用的草稿配置"""
        # 1.获取当前应用的草稿配置
        app_config_version = db.session.query(AppConfigVersion).filter(
            AppConfigVersion.app_id == self.id,
            AppConfigVersion.config_type == AppConfigType.DRAFT,
        ).one_or_none()

        # 2..检测配置是否存在，如果不在则创建一个默认值
        if not app_config_version:
            app_config_version = AppConfigVersion(
                app_id=self.id,
                version=0,
                config_type=AppConfigType.DRAFT,
                **DEFAULT_APP_CONFIG
            )
            db.session.add(app_config_version)
            db.session.commit()

        return app_config_version

class AppConfig(db.Model):
    """应用配置模型"""
    __tablename__ = "app_config"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_config_id"),
    )

    id = Column(String(36), default=uuid.uuid4, nullable=False) # 配置id
    app_id = Column(String(36), nullable=False) # 关联应用id
    model_config = Column(JSON, nullable=False, default="{}") # 模型配置
    dialog_round = Column(Integer, nullable=False, default=0) # 携带上下文轮数
    preset_prompt = Column(Text, nullable=False, default="") # 预设prompt
    tools = Column(JSON, nullable=False, default="[]") # 应用关联的工具列表
    workflows = Column(JSON, nullable=False, default="[]") # 应用管理的工作流列表
    retrieval_config = Column(JSON, nullable=False, default="[]") # 检索配置
    long_term_memory = Column(JSON, nullable=False, default="{}") # 长期记忆配置
    opening_statement = Column(Text, nullable=False, default="") # 开场白文案
    opening_questions = Column(JSON, nullable=False, default="[]") # 开场白问题建议列表
    speech_to_text = Column(JSON, nullable=False, default="{}") # 语音转文本配置
    text_to_speech = Column(JSON, nullable=False, default="{}") # 文本转语音配置
    suggested_after_answer = Column(JSON, nullable=False, default="{}")
    review_config = Column(JSON, nullable=False, default="{}") # 审核配置
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

class AppConfigVersion(db.Model):
    """应用配置版本历史表，用于存储草稿配置+历史发布配置"""
    __tablename__ = "app_config_version"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_config_version_id"),
    )

    id = Column(String(36), default=uuid.uuid4, nullable=False)
    app_id = Column(String(36), nullable=False)
    model_config = Column(JSON, nullable=False, default="{}")
    dialog_round = Column(Integer, nullable=False, default=0)
    preset_prompt = Column(Text, nullable=False, default="")
    tools = Column(JSON, nullable=False, default="[]")
    workflows = Column(JSON, nullable=False, default="[]")
    datasets = Column(JSON, nullable=False, default="[]")
    retrieval_config = Column(JSON, nullable=False, default="[]")
    long_term_memory = Column(JSON, nullable=False, default="{}")
    opening_statement = Column(Text, nullable=False, default="")
    opening_questions = Column(JSON, nullable=False, default="[]")
    speech_to_text = Column(JSON, nullable=False, default="{}")
    text_to_speech = Column(JSON, nullable=False, default="{}")
    suggested_after_answer = Column(JSON, nullable=False, default="{}")
    review_config = Column(JSON, nullable=False, default="{}")
    version = Column(Integer, nullable=False, default=0)
    config_type = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)


class AppDatasetJoin(db.Model):
    """应用知识库关联表模型"""
    __tablename__ = "app_dataset_join"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_dataset_join_id"),
    )
    id = Column(String(36), default=uuid.uuid4, nullable=False)
    app_id = Column(String(36), nullable=False)
    dataset_id = Column(String(36), nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)