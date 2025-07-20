#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/20 21:14
#Author  :Emcikem
@File    :conversation_service.py
"""
from injector import inject
from dataclasses import dataclass

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from internal.entity.conversation_entity import SUMMARIZER_TEMPLATE
from internal.service import BaseService
from pkg.sqlalchemy import SQLAlchemy
from langchain_core.prompts import ChatPromptTemplate


@inject
@dataclass
class ConversationService(BaseService):
    """会话服务"""
    db: SQLAlchemy

    @classmethod
    def summary(cls, human_message: str, ai_message: str, old_summary: str = "") -> str:
        """根据传递的人类消息、AI消息还有原始的摘要消息总结生成一段新的摘要"""
        # 1.创建prompt
        prompt = ChatPromptTemplate.from_template(SUMMARIZER_TEMPLATE)

        # 2.构建大语言模型实例，并且将大语言模型的温度降低，降低幻觉的概率
        llm = ChatOpenAI(model="deepseek-chat", temperature=0.5)

        # 3.构建链应用
        summary_chain = prompt | llm | StrOutputParser()

        # 4.调用链并获取新摘要消息
        new_summary = summary_chain.invoke({
            "summary": old_summary,
            "new_lines": f"Human: {human_message}\nAI: {ai_message}",
        })

        return new_summary