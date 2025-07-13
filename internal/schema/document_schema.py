#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/14 00:14
#Author  :Emcikem
@File    :document_schema.py
"""
from flask_wtf import FlaskForm
from marshmallow import Schema, fields, pre_dump
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, AnyOf
from internal.entity.dataset_entity import ProcessType
from .schema import ListField, DictField

from internal.model import Document

class CreateDocumentsReq(FlaskForm):
    """创建/心智文档列表规则"""
    upload_file_ids = ListField("upload_file_ids")
    process_type = StringField("process_type", validators=[
        DataRequired("文档处理类型不能为空"),
        AnyOf(values=[ProcessType.AUTOMATIC, ProcessType.CUSTOM], message="处理类型格式错误")
    ])
    rule = DictField("rule")

class CreateDocumentsResp(Schema):
    """创建文档列表响应结构"""
    documents = fields.List(fields.Dict, dump_default=[])
    batch = fields.String(dump_default="")

    @pre_dump
    def process_type(self, data: tuple[list[Document], str], **kwargs):
        return {
            "documents": [{
                "id": document.id,
                "name": document.name,
                "status": document.status,
                "created_at": int(document.created_at.timestamp()),
            }for document in data[0]],
            "batch": data[1]
        }

