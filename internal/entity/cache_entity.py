#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/17 22:59
#Author  :Emcikem
@File    :cache_entity.py
"""
# 缓存锁的过期时间，单位为妙，默认为600
LOCK_EXPIRE_TIME = 600

# 更新文档启用状态缓存锁
LOCK_DOCUMENT_UPDATE_ENABLED = "lock:document:update:enabled_{document_id}"