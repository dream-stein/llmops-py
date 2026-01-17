#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/11 17:13
@Author  : yps302@163.com
@File    : app_handler.py
"""
from flask import request
from openai import OpenAI


class APPHandler:
    """应用控制器"""

    def ping(self):
        return {"ping": "pong"}

    def completion(self):
        """聊天接口"""

        # 1.提取从接口中获取的输入，POST
        query = request.json.get("query")

        # 2.构建OPENAI客户端，并发起请求
        client = OpenAI(
            api_key="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",
            base_url="https://openrouter.ai/api/v1",
        )
        # 3.得到请求响应，将OPENAI的响应传给前端
        completion = client.chat.completions.create(
            model="xiaomi/mimo-v2-flash:free",
            messages=[
                {"role": "system", "content": "你是OpenAI开发的聊天机器人，请根据用户的输入回复对应的信息"},
                {"role": "user", "content": query},
            ]
        )
        content = completion.choices[0].message.content
        return content
