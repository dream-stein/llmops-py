#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/11 23:55
#Author  :Emcikem
@File    :upload_file_service.py
"""
from injector import inject
from dataclasses import dataclass
from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.model import UploadFile

@inject
@dataclass
class UploadFileService(BaseService):
    """上传文件记录服务"""
    db: SQLAlchemy

    def create_upload_file(self, **kwargs) -> UploadFile:
        """"创建文件上传记录"""
        return self.create(UploadFile, **kwargs)
