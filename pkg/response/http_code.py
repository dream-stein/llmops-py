#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/1/18 19:21
@Author  : yps302@163.com
@File    : http_code.py
"""
from enum import Enum


class HttpCode(str, Enum):
    """HTTP基础业务状态码"""
    SUCCESS = "success"  # 成功
    FAIL = "fail"  # 失败
    NOT_FOUND = "not_found"  # 未找到
    UNAUTHORIZED = "unauthorized"  # 未授权 如访问需要登录内容
    FORBIDDEN = "forbidden"  # 无权限 如访问其他人才有权限的内容
    VALIDATION_ERROR = "validation_error"  # 数据验证错误
