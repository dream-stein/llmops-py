#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/16 00:29
#Author  :Emcikem
@File    :keyword_table_service.py
"""
from uuid import UUID

from injector import inject
from dataclasses import dataclass
from .base_service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from internal.model import KeywordTable
from internal.entity.cache_entity import LOCK_KEYWORD_TABLE_UPDATE_KEYWORD_TABLE, LOCK_EXPIRE_TIME
from redis import Redis

@inject
@dataclass
class KeywordTableService(BaseService):
    """知识库关键词表服务"""
    db: SQLAlchemy
    redis_client: Redis

    def get_keyword_table_from_dataset_id(self, dataset_id: UUID) -> KeywordTable:
        """根据传递的知识库id获取关键词表"""
        keyword_table = self.db.session.query(KeywordTable).filter(
            KeywordTable.dataset_id == dataset_id,
        ).one_or_none()
        if keyword_table is None:
            keyword_table = self.create(KeywordTable, dataset_id=dataset_id, keyword_table={})

        return keyword_table

    def delete_keyword_table_from_ids(self, dataset_id: UUID, segment_ids: list[UUID]) -> None:
        """根据传递的知识库id+片段id列表删除对应关键词表中多余的数据"""
        # 1.删除知识库关键词表里的多余的数据，该操作需要上锁，避免在并发的情况下哪道错误的数据
        cache_key = LOCK_KEYWORD_TABLE_UPDATE_KEYWORD_TABLE.format(dataset_id=dataset_id)
        with self.redis_client.lock(cache_key, timeout=LOCK_EXPIRE_TIME):
            # 2.获取当前知识库的关键词表
            keyword_table_record = self.get_keyword_table_from_dataset_id(dataset_id)
            keyword_table = keyword_table_record.keyword_table.copy()

            # 3.将片段id列表转换成集合，并创建关键词集合用于清除空关键词
            segment_ids_to_delete = set(segment_ids)
            keywords_to_delete = set()

            # 4.循环遍历所有关键词执行判断与更新
            for keyword, ids in keyword_table.items():
                ids_set = set(ids)
                if segment_ids_to_delete.intersection(ids_set):
                    keyword_table[keyword] = list(ids_set.difference(segment_ids_to_delete))
                    if not keyword_table[keyword]:
                        keywords_to_delete.add(keyword)

            # 5.检测空关键词数据并删除(关键词并没有映射任何字段id的数据)
            for keyword in keywords_to_delete:
                del keyword_table_record[keyword]

            # 6.将关键词更新到关键词表中
            self.update(keyword_table_record, keyword_table=keyword_table_record)