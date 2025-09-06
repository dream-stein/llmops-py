#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/5 23:20
#Author  :Emcikem
@File    :conversation_handler.py
"""
from uuid import UUID

from flask_login import current_user
from injector import inject
from dataclasses import dataclass

from internal.schema.conversation_schema import GetConversationMessagesWithPageReq, GetConversationMessagesWithPageResp
from internal.service import ConversationService
from pkg.paginator import PageModel
from pkg.response import validate_error_json, success_json


@inject
@dataclass
class ConversationHandler:
    """会话处理器"""
    conversation_service: ConversationService

    def get_conversation_messages_with_page(self, conversation_id: UUID):
        """根据传递的回话id获取该会话的消息列表分页数据"""
        # 1.提取数据并校验
        req = GetConversationMessagesWithPageReq()
        if req.validate():
            return validate_error_json(req.errors)

        # 2.调用服务获取消息列表
        messages, paginator = self.conversation_service.get_conversation_messages_with_page(
            conversation_id,
            req,
            current_user
        )

        # 3.构建响应结构返回
        resp = GetConversationMessagesWithPageResp(many=True)

        return success_json(PageModel(list=resp.dump(messages), paginator=paginator))