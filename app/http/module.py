#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/25 16:53
@Author  : yps302@163.com
@File    : module.py
"""
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder

from internal.extension.database_extension import db


class ExtensionModule(Module):
    """拓展模块的依赖注入"""

    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, to=db)
