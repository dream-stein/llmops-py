#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/22 00:48
#Author  :Emcikem
@File    :google_serper_tool.py
"""
import dotenv
from langchain_community.tools import GoogleSerperRun
from pydantic import Field, BaseModel  # 使用 Pydantic v2 的导入方式
from langchain_community.utilities import GoogleSerperAPIWrapper

dotenv.load_dotenv()

class GoogleSerperArgsSchema(BaseModel):
    query: str = Field(description="执行谷歌搜素的查询语句")

google_serper = GoogleSerperRun(
    name="google-serper",
    description=(
        "一个低成本的谷歌搜素API",
        "用于查询时事相关问题，返回谷歌搜索结果。",
        "该工具传递的参数是搜素查询语句。"
    ),
    args_schema=GoogleSerperArgsSchema,
    api_wrapper=GoogleSerperAPIWrapper(),
)

print(google_serper.invoke("马路上的世界记录是什么"))