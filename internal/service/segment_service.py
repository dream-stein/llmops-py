#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/19 16:14
#Author  :Emcikem
@File    :segment_service.py
"""
import uuid
from datetime import datetime
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from numpy import character
from sqlalchemy import asc, func

from internal.entity.cache_entity import LOCK_SEGMENT_UPDATE_ENABED, LOCK_EXPIRE_TIME
from internal.entity.dataset_entity import SegmentStatus, DocumentStatus
from internal.exception import NotFoundException, FailException, ValidateErrorException
from internal.lib.helper import generate_text_hash
from internal.model import Segment, Document, Account
from internal.schema.segment_schema import (
    GetSegmentsWithPageReq,
    CreateSegmentReq,
    UpdateSegmentReq
)
from internal.service import (
    BaseService,
    KeywordTableService,
    VectorDatabaseService,
    EmbeddingsService,
    JiebaService,
)
from pkg.paginator import Paginator
from pkg.sqlalchemy import SQLAlchemy
from redis import Redis
from langchain_core.documents import Document as LCDocument

@inject
@dataclass
class SegmentService(BaseService):
    """片段服务"""

    db: SQLAlchemy
    redis_client: Redis
    keyword_table_service: KeywordTableService
    vector_database_service: VectorDatabaseService
    jieba_service: JiebaService
    embeddings_service: EmbeddingsService

    def create_segment(
            self,
            dataset_id: UUID,
            document_id: UUID,
            req: CreateSegmentReq,
            account: Account
    ) -> Segment:
        """根据传递的信息新增文档片段信息"""
        # 1.校验上传内容的token长度总数，不能超过1000
        token_count = self.embeddings_service.calculate_token_count(req.content.data)
        if token_count > 1000:
            raise ValidateErrorException("片段内容的长度不能超过1000 token")

        # 2.获取文档信息并校验
        document = self.get(Document, document_id)
        if (
            document is None
            or document.account_id != account.id
            or document.dataset_id != dataset_id
        ):
            raise NotFoundException("该知识库文档不存在，或无权限新增，请核实后重试")

        # 3.判断文档的状态是否可以新增片段数据，只有completed才可以新增
        if document.status != DocumentStatus.COMPLETED:
            raise FailException("当前文档不可新增片段，请稍后尝试")

        # 4.提取文档片段的最大的位置
        position = self.db.session.query(func.coalesce(func.max(Segment.position), 0)).filter(
            Segment.document_id == document_id
        ).scalar()

        # 5.检测是否传递了keywords，如果没有传递的话，调用jieba服务生成关键词
        if req.keywords.data is None or len(req.keywords.data) == 0:
            req.keywords.data = self.jieba_service.extract_keywords(req.content.data, 10)

        # 6.往MySQL数据中新增记录
        segment = None
        try:
            # 7.位置+1并且新增segment记录
            position += 1
            segment = self.create(
                Segment,
                account_id=account.id,
                dataset_id=dataset_id,
                document_id=document_id,
                node_id=uuid.uuid4(),
                position=position,
                content=req.content.data,
                character_count=len(req.content.data),
                token_count=token_count,
                keywords=req.keywords.data,
                hash=generate_text_hash(req.content.data),
                enabled=True,
                processing_started_at=datetime.now(),
                indexing_completed_at=datetime.now(),
                completed_at=datetime.now(),
                status=SegmentStatus.COMPLETED,
            )

            # 8.往向量数据库中新增数据
            self.vector_database_service.vector_store.add_documents(
                [LCDocument(
                    page_content=req.content.data,
                    metadata={
                        "account_id": document.account_id,
                        "dataset_id": document.dataset_id,
                        "document_id": document_id,
                        "segment_id": segment.id,
                        "node_id": segment.node_id,
                        "document_enabled": document.enabled,
                        "segment_enabled": True,
                    }
                )],
                ids=[segment.node_id]
            )

            # 9.重新计算片段的字符串总数以及token总数
            document_character_count, document_token_count = self.db.session.query(
                func.coalesce(func.sum(Segment.character_count), 0),
                func.coalesce(func.sum(Segment.token_count), 0)
            ).filter(Segment.document_id == document.id).first()

            # 10.更新文档的对应信息
            self.update(
                document,
                character_count=document_character_count,
                token_count=document_token_count,
            )

            # 11.更新关键词表信息
            if document.enabled is True:
                self.keyword_table_service.add_keyword_table_from_ids(dataset_id, [segment.id])

            return segment
        except Exception as e:
            if segment:
                self.update(
                    segment,
                    error=str(e),
                    status=SegmentStatus.ERROR,
                    enabled=False,
                    disabled_at=datetime.now(),
                    stopped_at=datetime.now(),
                )
            raise FailException("新增文档片段失败，请稍后尝试")

    def update_segment(
            self,
            dataset_id: UUID,
            document_id: UUID,
            segment_id: UUID,
            req: UpdateSegmentReq,
            account: Account,
    ) -> Segment:
        """根据传递的信息更新指定的文档片段信息"""
        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
                segment is None
                or segment.account_id != account.id
                or segment.dataset_id != dataset_id
                or segment.document_id != document_id
        ):
            raise NotFoundException("该文档片段不存在，或无权限修改，请核实后重试")

        # 2.判断文档片段是否处于可修改的状态
        if segment.status != SegmentStatus.COMPLETED:
            raise FailException("当前片段不可修改状态，请稍后尝试")

        # 3.检测是否传递了keywords，如果没有传递的话，调用jieba服务生成关键词
        if req.keywords.data is None or len(req.keywords.data) == 0:
            req.keywords.data = self.jieba_service.extract_keywords(req.content.data, 10)

        # 4.计算新内容hash值，用于判断是否需要更新向量数据库以及文档详情
        new_hash = generate_text_hash(req.content.data)
        required_update = segment.hash != new_hash

        try:
            # 5.更新segment记录
            self.update(
                segment,
                keywords=req.keywords.data,
                content=req.content.data,
                hash=new_hash,
                character_count=len(req.content.data),
                token_count=self.embeddings_service.calculate_token_count(req.content.data),
            )

            # 7.更新片段归属关键词信息
            self.keyword_table_service.delete_keyword_table_from_ids(dataset_id, [segment_id])
            self.keyword_table_service.add_keyword_table_from_ids(dataset_id, [segment_id])

            # 8.检测是否需要更新文档信息以及向量数据库
            if required_update:
                # 7.更新文档信息，涵盖字符总数、token总次数
                document = segment.document
                document_character_count, document_token_count = self.db.session.query(
                    func.coalesce(func.sum(Segment.character_count), 0),
                    func.coalesce(func.sum(Segment.token_count), 0)
                ).filter(Segment.document_id == document.id).first()

                # 7.更新文档的对应信息
                self.update(
                    document,
                    character_count=document_character_count,
                    token_count=document_token_count,
                )

                # 8.更新向量数据库对应记录
                self.vector_database_service.collection.data.update(
                    uuid=segment.node_id,
                    properties={
                        "text": req.content.data,
                    },
                    vector=self.embeddings_service.embeddings.embed_query(req.content.data)
                )
        except Exception as e:
            raise FailException("更新片段记录失败，请稍后重试")

        return segment

    def get_segments_with_page(
            self,
            dataset_id: UUID,
            document_id: UUID,
            req: GetSegmentsWithPageReq,
            account: Account
    ) -> tuple[list[Segment], Paginator]:
        """根据传递的信息获取片段列表分页数据"""
        # 1.获取文档并校验权限
        document = self.get(Document, document_id)
        if document is None or document.dataset_id != dataset_id or document.account_id != account.id:
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

    def get_segment(
            self,
            dataset_id: UUID,
            document_id: UUID,
            segment_id: UUID,
            account: Account,
    ) -> Segment:
        """根据传递的信息获取片段详情"""
        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
            segment is None
            or segment.account_id != account.id
            or segment.dataset_id != dataset_id
            or segment.document_id != document_id
        ):
            raise NotFoundException("该文档片段不存在，或无权限查看，请核实后重试")

        return segment

    def update_segment_enabled(
            self,
            dataset_id: UUID,
            document_id: UUID,
            segment_id: UUID,
            enabled: bool,
            account: Account,
    ) -> Segment:
        """根据传递的信息更新文档片段的启用状态信息"""
        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
                segment is None
                or segment.account_id != account.id
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
                return segment
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

    def delete_segment(
            self,
            dataset_id: UUID,
            document_id: UUID,
            segment_id: UUID,
            account: Account,
    ) -> Segment:
        """根据传递的信息删除指定的文档片段信息，该服务是同步方法"""
        # 1.获取片段信息并校验权限
        segment = self.get(Segment, segment_id)
        if (
                segment is None
                or segment.account_id != account.id
                or segment.dataset_id != dataset_id
                or segment.document_id != document_id
        ):
            raise NotFoundException("该文档片段不存在，或无权限查看，请核实后重试")

        # 2.判断文档是否处于可以删除的状态，只有COMPLETED/ERROR才可以删除
        if segment.status not in [SegmentStatus.COMPLETED, SegmentStatus.ERROR]:
            raise FailException("当前文档片段处于不可删除状态，请稍后尝试")

        # 3.删除文档片段并获取该文档的片段信息
        document = segment.document
        self.delete(segment)

        # 4.同步删除关键词表中属于该片段的关键词
        self.keyword_table_service.delete_keyword_table_from_ids(dataset_id, [segment_id])

        # 5.同步删除向量数据库存储的记录
        try:
            self.vector_database_service.collection.data.delete_by(segment.node_id)
        except Exception as e:
            print("")

        # 6.更新文档信息，涵盖字符串总数、token总次数
        document_character_count, document_token_count = self.db.session.query(
            func.coalesce(func.sum(Segment.character_count), 0),
            func.coalesce(func.sum(Segment.token_count), 0)
        ).filter(Segment.document_id == document.id).first()

        # 7.更新文档的对应信息
        self.update(
            document,
            character_count=document_character_count,
            token_count=document_token_count,
        )

        return segment
