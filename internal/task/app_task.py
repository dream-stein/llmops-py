#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/24 14:55
#Author  :Emcikem
@File    :app_task.py
"""
from uuid import UUID

from celery import shared_task

@shared_task
def auto_create_app(
        name: str,
        description: str,
        account_id: UUID,
) -> None:
    """根据传递的名称、描述、账号id创建一个Agent"""
    from app.http.module import injector
    from internal.service import AppService

    app_service = injector.get(AppService)
    app_service.auto_create_app(name, description, account_id)