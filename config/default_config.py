#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 22:05
@Author  : yps302@163.com
@File    : default_config.py
"""
# 应用默认配置
DEFAULT_CONFIG = {
    # wft配置
    "WTF_CSRF_ENABLED": False,
    # SQLALCHEMY数据库配置
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": True,
}
