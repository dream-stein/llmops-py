#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/12 15:36
#Author  :Emcikem
@File    :dataset_entity.py
"""
from enum import Enum

DEFAULT_DATASET_DESCRIPTION_FORMATTER = "当你需要回答关于《{name}》的时候，可以使用该知识库"

class ProcessType(str, Enum):
    """文档处理规则类型枚举"""
    AUTOMATIC = "automatic"
    CUSTOM = "custom"