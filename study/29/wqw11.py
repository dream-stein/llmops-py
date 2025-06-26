#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/27 00:32
#Author  :Emcikem
@File    :wqw11.py
"""

import nltk
import requests

# 测试NLTK服务器可访问性
try:
    response = requests.get("https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml", timeout=5)
    print("可以访问NLTK服务器" if response.status_code == 200 else "服务器不可用")
except:
    print("网络连接失败，请检查代理或防火墙设置")

# 尝试使用国内镜像
nltk.set_proxy("http://mirrors.aliyun.com/nltk_data/")
nltk.download('punkt')