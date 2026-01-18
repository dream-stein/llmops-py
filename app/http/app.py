#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/12 23:28
@Author  : yps302@163.com
@File    : app.py
"""
import dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http

# 将env加载到环境变量中
dotenv.load_dotenv()

config = Config()

injector = Injector()

app = Http(__name__, conf=config, router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
