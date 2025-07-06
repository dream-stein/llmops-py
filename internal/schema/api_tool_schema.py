#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/6 15:33
#Author  :Emcikem
@File    :api_tool_schema.py
"""
from marshmallow import Schema, fields, pre_dump
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from .schema import ListField
from internal.model import ApiToolProvider


class ValidateOpenAPISchemaReq(FlaskForm):
    """校验OpenAPI规范字符串请求"""
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])

class CreateApiToolReq(FlaskForm):
    """创建自定义API工具请求"""
    name = StringField("name", validators=[
        DataRequired(message="工具提供者名字不能为空"),
        Length(min=1, max=30, message="工具提供者的名字长度在1-30"),
    ])
    icon = StringField("icon", validators=[
        DataRequired(message="根据提供者的图标不能为空"),
        URL(message="工具提供者的图标必须是URL链接"),
    ])
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空"),
    ])
    headers = ListField("headers")

    @classmethod
    def validate_headers(cls, form, field):
        """校验headers的请求的数据是否正确，涵盖列表校验，列表元素校验"""
        for header in field.data:
            if not isinstance(header, dict):
                raise ValidationError("headers里的每一个元素都必须是字典")
            if set(header.keys()) != {"key", "value"}:
                raise ValidationError("headers里的每一个元素都必须包含key/value两个熟悉，不允许有其他元素")

class GetApiToolProviderResp(Schema):
    """获取API工具提供者响应信息"""
    id = fields.UUID()
    name = fields.String()
    icon = fields.String()
    openapi_schema = fields.String()
    headers = fields.List(fields.Dict, default=[])
    created_at = fields.Integer(default=0)

    @pre_dump
    def process_data(self, data: ApiToolProvider, **kwargs):
        return {
            "id": data.id,
            "name": data.name,
            "icon": data.icon,
            "openapi_schema": data.openapi_schema,
            "headers": data.headers,
            "created_at": int(data.created_at.timestamp()),
        }

