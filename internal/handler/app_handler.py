#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/11 17:13
@Author  : yps302@163.com
@File    : app_handler.py
"""
import uuid
from dataclasses import dataclass

from injector import inject
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from internal.excepiton import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class APPHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用成功创建,id为{app.id}")

    def get_app(self, id: uuid.UUID):
        app = self.app_service.get_app(id)
        return success_message(f"成功获取应用，名字是{app.name}")

    def update_app(self, id: uuid.UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是{app.name}")

    def delete_app(self, id: uuid.UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，ID为{app.id}")

    def ping(self):
        raise FailException("114514")
        # return {"ping": "pong"}

    def completion(self):
        """聊天接口"""

        # 1.提取从接口中获取的输入，POST

        # 声明式验证校验输入
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)
        # query = request.json.get("query")

        prompt = ChatPromptTemplate.from_template("{query}")
        # 2.构建OPENAI客户端，并发起请求
        llm = ChatOpenAI(model="LongCat-Flash-Lite")
        # 3.得到请求响应，将OPENAI的响应传给前端
        ai_message = llm.invoke(prompt.invoke({"query": req.query.data}))

        parser = StrOutputParser()

        # 4.解析响应内容
        content = parser.invoke(ai_message)

        return success_json({"content": content})
