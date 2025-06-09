#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/10 00:39
#Author  :Emcikem
@File    :module.py
"""
from flask_sqlalchemy import SQLAlchemy
from injector import Binder, Module, Injector

from internal.extension.database_extension import db

class ExtensionModule(Module):
    """扩展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)

injector = Injector([ExtensionModule])
