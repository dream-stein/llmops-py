#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 11:22
@Author  : yps302@163.com
@File    : config.py
"""


class Config:
    def __init__(self):
        # 关闭wtf的csrf保护
        self.WTF_CSRF_ENABLED = False
