#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/14 23:16
#Author  :Emcikem
@File    :indexing_service.py
"""
import re
import uuid
from datetime import datetime
from uuid import UUID

from injector import inject
from dataclasses import dataclass

from sqlalchemy import func

from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.model import Document, Segment
from internal.entity.dataset_entity import DocumentStatus, SegmentStatus
from langchain_core.documents import Document as LCDocument

from internal.core.file_extractor import FileExtractor
from .process_rule_service import ProcessRuleService
from .embeddings_service import EmbeddingsService
from internal.lib.helper import generate_text_hash

@inject
@dataclass
class IndexingService(BaseService):
    """索引构建服务"""
    db: SQLAlchemy
    file_extractor: FileExtractor
    process_rule_service: ProcessRuleService
    embeddings_service: EmbeddingsService

    def build_documents(self, document_ids: list[UUID]) -> None:
        """根据传递的文档id列表构建知识库，涵盖了加兹安、分割、索引构建、数据"""
        # 1.根据传递的文档id获取所有文档
        documents = self.db.session.query(Document).filter(
            Document.id.in_(document_ids)
        ).all()

        # 2.执行循环遍历所有文档完成对每个文档的构建
        for document in documents:
            try:
                # 3.更新当前状态为解析中，并记录开始处理的时间
                self.update(document, status=DocumentStatus.PARSING, processing_started_at=datetime.now())

                # 4.执行文档加载步骤，并更新文档状态与时间
                lc_documents = self._parsing(document)

                # 5.执行文档分割步骤，并更新文档状态与时间，涵盖了片段的信息
                lc_segments = self._splitting(document, lc_documents)

                # 6.执行文档索引构建，涵盖关键词提取、向量，并更新数据状态


                # 7.存储操作，涵盖文档状态更新，以及向量数据库的存储
                pass
            except Exception as e:
                self.update(
                    document,
                    status=DocumentStatus.ERROR,
                    error=str(e),
                    stopped_at=datetime.now(),
                )

    def _parsing(self, document: Document) -> list[LCDocument]:
        """解析传递的文档为LangChain文档列表"""
        # 1.获取upload_file并加载LangChain文档
        upload_file = document.upload_file
        lc_documents = self.file_extractor.load(upload_file, False, True)

        # 2.循环处理LangChain文档，并删除多余的空白字符串
        for lc_documents in lc_documents:
            lc_documents.page_content = self._clean_extra_text(lc_documents.page_content)

        # 3.更新文档状态并记录时间
        self.update(
            document,
            character_count=sum([len(lc_documents.page_content) for lc_documents in lc_documents]),
            status=DocumentStatus.SPLITTING,
            parsing_cpmpleted_at=datetime.now(),
        )

        return lc_documents

    def _splitting(self, document: Document, lc_documents: list[LCDocument]) -> list[LCDocument]:
        """根据传递的信息进行文档分割，拆分成小块片段"""
        # 1.根据process_rule获取文本分割器
        process_rule = document.process_rule
        text_splitter = self.process_rule_service.get_text_splitter_by_process_rule(
            process_rule,
            self.embeddings_service.calculate_token_count,
        )

        # 2.按照process_rule规则清除多余的字符串
        for lc_document in lc_documents:
            lc_document.page_content = self.process_rule_service.clean_text_by_process_rule(
                lc_document.page_content,
                process_rule,
            )

        # 3.分割文档列表为片段列表
        lc_segments = text_splitter.split_documents(lc_documents)

        # 4.获取对应文档下得到最大片段位置
        position = self.db.session.query(func.coalesce(func.max(Segment.position), 0)).filter(
            Segment.document_id == document.id,
        ).scalar()

        # 5.循环处理片段数据并添加有数据，他是村粗到MySQL数据库中
        segments = []
        for lc_segment in lc_segments:
            position += 1
            content = lc_segment.page_content
            segment = self.create(
                Segment,
                account_id=document.account_id,
                dataset_id=document.dataset_id,
                document_id=document.id,
                node_id=str(uuid.uuid4()),
                position=position,
                content=content,
                character_count=len(content),
                token_count=self.embeddings_service.calculate_token_count(content),
                hash=generate_text_hash(content),
                status=SegmentStatus.WAITING,
            )
            lc_segment.metadata = {
                "account_id": str(document.account_id),
                "dataset_id": document.dataset_id,
                "document_id": str(document.id),
                "segment_id": str(segment.id),
                "node": str(segment.node_id),
                "document_enabled": False,
                "segment_enabled": False,
            }
            segments.append(segment)

        # 6.更新文档的数据，涵盖状态、token数等内容
        self.update(
            document,
            token_count=sum([len(segment.token_count) for segment in segments]),
            status=DocumentStatus.INDEXING,
            splitting_cpmpleted_at=datetime.now(),
        )

        return lc_segments

    @classmethod
    def _clean_extra_text(cls, text: str) -> str:
        """清除过滤传递的多余空白字符串"""
        text = re.sub(r'<\|', '<', text)
        text = re.sub(r'\|>', '>', text)
        text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F\xEF\xBF\xBE]', '', text)
        text = re.sub('\uFFFE', '', text)  # 删除零宽非标记字符
        return text