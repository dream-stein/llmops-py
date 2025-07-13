#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/14 00:23
#Author  :Emcikem
@File    :document_service.py
"""
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from internal.entity.upload_file_entity import ALLOWED_DOCUMENT_EXTENSION
from internal.exception import ForbiddenException, FailException
from internal.model import Document, Dataset, UploadFile
from internal.service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.entity.dataset_entity import ProcessType

@inject
@dataclass
class DocumentService(BaseService):
    """文档服务"""
    db: SQLAlchemy

    def create_documents(
            self,
            dataset_id: UUID,
            upload_file_ids: list[UUID],
            process_type: str = ProcessType.AUTOMATIC,
            rule: dict = None
    ) -> tuple[list[Document], str]:
        """根据传递的信息创建文档列表并调用异步任务"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.检测知识库权限
        dataset = self.get(Dataset, dataset_id)
        if dataset is None or str(dataset.account_id) != account_id:
            raise ForbiddenException("当前用户无该数据库权限或知识库不存在")

        # 2.提取维基并校验文件权限与文件扩展
        upload_files = self.db.session.query(UploadFile).filter(
            UploadFile.account_id == account_id,
            UploadFile.id in upload_file_ids,
        ).all()
        upload_files = [
            upload_file for upload_file in upload_files
            if upload_file.extension.lower() in ALLOWED_DOCUMENT_EXTENSION
        ]
        if len(upload_files) == 0:
            raise FailException("暂未解析到合法文件，请重新上传")

        # 3.创建批次与处理规则并记录到数据库中
