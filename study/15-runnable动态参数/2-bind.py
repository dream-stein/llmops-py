#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/22 19:02
#Author  :Emcikem
@File    :2-bind.py
"""
from langchain_core.runnables import RunnableLambda


def get_weather(location: str, unit: str) -> str:
    print(location)
    print(unit)
    return f"{location}.{unit}"

get_weather_runnable = RunnableLambda(get_weather).bind(unit="摄氏度")
resp = get_weather_runnable.invoke({"location": "广州"})
print(resp)