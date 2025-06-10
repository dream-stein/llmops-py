#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 13:51
#Author  :Emcikem
@File    :app_handler.py
"""
from dataclasses import dataclass

from flask import request, jsonify
from injector import inject
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message
import os

@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经创建成功，id为{app.id}")

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        query = request.json.get("query")

        # 2.构建OpenAI客户端，并发起请求
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )

        # 3.得到请求相应，然后将OpenAPI的相应传递给前端
        completion = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是openai开发的聊天机器人，请根据用户输入回复对应的信息"},
                {"role": "user", "content": query},
            ]
        )

        content = completion.choices[0].message.content

        return success_json({"content": content})

    def ping(self):
        raise FailException("数据未找到")
        # return {"ping": "pong"}