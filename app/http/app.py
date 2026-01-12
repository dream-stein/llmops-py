#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/12 23:28
@Author  : yps302@163.com
@File    : app.py
"""
from injector import Injector

from internal.router import Router
from internal.server import Http

injector = Injector()
app = Http(__name__, router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
