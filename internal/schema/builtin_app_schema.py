#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/28 00:20
#Author  :Emcikem
@File    :builtin_app_schema.py
"""
from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from wtforms import StringField
from wtforms.validators import DataRequired, UUID

from internal.core.builtin_apps.entities.builtin_app_entity import BuiltinAppEntity
from internal.core.builtin_apps.entities.category_entity import CategoryEntity

class GetBuiltinAppCategoriesResp(Schema):
    """获取内置应用分类列表响应"""
    category = fields.String(dump_default="")
    name = fields.String(dump_default="")

    @pre_dump
    def process_data(self, data: CategoryEntity, **kwargs):
        return data.model_dump()

class GetBuiltinAppsResp(Schema):
    """获取内置应用实体列表响应"""
    id = fields.String(dump_default="")
    category = fields.String(dump_default="")
    name = fields.String(dump_default="")
    icon = fields.String(dump_default="")
    description = fields.String(dump_default="")
    model_config = fields.Dict(dump_default={})
    created_at = fields.Integer(dump_default=0)

    @pre_dump
    def process_data(self, data: BuiltinAppEntity, **kwargs):
        return {
            #todo:这个什么写法
            **data.model_dump(include={"id", "category", "name", "icon", "description", "created_at"}),
            "model_config": {
                "provider": data.language_model_config.get("provider", ""),
                "model": data.language_model_config.get("model", ""),
            }
        }