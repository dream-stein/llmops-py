#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/22 22:20
#Author  :Emcikem
@File    :加密.py
"""

def main(params):
    import json
    import hashlib
    import base64
    import urllib.parse
    # 1.将RequestData和ApiKey拼接
    request_data = {"LogisticCode": f"{params.get('logistic_code')}"}
    api_key = "060f080b-a10a-4f0b-a76d-8d0c71ccd31e"
    combined_data = json.dumps(request_data) + api_key

    # 2.MD5加密并转换成小写
    md5_hash = hashlib.md5(combined_data.encode("utf-8")).hexdigest()

    # 3.Base64编码
    base64_encoded = base64.b16encode(md5_hash.encode("utf-8")).decode("utf-8")

    # 4.URL编码
    url_encoded = urllib.parse.quote(base64_encoded)
    return {
        "RequestType": 8002,
        "EBusinessId": 1897913,
        "DataSign": url_encoded,
        "RequestData": urllib.parse.quote(json.dumps(request_data)),
    }
