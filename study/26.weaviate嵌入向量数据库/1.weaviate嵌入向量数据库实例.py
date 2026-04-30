#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/30 17:18
@Author  : yps302@163.com
@File    : 1.weaviate嵌入向量数据库实例.py
"""
import os

import dotenv
import weaviate
from langchain_openai import OpenAIEmbeddings
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey
from weaviate.collections.classes.filters import Filter

dotenv.load_dotenv()

# 原始文本与元数据
texts = [
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松。",
    "猫咪在窗台上打盹，看起来非常可爱。",
    "学习新技能是每个人都应该追求的目标。",
    "我最喜欢的食物是意大利面，尤其是番茄酱的那种。",
    "昨晚我做了一个奇怪的梦，梦见自己在太空飞行。",
    "我的手机突然关机了，让我有些焦虑。",
    "阅读是我每天都会做的事情，我觉得很充实。",
    "他们一起计划了一次周末的野餐，希望天气能好。",
    "我的狗喜欢追逐球，看起来非常开心。",
]
metadatas = [
    {"page": 1},
    {"page": 2},
    {"page": 3},
    {"page": 4},
    {"page": 5},
    {"page": 6, "account_id": 1},
    {"page": 7},
    {"page": 8},
    {"page": 9},
    {"page": 10},
]

# 1.连接向量数据库
client= weaviate.connect_to_wcs(
    cluster_url="1zbpy1imtp8vrbpdkpzfg.c0.asia-southeast1.gcp.weaviate.cloud",
    auth_credentials=AuthApiKey("THg0RmM3Vy9WdmtWRXFNT182citCZTNobXZYQy94V0V1ZTZwS3ZWRy9kN3l2bDdXNDVXSW00Q0lyWlR3PV92MjAw"),
)

embedding = OpenAIEmbeddings(
    model="BAAI/bge-m3",
    # 使用 os.getenv 读取，即使源码要求 SecretStr，这里直接传字符串即可
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL")
)

# 2.创建向量数据库实例
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemo",
    text_key="text",
    embedding=embedding,
)

# # 3.添加数据
# ids=db.add_texts(texts,metadatas)
# print(ids)

# 4.执行搜索
# filters = Filter.by_property("page").greater_or_equal(5)
# print(db.similarity_search_with_score("笨笨是一只猫咪",filters=filters))
# print(db.similarity_search(
# query="笨笨是一只很喜欢睡觉的猫咪", # 有些模型加前缀效果更好
#     k=3,
#     alpha=0 # 0.5 表示语义和字面各占一半权重
# ))
#
# collection = client.collections.get("DatasetDemo")
# # 直接按顺序查前 10 条，不带向量搜索
# objs = collection.query.fetch_objects(limit=10)
# for o in objs.objects:
#     print(f"ID: {o.uuid}, Content: {o.properties.get('text')}")
#

retriever =db.as_retriever()
print(retriever.invoke(("笨笨")))