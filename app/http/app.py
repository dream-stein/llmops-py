#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 15:12
#Author  :Emcikem
@File    :app.py
"""
import dotenv
from injector import Injector

from config import Config
from internal.router import Router
from internal.server import Http

# 将env加载到环境变量中
dotenv.load_dotenv()
conf = Config()
injector = Injector()

app = Http(
    __name__,
    conf=conf,
    router=injector.get(Router),
)
if __name__ == "__main__":
    app.run(debug=True)
