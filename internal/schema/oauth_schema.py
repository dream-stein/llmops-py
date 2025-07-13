#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 14:15
#Author  :Emcikem
@File    :oauth_schema.py
"""
from flask_wtf import FlaskForm
from marshmallow import Schema, fields
from wtforms import StringField
from wtforms.validators import DataRequired


class AuthorizeReq(FlaskForm):
    """第三方授权认证请求体"""
    code = StringField('code', validators=[DataRequired("code代码不能为空")])

class AuthorizeResp(Schema):
    """第三方授权认证响应结构"""