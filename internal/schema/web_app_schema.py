#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/3 23:36
#Author  :Emcikem
@File    :web_app_schema.py
"""

from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from wtforms import StringField
from wtforms.validators import UUID, Optional, DataRequired

from internal.model import App


class GetWebAppResp(Schema):
    """获取WebApp基础信息的响应结构"""
    id = fields.UUID(dump_default="")
    icon = fields.String(dump_default="")
    name = fields.String(dump_default="")
    description = fields.String(dump_default="")
    app_config = fields.Dict(dump_default="")

    @pre_dump
    def process_data(self, data: App, **kwargs):
        app_config = data.app_config
        return {
            "id": data.id,
            "icon": data.icon,
            "name": data.name,
            "description": data.description,
            "app_config": {
                "opening_statement": app_config.opening_statement,
                "opening_questions": app_config.opening_questions,
                "suggested_after_answer": app_config.suggested_after_answer,
            }
        }

class WebAppChatReq(FlaskForm):
    """WebApp对话请求结构体"""
    conversation_id = StringField("conversation_id", default="", validators=[
        Optional(),
        UUID(message="会话id格式必须为uuid")
    ])
    query = StringField("query", default="", validators=[
        DataRequired(message="用户提问query不能为空")
    ])