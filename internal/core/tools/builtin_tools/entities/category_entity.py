#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/6 13:18
#Author  :Emcikem
@File    :category_entity.py
"""
from pydantic import BaseModel, field_validator

from internal.exception import FailException


class CategoryEntity(BaseModel):
    """分类实体"""
    category: str # 分类唯一标识
    name: str # 分类名称
    icon: str # 分类图标名称

    @field_validator('icon')
    def check_icon_extension(cls, value: str):
        """校验icon的扩展名是不是svg，如果不是抛出错误"""
        if not value.endswith(".svg"):
            raise FailException(f"该分类的icon图标不是.svg格式")
        return value