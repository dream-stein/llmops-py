#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/12 23:17
@Author  : yps302@163.com
@File    : http.py
"""
import os

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from internal.excepiton import CustomException
from internal.router import Router
from pkg.response import Response, json, HttpCode
from pkg.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)


class Http(Flask):
    """Http服务引擎"""

    def __init__(
            self,
            *args,
            conf: Config,
            db: SQLAlchemy,
            migrate: Migrate,
            router: Router,
            **kwargs):
        # 1.调用父类构造函数初始化
        super().__init__(*args, **kwargs)

        # 2.初始化应用配置
        self.config.from_object(conf)

        # 3.注册绑定异常错误处理
        self.register_error_handler(Exception, self._register_error_handler)

        # 4.初始化flask扩展
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migration")
        # 5.解决前后端跨域问题
        CORS(self, resources={
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
                # "methods": ["GET", "POST"],
                # "allow_headers": ["Content-Type"],
            }
        })
        # 5.注册应用路由
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        # 1.判断是不是自定义异常 如果是就提取message和code
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {},
            ))
        if self.debug or os.getenv('FLASK_ENV') == 'development':
            raise error
        # 2.如果不是 则可能是程序或数据库异常 也可以提取异常设置为fail
        return json(Response(
            code=HttpCode.FAIL,
            message=str(error),
            data={},
        ))
