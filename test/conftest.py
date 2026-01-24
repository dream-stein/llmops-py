#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 20:18
@Author  : yps302@163.com
@File    : conftest.py
"""
import pytest

from app.http.app import app


@pytest.fixture
def client():
    """获取Flask应用的测试应用并返回"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
