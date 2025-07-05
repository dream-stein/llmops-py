#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/4 23:39
#Author  :Emcikem
@File    :google_serper.py
"""
from langchain_core.tools import BaseTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools import GoogleSerperRun
from pydantic import BaseModel, Field

class GoogleSerperArgsSchema(BaseModel):
    """谷歌SerperAPI搜素参数描述"""
    query: str = Field(description="需要检索查询的语句.")

def google_serper(**kwargs) -> BaseTool:
    """谷歌Serp搜素"""
    return GoogleSerperRun(
        name='Google Serper',
        description="这是一个低成本的谷歌搜素API。当你需要搜索时事的时候，可以使用该工具，该工具的输入是一个查询语句",
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper(),
    )