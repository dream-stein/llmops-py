#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/4 17:11
@Author  : yps302@163.com
@File    : 2.FileSystemBlobLoader.py
"""
from langchain_community.document_loaders import FileSystemBlobLoader

loader=FileSystemBlobLoader(".",show_progress=True)

for blob in loader.yield_blobs():
    print(blob.source)