#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 15:05
#Author  :Emcikem
@File    :http.py
"""
from flask import Flask

from config import Config
from internal.router import Router

class Http(Flask):
    """Http服务引擎"""

    def __init__(self, *args, conf: Config, router: Router, **kwargs):
        super().__init__(*args, **kwargs)
        # 注册应用路由
        router.register_router(self)

        self.config.from_object(conf)
