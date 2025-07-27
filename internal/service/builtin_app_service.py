#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/28 00:17
#Author  :Emcikem
@File    :builtin_app_service.py
"""
from dataclasses import dataclass

from injector import inject

from internal.core.builtin_apps import BuiltinAppManager
from internal.core.builtin_apps.entities.builtin_app_entity import BuiltinAppEntity
from internal.core.builtin_apps.entities.category_entity import CategoryEntity
from internal.service import BaseService

@inject
@dataclass
class BuiltinAppService(BaseService):
    """内置应用服务"""
    builtin_app_manager: BuiltinAppManager

    def get_categories(self) -> list[CategoryEntity]:
        """获取分类列表信息"""
        return self.builtin_app_manager.get_categories()

    def get_builtin_apps(self) -> list[BuiltinAppEntity]:
        """获取所有内置应用实体信息列表"""
        return self.builtin_app_manager.get_builtin_apps()
