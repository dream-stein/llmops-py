#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 15:13
#Author  :Emcikem
@File    :dataset_handler.py
"""
from uuid import UUID

from injector import inject
from dataclasses import dataclass
from internal.schema.dataset_schema import (
    CreateDatasetReq,
    GetDatasetResp,
    UpdateDatasetReq,
    GetDatasetsWithPageReq,
    GetDatasetsWithPageResp
)
from pkg.paginator import PageModel
from pkg.response import validate_error_json, success_json, success_message
from internal.service import DatasetService, EmbeddingsService
from flask import request
from internal.service import JiebaService
from internal.core.file_extractor import FileExtractor

@inject
@dataclass
class DatasetHandler:
    """知识库处理器"""
    dataset_service: DatasetService
    jieba_service: JiebaService
    file_extractor: FileExtractor
    embeddings_service: EmbeddingsService

    def embeddings_query(self):
        query = request.args.get("query")
        keywords = self.jieba_service.extract_keywords(query)
        return success_json({"keywords": keywords})

    def create_dataset(self):
        """创建知识库"""
        # 1.提取请求并校验
        req = CreateDatasetReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建知识库
        self.dataset_service.create_dataset(req)

        # 3.返回成功调用提示
        return success_message("创建知识库成功")

    def get_dataset(self, dataset_id: UUID):
        """根据传递的知识库id获取详情"""
        dataset = self.dataset_service.get_dataset(dataset_id)
        resp = GetDatasetResp()

        return success_json(resp.dump(dataset))

    def update_dataset(self, dataset_id: UUID):
        """根据传递的知识库id+信息更新知识库"""
        # 1.提取请求并校验
        req = UpdateDatasetReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建知识库
        self.dataset_service.update_dataset(dataset_id, req)

        # 3.返回成功调用提示
        return success_message("更新知识库成功")

    def get_datasets_with_page(self):
        """获取知识库分页+搜索列表数据"""
        # 1.提取query数据并校验
        req = GetDatasetsWithPageReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取分页数据
        datasets, paginator = self.dataset_service.get_datasets_with_page(req)

        # 3.构建响应
        resp = GetDatasetsWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(datasets), paginator=paginator))
