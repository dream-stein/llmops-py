#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/10 00:39
#Author  :Emcikem
@File    :module.py
"""
from pkg.sqlalchemy import SQLAlchemy
from injector import Binder, Module, Injector
from flask_migrate import Migrate
from internal.extension.migrate_extension import migrate
from internal.extension.redis_extension import redis_client
from internal.extension.database_extension import db
from redis import Redis
from flask_login import LoginManager
from internal.extension.login_extension import login_manager

class ExtensionModule(Module):
    """扩展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
        binder.bind(Redis, to=redis_client)
        binder.bind(LoginManager, to=login_manager)

injector = Injector([ExtensionModule])
