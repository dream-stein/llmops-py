#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/10 00:27
#Author  :Emcikem
@File    :default_config.py
"""
# 应用默认配置项
DEFAULT_CONFIG = {
    # wft配置
    "WTF_CSRF_ENABLED": "False",

    # SQLAlchemy数据库配置（默认使用本地sqlite，便于本地开发无需额外服务）
    "SQLALCHEMY_DATABASE_URI": "sqlite:///storage/dev.sqlite3",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": "True",

    # Redis数据库配置
    "REDIS_HOST": "localhost",
    "REDIS_PORT": 6379,
    "REDIS_USERNAME": "",
    "REDIS_PASSWORD": "",
    "REDIS_DB": 0,
    "REDIS_USE_SSL": "False",

    # Celery默认配置
    "CELERY_BROKER_DB": 1,
    "CELERY_RESULT_BACKEND_DB": 1,
    "CELERY_TASK_IGNORE_RESULT": "False",
    "CELERY_RESULT_EXPIRES": 3600,
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP": "True",

    # 辅助Agent智能体应用id
    "ASSISTANT_AGENT_ID": "6774fcef-b594-8008-b30c-a05b8190afe6"
}
