#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/27 23:32
#Author  :Emcikem
@File    :category_entity.py
"""
from pydantic import BaseModel, Field

class CategoryEntity(BaseModel):
    """内置根据分类实体"""
    category: str = Field(default="") # 分类唯一标识
    name: str = Field(default="") # 分类对应的名称