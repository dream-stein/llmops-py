#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/19 16:14
#Author  :Emcikem
@File    :segment_service.py
"""
from datetime import datetime
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from sqlalchemy import asc

from internal.entity.cache_entity import LOCK_SEGMENT_UPDATE_ENABED, LOCK_EXPIRE_TIME
from internal.entity.dataset_entity import SegmentStatus
from internal.exception import NotFoundException, FailException
from internal.model import Segment, Document
from internal.schema.segment_schema import GetSegmentsWithPageReq
from internal.service import BaseService, KeywordTableService, VectorDatabaseService
from pkg.paginator import Paginator
from pkg.sqlalchemy import SQLAlchemy
from redis import Redis

@inject
@dataclass
class SegmentService(BaseService):
    """片段服务"""

    db: SQLAlchemy
    redis_client: Redis
    keyword_table_service: KeywordTableService
    vector_database_service: VectorDatabaseService

    def get_segments_with_page(
            self, dataset_id: UUID, document_id: UUID, req: GetSegmentsWithPageReq
    ) -> tuple[list[Segment], Paginator]:
        """根据传递的信息获取片段列表分页数据"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.获取文档并校验权限
        document = self.get(Document, document_id)
        if document is None or document.dataset_id != dataset_id or str(document.document_id) != document_id:
            raise NotFoundException("该知识库文档不存在，或无权限查看，请核实后重试")

        # 2.构建分页查询器
        paginator = Paginator(db=self.db, req=req)

        # 3.构建筛选器
        filters = [Segment.document_id == document_id]
        if req.search_word.data:
            filters.append(Segment.content.ilike(f"%{req.search_word.data}%"))

        # 4.执行分页并获取数据
        segments = paginator.paginate(
            self.db.session.query(Segment).filter(*filters).order_by(asc("position"))
        )

        return segments, paginator

    def get_segment(self, dataset_id: UUID, document_id: UUID, segment_id: UUID) -> Segment:
        """根据传递的信息获取片段详情"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
            segment is None
            or str(segment.account_id) != account_id
            or segment.dataset_id != dataset_id
            or segment.document_id != document_id
        ):
            raise NotFoundException("该文档片段不存在，或无权限查看，请核实后重试")

        return segment

    def update_segment_enabled(
            self, dataset_id: UUID, document_id: UUID, segment_id: UUID, enabled: bool
    ) -> Segment:
        """根据传递的信息更新文档片段的启用状态信息"""
        # todo:等待授权认证模块
        account_id = "b8434b9c-ee56-4bfd-bd24-84d3caef5599"

        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
                segment is None
                or str(segment.account_id) != account_id
                or segment.dataset_id != dataset_id
                or segment.document_id != document_id
        ):
            raise NotFoundException("该文档片段不存在，或无权限查看，请核实后重试")

        # 2.判断文档片段是否处于可启用/禁用的环境
        if segment.status != SegmentStatus.COMPLETED:
            raise FailException("当前片段不可修改状态，请稍后重试")

        # 3.判断更新的片段启用状态和数据库的数据是否一致，如果是则抛出错误
        if enabled == segment.enabled:
            raise FailException(f"片段状态修改错误，当前以是{'启用' if enabled else '禁用'}")

        # 4.获取更新片段启用状态所并上锁检测
        cache_key = LOCK_SEGMENT_UPDATE_ENABED.format(segment_id=segment_id)
        cache_result = self.redis_client.get(cache_key)
        if cache_result is not None:
            raise FailException("当前文档片段正在修改状态，请稍后重试")

        # 5.上锁并更新对应的数据，涵盖MySQL的记录、weaviate、关键词表
        with self.redis_client.lock(cache_key, LOCK_EXPIRE_TIME):
            try:
                # 6.修改MySQL数据库里的文档片段状态
                self.update(
                    segment,
                    enabled=enabled,
                    disabled_at=None if enabled else datetime.utcnow(),
                )

                # 7.更新关键词表的对应信息，有可能新增，也有可能删除
                document = segment.document
                if enabled is True and document.enabled is True:
                    self.keyword_table_service.add_keyword_table_from_ids(dataset_id, [segment_id])
                else:
                    self.keyword_table_service.delete_keyword_table_from_ids(dataset_id, [segment_id])

                # 8.同步处理weaviate数据
                self.vector_database_service.collection.data.update(
                    uuid=segment.node_id,
                    properties={"segment_enabled": enabled},
                )
            except Exception as e:
                self.update(
                    segment,
                    error =str(e),
                    status=SegmentStatus.ERROR,
                    enabled=False,
                    disabled_at=datetime.now(),
                    stopped_at=datetime.now(),
                )
                raise FailException("当前文档片段启用失败，请稍后重试")