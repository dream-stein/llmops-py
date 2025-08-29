#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 15:12
#Author  :Emcikem
@File    :app.py
"""
import os
import sys
import dotenv
from flask_login import LoginManager

# 将项目根目录加入到sys.path，确保以脚本运行时能找到顶级包
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from internal.router import Router
from internal.server import Http
from app.http.module import injector
from internal.middleware import Middleware

# 1.将env加载到环境变量中
dotenv.load_dotenv()

# 2.构建LLMOps项目配置
conf = Config()

app = Http(
    __name__,
    conf=conf,
    db=injector.get(SQLAlchemy),
    migrate=injector.get(Migrate),
    router=injector.get(Router),
    middleware=injector.get(Middleware),
    login_manager=injector.get(LoginManager),
)

celery = app.extensions["celery"]

if __name__ == "__main__":
    app.run(debug=True)
