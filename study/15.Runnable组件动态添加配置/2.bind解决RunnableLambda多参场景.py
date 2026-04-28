#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/28 15:32
@Author  : yps302@163.com
@File    : 2.bind解决RunnableLambda多参场景.py
"""
import random

from langchain_core.runnables import RunnableLambda
from sqlalchemy.ext.asyncio import result


def get_weather(location:str,unit:str)->str:
    """根据传入位置+温度单位获取温度信息"""
    print("location:",location)
    print("unit:",unit)
    return f"{location}天气为{random.randint(24,40)}{unit}"

# get_weather_runnable=RunnableLambda(get_weather)
# 直接这么传会报错 因为invoke会把内容全部传入第一个参数
# resp=get_weather_runnable.invoke({"location":"上海","unit":"摄氏度"})

get_weather_runnable=RunnableLambda(get_weather).bind(unit="摄氏度")
print(get_weather_runnable.kwargs)
resp=get_weather_runnable.invoke("广州")

print(resp)