#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/8 00:04
#Author  :Emcikem
@File    :config.py
"""
class Config:
    def __init__(self):
        # 关闭wtf的csrf保护
        self.WTF_CSRF_ENABLED = False