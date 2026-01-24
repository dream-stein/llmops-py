#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/24 20:05
@Author  : yps302@163.com
@File    : test_app_handler.py
"""

import pytest

from pkg.response import HttpCode


class TestAppHandler:
    """app控制器的测试类"""

    """在课程的基础上 把响应校验也参数化了"""

    @pytest.mark.parametrize("user_query,expected_code", [
        (None, HttpCode.VALIDATION_ERROR),
        ("你好，你是谁？", HttpCode.SUCCESS),
    ])
    def test_completion(self, user_query, expected_code, client):
        resp = client.post("/app/completion", json={"query": user_query})
        assert resp.status_code == 200
        assert resp.json.get("code") == expected_code
        print("响应：", resp.json)
