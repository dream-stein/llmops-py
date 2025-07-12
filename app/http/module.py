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

class ExtensionModule(Module):
    """扩展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)
        binder.bind(Redis, to=redis_client)

injector = Injector([ExtensionModule])
