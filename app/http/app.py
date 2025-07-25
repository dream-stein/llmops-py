#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/7 15:12
#Author  :Emcikem
@File    :app.py
"""
import dotenv
from flask_login import LoginManager

from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from internal.router import Router
from internal.server import Http
from .module import injector
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
