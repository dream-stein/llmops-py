#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/15 00:13
#Author  :Emcikem
@File    :process_rule_service.py
"""
import re
from typing import Callable

from injector import inject
from dataclasses import dataclass
from internal.model import ProcessRule
from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter

@inject
@dataclass
class ProcessRuleService:
    """处理规则服务"""

    @classmethod
    def get_text_splitter_by_process_rule(
            cls,
            process_rule: ProcessRule,
            length_function: Callable[[str], int],
            **kwargs
    ) -> TextSplitter:
        """根据传递的处理规则+长度计算函数，获取相应的文本分割器"""
        return RecursiveCharacterTextSplitter(
            chunk_size=process_rule.rule["segment"]["chunk_size"],
            chunk_function=process_rule.rule["segment"]["chunk_overlap"],
            separators=process_rule.rule["segment"]["separators"],
            is_separator_regex=True,
            length_function=length_function,
            **kwargs
        )

    @classmethod
    def clean_text_by_process_rule(cls, text: str, process_rule: ProcessRule) -> str:
        """根据传递的处理规则清除多余的字符串"""
        # 1.循环遍历所有与处理规则
        for pre_process_rule in process_rule.rule["pre_process_rules"]:
            # 2.删除多余空格
            if pre_process_rule["id"] == "remove_extra_space" and pre_process_rule["enabled"] is True:
                pattern = r'\n{3,}'
                text = re.sub(pattern, '\n\n', text)
                pattern = r'[\t\f\r\x20\ua0\ue00\ue0e\u2000-\u200a\u202f\u205f\uf000]{2,}'
                text = re.sub(pattern, ' ', text)
            # 3.删除多余的URL链接及邮箱
            if pre_process_rule["id"] == 'remove_url_and_email' and pre_process_rule["enabled"] is True:
                pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
                text = re.sub(pattern, '', text)
                pattern = r'https?://[^\s]+'
                text = re.sub(pattern, '', text)

        return text