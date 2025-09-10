#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/11 00:02
#Author  :Emcikem
@File    :weaviate.py
"""
import os

from langchain.vectorstores import weaviate
from langgraph_sdk import Auth

# Best practice: store your credentials in environment variables
weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

print(client.is_ready())