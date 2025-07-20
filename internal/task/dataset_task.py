#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/20 14:06
#Author  :Emcikem
@File    :dataset_task.py
"""
from uuid import UUID

from celery import shared_task

@shared_task
def delete_dataset(dataset_id: UUID) -> None:
    """根据传递的知识库id删除特定的知识库信息"""
    from app.http.module import injector
    from internal.service import IndexingService

    indexing_service = injector.get(IndexingService)
    indexing_service.delete_dataset(dataset_id)