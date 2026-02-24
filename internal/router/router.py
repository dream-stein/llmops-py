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


@inject
@dataclass
class Router:
    """路由"""
    app_handler: APPHandler

    def register_router(self, app: Flask):
        """注册路由"""
        # 1.创建一个蓝图
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2.将蓝图与对应控制器方法绑定
        bp.add_url_rule("/ping", view_func=self.app_handler.ping)
        bp.add_url_rule("/apps/<uuid:app_id>/debug", methods=["POST", "OPTIONS"], view_func=self.app_handler.debug)
        bp.add_url_rule("/app", methods=["POST"], view_func=self.app_handler.create_app)
        bp.add_url_rule("/app/<uuid:id>", methods=["GET"], view_func=self.app_handler.get_app)
        bp.add_url_rule("/app/<uuid:id>", methods=["POST"], view_func=self.app_handler.update_app)
        bp.add_url_rule("/app/<uuid:id>/delete", methods=["POST"], view_func=self.app_handler.delete_app)
        # 3.在应用上注册蓝图
        app.register_blueprint(bp)
