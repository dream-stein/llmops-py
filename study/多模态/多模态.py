#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/21 21:28
#Author  :Emcikem
@File    :多模态.py.py
"""
import os
import base64

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),
    base_url=os.getenv("MOONSHOT_API_BASE"),
)

# 使用提供的实际图片路径
image_path = "/Users/linyongqi/PycharmProjects/llmops-py/study/多模态/cv.png"

with open(image_path, "rb") as f:
    image_data = f.read()

# 提取图片扩展名并移除前面的点号
image_ext = os.path.splitext(image_path)[1][1:]
# 生成base64格式的image_url
image_url = f"data:image/{image_ext};base64,{base64.b64encode(image_data).decode('utf-8')}"

completion = client.chat.completions.create(
    model="moonshot-v1-8k-vision-preview",
    messages=[
        {"role": "system", "content": "你是 Kimi。"},
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
                {
                    "type": "text",
                    "text": "请描述图片的内容。",
                },
            ],
        },
    ],
)

print(completion.choices[0].message.content)
