#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/1 20:32
@Author  : yps302@163.com
@File    : migrate_extension.py
"""
from flask_migrate import Migrate

migrate = Migrate(compare_server_default=True)
