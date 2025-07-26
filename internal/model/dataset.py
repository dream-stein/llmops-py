#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 14:17
#Author  :Emcikem
@File    :dataset.py
"""
from datetime import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    JSON, Integer, Boolean,
    func
)
from internal.extension.database_extension import db
from . import UploadFile
from .app import AppDatasetJoin

class Dataset(db.Model):
    """知识库"""
    __tablename__ = "dataset"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_dataset_id"),
    )

    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    name = Column(String(255), nullable=False, default="")
    icon = Column(String(255), nullable=False, default="")
    description = Column(Text, nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def document_count(self) -> int:
        """只读属性，获取知识库下的文档数"""
        return (
            db.session.query(func.count(Document.id))
            .filter(Document.dataset_id == self.id)
            .scalar()
        )

    @property
    def hit_count(self) -> int:
        """只读属性，获取该知识库的命中次数"""
        return (
            db.session.query(func.coalesce(func.sum(Segment.hit_count), 0))
            .filter(Segment.dataset_id == self.id)
            .scalar()
        )

    @property
    def character_count(self) -> int:
        """只读属性，获取该知识库下的字符总数"""
        return (
            db.session.query(func.coalesce(func.sum(Document.character_count), 0))
            .filter(Document.dataset_id == self.id)
            .scalar()
        )

    @property
    def related_app_count(self) -> int:
        """只读属性，获取该知识库关联的应用数"""
        return (
            db.session.query(func.count(AppDatasetJoin.id))
            .filter(AppDatasetJoin.dataset_id == self.id)
            .scalar()
        )

class Document(db.Model):
    """文档表模型"""
    __tablename__ = "document"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_document_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    dataset_id = Column(String(36), nullable=False)
    upload_file_id = Column(String(36), nullable=False)
    process_rule_id = Column(String(36), nullable=False)
    batch = Column(String(255), nullable=False, default="")
    name = Column(String(255), nullable=False, default="")
    position = Column(String(255), nullable=False, default="")
    character_count = Column(Integer, nullable=False, default=0)
    token_count = Column(Integer, nullable=False, default=0)
    processing_started_at = Column(DateTime, nullable=True)
    parsing_completed_at = Column(DateTime, nullable=True)
    splitting_completed_at = Column(DateTime, nullable=True)
    indexing_completed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    stopped_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=False, default="")
    enabled = Column(Boolean, nullable=False, default=False)
    disabled_at = Column(DateTime, nullable=True)
    status = Column(String(255), nullable=False, default="waitting")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def upload_file(self) -> "UploadFile":
        return db.session.query(UploadFile).filter(
            UploadFile.id == self.upload_file_id,
        ).one_or_none()

    @property
    def process_rule(self) -> "ProcessRule":
        return db.session.query(ProcessRule).filter(
            ProcessRule.id == self.process_rule_id,
        ).one_or_none()

    @property
    def segment_count(self) -> int:
        return db.session.query(func.count(Segment.id)).filter(
            Segment.document_id == self.id,
        ).scalar()

    @property
    def hit_count(self) -> int:
        return db.session.query(func.coalesce(func.sum(Segment.hit_count), 0)).filter(
            Segment.document_id == self.id,
        ).scalar()

class Segment(db.Model):
    """片段表模型"""
    __tablename__ = "segment"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_segment_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    dataset_id = Column(String(36), nullable=False)
    document_id = Column(String(36), nullable=False)
    node_id = Column(String(36), nullable=False)
    position = Column(Integer, nullable=False, default=1)
    content = Column(Text, nullable=False, default="")
    character_count = Column(Integer, nullable=False, default=0)
    token_count = Column(Integer, nullable=False, default=0)
    keywords = Column(JSON, nullable=False, default={})
    hash = Column(String(255), nullable=False, default="")
    hit_count = Column(Integer, nullable=False, default=0)
    enabled = Column(Boolean, nullable=False, default=False)
    disabled_at = Column(DateTime, nullable=True)
    processing_started_at = Column(DateTime, nullable=True)
    indexing_completed_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    stopped_at = Column(DateTime, nullable=True)
    error = Column(Text, nullable=False, default="")
    status = Column(String(255), nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    @property
    def document(self) -> "Document":
        return db.session.query(Document).get(self.document_id)

class KeywordTable(db.Model):
    """"关键词表模型"""
    __tablename__ = "keyword_table"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_keyword_table_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)
    dataset_id = Column(String(36), nullable=False)
    keyword_table = Column(JSON, nullable=False, default={})
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

class DatasetQuery(db.Model):
    """知识库查询"""
    __tablename__ = "dataset_query"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_dataset_query_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)
    dataset_id = Column(String(36), nullable=False)
    query = Column(Text, nullable=False, default="")
    status = Column(String(255), nullable=False, default="HitTesting")
    source_app_id = Column(String(36), nullable=True)
    created_by = Column(String(36), nullable=True)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

class ProcessRule(db.Model):
    """文档处理规则表模型"""
    __tablename__ = "process_rule"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_process_rule_id"),
    )
    id = Column(String(36), nullable=False, default=uuid.uuid4)
    account_id = Column(String(36), nullable=False)
    dataset_id = Column(String(36), nullable=False)
    mode = Column(String(255), nullable=False, default="automic")
    rule = Column(JSON, nullable=False, default="")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)