#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 13:35
#Author  :Emcikem
@File    :celery_extension.py
"""
from celery import Task, Celery
from flask import Flask

def init_app(app: Flask):
    """Celery配置服务初始化"""

    class FakeTask(Task):
        """定义FlaskTask，确保Celery在Flask应用的上下文中运行，这样可以访问flask配置、数据库等内容"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    # 1.创建Celery应用并配置
    celery_app = Celery(app.name, task_cls=FakeTask)
    celery_app.config_from_object(app.config["CELERY"])

    # 将celery挂在到app的扩展中
    app.extensions["celery"] = celery_app