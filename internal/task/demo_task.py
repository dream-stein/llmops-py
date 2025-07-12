#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 13:57
#Author  :Emcikem
@File    :demo_task.py
"""
import time
from uuid import UUID

from celery import shared_task
from flask import current_app

@shared_task
def demo_task(id: UUID) -> str:
    """测试异步任务"""

    print("休眠5s")
    time.sleep(5)
    print(f"id的值:{id}")
    print(f"配置信息:{current_app.config}")
    return "木小可"