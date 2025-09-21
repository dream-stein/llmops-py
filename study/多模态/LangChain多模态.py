#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import base64
import requests  # 用于下载网络图片
import dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from internal.lib.helper import image_to_base64

dotenv.load_dotenv()

# 初始化模型
# llm = ChatOpenAI(
#     api_key=os.getenv("MOONSHOT_API_KEY"),
#     base_url=os.getenv("MOONSHOT_API_BASE"),
#     model="moonshot-v1-8k-vision-preview"
# )
llm = ChatOpenAI(
    model="deepseek-chat"
)

# 图片来源（可以是本地路径或网络URL）
image_source = "https://inews.gtimg.com/om_bt/ORGPk28hA-V-WHa7XTwJbWYmb-IzAqnlUh2h9YFWvM7GIAA/641"  # 网络URL
# image_source = "/path/to/local/image.png"  # 本地路径

# 转为Base64
try:
    image_base64 = image_to_base64(image_source)
except Exception as e:
    print(f"图片处理失败：{e}")
    exit()

# 构造消息
messages = [
    SystemMessage(content="你是一个多模态助手，能理解图像并回答问题。"),
    HumanMessage(
        content=[
            {"type": "image_url", "image_url": {"url": image_base64}},
            {"type": "text", "text": "详细描述下这个图片"}
        ]
    )
]
content = ""
for chunk in llm.stream(messages):
    content += chunk.content
    print(content)

