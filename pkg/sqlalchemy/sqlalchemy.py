#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/11 00:08
#Author  :Emcikem
@File    :sqlalchemy.py
"""
from contextlib import contextmanager
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy

class SQLAlchemy(_SQLAlchemy):
    """重写Flask-SQLAlchemy中的核心勒，实现自动提交"""

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
