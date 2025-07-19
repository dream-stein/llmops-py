#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/19 12:31
#Author  :Emcikem
@File    :segment_handler.py
"""
from uuid import UUID

from injector import inject
from dataclasses import dataclass
from flask import request

from internal.schema.segment_schema import (
    GetSegmentsWithPageReq,
    GetSegmentsWithPageResp,
    GetSegmentResp, UpdateSegmentEnabledReq,
)
from pkg.paginator import PageModel
from pkg.response import validate_error_json, success_json, success_message
from internal.service import SegmentService


@inject
@dataclass
class SegmentHandler:
    """片段处理器"""
    segment_service: SegmentService

    def get_segments_with_page(self, dataset_id: UUID, document_id: UUID):
        """获取指定指示剂文档的片段列表信息"""
        # 1.提取请求并校验
        req = GetSegmentsWithPageReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取片段列表+分页数据
        segments, paginator = self.segment_service.get_segments_with_page(dataset_id, document_id, req)

        # 3.构建响应结构并返回
        resp = GetSegmentsWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(segments), paginator=paginator))

    def get_segment(self, dataset_id: UUID, document_id: UUID, segment_id: UUID):
        """获取指定的文档片段信息详情"""
        segment = self.segment_service.get_segment(dataset_id, document_id, segment_id)
        resp = GetSegmentResp()
        return success_json(resp.dump(segment))

    def update_segment_enabled(self, dataset_id: UUID, document_id: UUID, segment_id: UUID):
        """根据传递的信息更新指定的文档片段启用状态"""
        # 1.提取请求并校验
        req = UpdateSegmentEnabledReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新文档片段的启用状态
        self.segment_service.update_segment_enabled(dataset_id, document_id, segment_id, req.enabled.data)

        return success_message("修改片段状态成功")