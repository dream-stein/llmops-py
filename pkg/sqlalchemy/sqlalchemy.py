#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/1 15:39
@Author  : yps302@163.com
@File    : sqlalchemy.py
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):
    """重写flask_sqlalchemy中的核心类，实现自动提交"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise Exception
