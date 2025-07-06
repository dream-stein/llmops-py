#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/6 15:33
#Author  :Emcikem
@File    :api_tool_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ValidateOpenAPISchemaReq(FlaskForm):
    """校验OpenAPI规范字符串请求"""
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])