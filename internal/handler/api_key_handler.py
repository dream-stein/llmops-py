#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 23:06
#Author  :Emcikem
@File    :api_key_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from injector import inject

@inject
@dataclass
class ApiKeyHandler:

    def create_api_key(self):
        """创建API秘钥"""
        pass

    def delete_api_key(self, api_key_id: UUID):
        """根据传递的id删除API秘钥"""
        pass

    def update_api_key(self, api_key_id: UUID):
        """根据传递的信息更新API秘钥"""
        pass

    def update_api_key_is_active(self, api_key_id: UUID):
        """根据传递的信息更新API秘钥激活状态"""
        pass

    def get_api_keys_with_page(self):
        """获取当且登录账号的API秘钥分页列表信息"""
        pass