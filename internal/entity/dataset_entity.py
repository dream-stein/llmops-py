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

# 默认的处理规则
DEFAULT_PROCESS_RULE = {
    "mode": "custom",
    "rule": {
        "pre_process_rules": [
            {"id": "remove_extra_space", "enabled": True},
            {"id": "remove_url_and_email", "enabled": True},
        ],
        "segment": {
            "separators": [
                "\n\n",
                "\n",
                "。|！|？",
                "\.\s|\!\s|\?\s",  # 英文标点符号后面通常需要加空格
                "; |;\s",
                ", |,\s",
                " ",
                ""
            ],
            "chunk_size": 500,
            "chunk_overlap": 50,
        }
    }
}

class DocumentStatus(str, Enum):
    """文档状态类型枚举"""
    WAITING = "waiting"
    PARSING = "parsing"
    SPLITTING = "splitting"
    INDEXING = "indexing"
    COMPLETED = "completed"
    ERROR = "error"

class SegmentStatus(str, Enum):
    """片段状态类型枚举"""
    WAITING = "waiting"
    INDEXING = "indexing"
    COMPLETED = "completed"
    ERROR = "error"

class RetrievalStrategy(str, Enum):
    """检索策略类型枚举"""
    FULL_TEXT = "fulltext"
    SEMANTIC = "semantic"
    HYBRID = "hybrid"

class RetrievalSource(str, Enum):
    """检索来源"""
    HIT_TESTING = "hit_testing"
    APP = "app"