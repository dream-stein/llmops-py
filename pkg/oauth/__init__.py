#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/13 12:25
#Author  :Emcikem
@File    :__init__.py.py
"""
from .oauth import OAuthUserInfo, OAuth
from .github_oauth import GithubOAuth

__all__ = ["OAuth", "OAuthUserInfo", "GithubOAuth"]