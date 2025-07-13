#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 23:28
#Author  :Emcikem
@File    :api_key_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField
from marshmallow import Schema, fields, pre_dump
from wtforms.validators import Length
# from internal.lib.helper import datetime_to_timestamp
from internal.model import ApiKey

class CreateApiKeyReq(FlaskForm):
    """创建API秘钥请求"""
    is_active = BooleanField("is_active")
    remark = StringField("remark", validators=[
        Length(max=100, message="秘钥备注不能超过100个字符")
    ])

class UpdateApiKeyReq(FlaskForm):
    """更新API秘钥请求"""
    is_active = BooleanField("is_active")
    remark = StringField("remark", validators=[
        Length(max=100, message="秘钥备注不能超过100个字符")
    ])

class UpdateApiKeyIsActiveReq(FlaskForm):
    """更新API秘钥激活请求"""
    is_active = BooleanField("is_active")

class GetApiKeysWithPageResp(Schema):
    """获取API秘钥分页列表数据"""
    id = fields.UUID(dump_default="")
    api_key = fields.String(dump_default="")
    is_active = fields.Boolean(dump_default=False)
    remark = fields.String(dump_default="")
    updated_at = fields.Integer(dump_default=0)
    created_at = fields.Integer(dump_default=0)

    @pre_dump
    def process_page(self, data: ApiKey, **kwargs):
        return {
            "id": data.id,
            "api_key": data.api_key,
            "is_active": data.is_active,
            "remark": data.remark,
            "updated_at": int(data.updated_at.timestamp()),
            "created_at": int(data.created_at.timestamp()),
        }