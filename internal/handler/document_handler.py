#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/14 00:12
#Author  :Emcikem
@File    :document_handler.py
"""
from dataclasses import dataclass

from flask import request
from flask_login import current_user
from injector import inject
from uuid import UUID

from internal.schema.dataset_schema import UpdateDocumentEnabledReq
from internal.schema.document_schema import CreateDocumentsReq, CreateDocumentsResp, GetDocumentResp, \
    UpdateDocumentNameReq, GetDocumentsWithPageReq, GetDocumentsWithPageResp
from pkg.paginator import PageModel
from pkg.response import validate_error_json, success_json, success_message
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
        documents, batch = self.document_service.create_documents(dataset_id, current_user, **req.data)

        # 3.生成响应结构并返回
        resp = CreateDocumentsResp()

        return success_json(resp.dump((documents, batch)))

    def get_document(self, dataset_id: UUID, document_id: UUID):
        """根据传递的知识库id+文档id获取文档详情信息"""
        document = self.document_service.get_documents(dataset_id, document_id, current_user)

        resp = GetDocumentResp()

        return success_json(resp.dump(document))


    def update_document_name(self, dataset_id: UUID, document_id: UUID):
        """根据传递的知识库id+文档id更新对呀文档的名称信息"""
        # 1.提取请求并校验数据
        req = UpdateDocumentNameReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新文档名称信息
        self.document_service.update_document(dataset_id, document_id, account=current_user, name=req.name.data)

        return success_message("更新文档名称成功")

    def update_document_enabled(self, dataset_id: UUID, document_id: UUID):
        """根据传递的知识库id+文档id更新指定文档的启用状态"""
        # 1.提取请求并校验
        req = UpdateDocumentEnabledReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更改指定文档的状态
        self.document_service.update_document_enabled(dataset_id, document_id, req.enabled.data, current_user)

        return success_message("更改文档启用状态成功")

    def delete_document(self, dataset_id: UUID, document_id: UUID):
        """根据指定的知识库id+文档id删除指定的文档信息"""
        self.document_service.delete_document(dataset_id, document_id, current_user)

        return success_message("删除文档成功")

    def get_documents_with_page(self, dataset_id: UUID):
        """根据传递的知识库id获取文档分页列表数据"""
        # 1.提取请求数据并校验
        req = GetDocumentsWithPageReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取分页列表数据以及分页数据
        documents, paginator = self.document_service.get_documents_with_page(dataset_id, req, current_user)

        # 3.构建响应结构并映射
        resp = GetDocumentsWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(documents), paginator=paginator))

    def get_documents_status(self, dataset_id: UUID, batch: str):
        """根据传递的知识库id+批处理标识或取文档的状态"""
        documents_status = self.document_service.get_documents_status(dataset_id, batch, current_user)

        return success_json(documents_status)