#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/19 12:39
#Author  :Emcikem
@File    :segment_schema.py
"""
from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from pydantic_core import ValidationError
from wtforms.fields.simple import StringField, BooleanField
from wtforms.validators import Optional

from internal.lib.helper import datetime_to_timestamp
from internal.model import Segment
from pkg.paginator import PaginatorReq

class GetSegmentsWithPageReq(PaginatorReq):
    """获取文档片段列表请求"""
    search_word = StringField("search_word", default="", validators=[
        Optional(),
    ])

class GetSegmentsWithPageResp(Schema):
    """获取文档片段列表相应结构"""
    id = fields.UUID(dump_default="")
    document_id = fields.UUID(dump_default="")
    dataset_id = fields.UUID(dump_default="")
    position = fields.Integer(dump_default=0)
    content = fields.String(dump_default="")
    keywords = fields.List(fields.String, dump_default=[])
    character_count = fields.Integer(dump_default=0)
    token_count = fields.Integer(dump_default=0)
    hit_count = fields.Integer(dump_default=0)
    enabled = fields.Boolean(dump_default=True)
    disabled_at = fields.Integer(dump_default=0)
    status = fields.String(dump_default="")
    error = fields.String(dump_default="")
    updated_at = fields.Integer(dump_default=0)
    created_at = fields.Integer(dump_default=0)

    @pre_dump
    def process_data(self, data: Segment, **kwargs):
        return {
            "id": data.id,
            "document_id": data.document_id,
            "dataset_id": data.dataset_id,
            "position": data.position,
            "content": data.content,
            "keywords": data.keywords,
            "character_count": data.character_count,
            "token_count": data.token_count,
            "hit_count": data.hit_count,
            "enabled": data.enabled,
            "disabled_at": datetime_to_timestamp(data.disabled_at),
            "status": data.status,
            "error": data.error,
            "updated_at": datetime_to_timestamp(data.updated_at),
            "created_at": datetime_to_timestamp(data.created_at),
        }

class GetSegmentResp(Schema):
    """获取文档片段详情相应结构"""
    id = fields.UUID(dump_default="")
    document_id = fields.UUID(dump_default="")
    dataset_id = fields.UUID(dump_default="")
    position = fields.Integer(dump_default=0)
    content = fields.String(dump_default="")
    keywords = fields.List(fields.String, dump_default=[])
    character_count = fields.Integer(dump_default=0)
    token_count = fields.Integer(dump_default=0)
    hit_count = fields.Integer(dump_default=0)
    hash = fields.String(dump_default="")
    enabled = fields.Boolean(dump_default=True)
    disabled_at = fields.Integer(dump_default=0)
    status = fields.String(dump_default="")
    error = fields.String(dump_default="")
    updated_at = fields.Integer(dump_default=0)
    created_at = fields.Integer(dump_default=0)

    @pre_dump
    def process_data(self, data: Segment, **kwargs):
        return {
            "id": data.id,
            "document_id": data.document_id,
            "dataset_id": data.dataset_id,
            "position": data.position,
            "content": data.content,
            "keywords": data.keywords,
            "character_count": data.character_count,
            "token_count": data.token_count,
            "hit_count": data.hit_count,
            "hash": data.hash,
            "enabled": data.enabled,
            "disabled_at": datetime_to_timestamp(data.disabled_at),
            "status": data.status,
            "error": data.error,
            "updated_at": datetime_to_timestamp(data.updated_at),
            "created_at": datetime_to_timestamp(data.created_at),
        }

class UpdateSegmentEnabledReq(FlaskForm):
    """更新文档片段启用状态请求"""
    enabled = BooleanField("enabled")

    def validate_enabled(self, field: BooleanField) -> None:
        """校验文档启用姿态enabled"""
        if not isinstance(field.data, bool):
            raise ValidationError("enabled状态不能为空且必须为布尔值")