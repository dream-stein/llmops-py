#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 15:02
#Author  :Emcikem
@File    :FIleSystemBlobLoader.py
"""
from langchain_community.document_loaders.blob_loaders import FileSystemBlobLoader

loader = FileSystemBlobLoader(".", show_progress=True)

for blob in loader.yield_blobs():
    print(blob.source)
    print(blob.as_string())