#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 13:51
#Author  :Emcikem
@File    :app_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from flask import request
from flask_login import current_user
from injector import inject

from internal.schema.app_schema import CreateAppReq, GetAppResp, GetAppsWithPageReq, GetAppsWithPageResp
from internal.service import AppService
from pkg.paginator import PageModel
from pkg.response import success_json, success_message, validate_error_json


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""

        # 1.提取请求并校验
        req = CreateAppReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务创建应用信息
        app = self.app_service.create_app(req, current_user)

        # 3.返回创建成功响应提示
        return success_json({"id": app.id})

    def get_app(self, app_id: UUID):
        """获取指定的应用基础配置"""
        app = self.app_service.get_app(app_id, current_user)
        resp = GetAppResp()
        return success_json(resp.dump(app))

    def get_draft_app_config(self, app_id: UUID):
        """根据传递的应用id，获取指定的应用草稿配置信息"""
        draft_config = self.app_service.get_draft_app_config(app_id, current_user)
        return success_json(draft_config)

    def update_draft_app_config(self, app_id: UUID):
        """根据传递的应用id+草稿配置更新应用的最新草稿配置"""
        # 1.获取草稿请求json数据
        draft_app_config = request.get_json(force=True, silent=True) or {}

        draft_app_config = self.app_service._validate_draft_app_config(draft_app_config, current_user)

        return success_json(draft_app_config)

    def get_apps_with_page(self):
        """获取当前登录账号的应用分页列表数据"""
        # 1.提取数据并校验
        req = GetAppsWithPageReq(request.args)
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取列表数据以及分页器
        apps, paginator = self.app_service.get_apps_with_page(req, current_user)

        # 3.构建响应结构并返回
        resp = GetAppsWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(apps), paginator=paginator))


    def ping(self):
        pass
