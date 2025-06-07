#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 13:51
#Author  :Emcikem
@File    :app_handler.py
"""
import os

from flask import request
from openai import OpenAI

class AppHandler:
    """应用控制器"""

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
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

        return content

    def ping(self):
        return {"ping": "pong"}