#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 18:29
#Author  :Emcikem
@File    :account_handler.py
"""
from flask_login import current_user
from injector import inject
from dataclasses import dataclass
from internal.schema.account_schema import GetCurrentUserResp, UpdatePasswordReq, UpdateNameReq, UpdateAvatarReq
from pkg.response import success_json, validate_error_json, success_message
from internal.service import AccountService


@inject
@dataclass
class AccountHandler:
    """账号设置处理器"""
    account_service: AccountService

    def get_current_user(self):
        """获取当且登录账号信息"""
        resp = GetCurrentUserResp()
        return success_json(resp.dump(current_user))

    def update_password(self):
        """更新当且登录账号密码"""
        # 1.提取请求数据并校验
        req = UpdatePasswordReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号密码
        self.account_service.update_password(req.password.data, current_user)

        return success_message("更新账号密码成功")

    def update_name(self):
        """更新当且登录账号名称"""
        # 1.提起请求数据并校验
        req = UpdateNameReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号名称
        self.account_service.update_account(current_user, name=req.name.data)

        return success_message("更新账号名称成功")



    def update_avatar(self):
        """更新当且账号头像"""
        # 1.提取请求数据并校验
        req = UpdateAvatarReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务更新账号头像
        self.account_service.update_account(current_user, avatar=req.avatar.data)

        return success_message("更新账号成功")
