#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/14 00:12
#Author  :Emcikem
@File    :document_handler.py
"""
from dataclasses import dataclass
from injector import inject
from uuid import UUID
from internal.schema.document_schema import CreateDocumentsReq, CreateDocumentsResp
from pkg.response import validate_error_json, success_json
from internal.service import DocumentService

@inject
@dataclass
class DocumentHandler:
    """文档处理器"""
    document_service: DocumentService

    def create_documents(self, dataset_id: UUID):
        """知识库新增/上传文档列表"""
        # 1.提取请求并校验
        req = CreateDocumentsReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务并创建文档，返回文档列表信息+处理批次
        documents, batch = self.document_service.create_documents(dataset_id, **req.data)

        # 3.生成响应结构并返回
        resp = CreateDocumentsResp()

        return success_json(resp.dump((documents, batch)))

    def get_documents_status(self, dataset_id: UUID, batch: str):
        """根据传递的知识库id+批处理标识或取文档的状态"""
        documents_status = self.document_service.get_documents_status(dataset_id, batch)

        return success_json(documents_status)