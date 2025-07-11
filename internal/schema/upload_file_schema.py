#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/11 21:31
#Author  :Emcikem
@File    :upload_file_schema.py
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from marshmallow import Schema, fields, pre_dump

from internal.entity.upload_file_entity import ALLOWED_DOCUMENT_EXTENSION
from internal.model import UploadFile

class UploadFileReq(FlaskForm):
    """上传文件请求"""
    file = FileField("file", validators=[
        FileRequired("上传文件不能为空"),
        FileSize(max_size=15*1024*1024, message="上传文件大小不能超过15MB"),
        FileAllowed(ALLOWED_DOCUMENT_EXTENSION, message=f"仅允许上传{'/'.join(ALLOWED_DOCUMENT_EXTENSION)}文件")
    ])

class UploadFileResp(Schema):
    """上传文件的接口响应接口"""
    id = fields.UUID(default="")
    account_id = fields.UUID(default="")
    name = fields.String(default="")
    key = fields.String(default="")
    size = fields.Integer(default=0)
    extension = fields.String(default="")
    mime_type = fields.String(default="")
    created_at = fields.Integer(default=0)

    @pre_dump
    def process_data(self, data: UploadFile, **kwargs):
        return {
            "id": data.id,
            "account_id": data.account_id,
            "name": data.name,
            "key": data.key,
            "size": data.size,
            "extension": data.extension,
            "mime_type": data.mime_type,
            "created_at": int(data.created_at.timestamp()),
        }