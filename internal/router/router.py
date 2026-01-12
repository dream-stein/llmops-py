#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/11 17:16
@Author  : yps302@163.com
@File    : router.py
"""
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import APPHandler


@dataclass
@inject
class Router:
    """路由"""
    app_handler: APPHandler

    def register_router(self, app: Flask):
        """注册路由"""
        # 1.创建一个蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2.将蓝图与对应控制器方法绑定
        bp.add_url_rule("/ping", view_func=self.app_handler.ping)

        # 3.在应用上注册蓝图
        app.register_blueprint(bp)
