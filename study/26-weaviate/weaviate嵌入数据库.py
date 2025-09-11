#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/11 23:24
#Author  :Emcikem
@File    :weaviate嵌入数据库.py
"""
import os

import dotenv
import weaviate
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

# client = weaviate.connect_to_weaviate_cloud(
#     cluster_url="giwdf5qksa61wnkzxy40ea.c0.asia-southeast1.gcp.weaviate.cloud",
#     auth_credentials=AuthApiKey("UFZoTXF4NWpKa1JuNHo1S19ZTVQ3TWIvY29SZ1MvMlh3NjBmT2Y4NUVrZ3JlNTNSYmpEMjJJLzZDNS9zPV92MjAw"),
# )
#
# print(1111)

with weaviate.connect_to_weaviate_cloud(
    cluster_url="giwdf5qksa61wnkzxy40ea.c0.asia-southeast1.gcp.weaviate.cloud",
    auth_credentials=AuthApiKey("UFZoTXF4NWpKa1JuNHo1S19ZTVQ3TWIvY29SZ1MvMlh3NjBmT2Y4NUVrZ3JlNTNSYmpEMjJJLzZDNS9zPV92MjAw"),
) as client:
    print(1111)