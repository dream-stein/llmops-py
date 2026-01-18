#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 11:08
@Author  : yps302@163.com
@File    : app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    """基础聊天接口请求验证"""
    # 必填、长度最大为2000
    query = StringField("query", validators=[
        DataRequired(message="用户提问必填！"),
        Length(max=2000, message="用户提问最大长度为2000！"),
    ])
