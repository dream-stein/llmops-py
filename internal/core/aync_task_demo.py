#!/usr/bin/env python  # 注意：原代码“eny”是笔误，需改为“env”
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/27 15:24
#Author  :Emcikem
@File    :sync_task_demo.py
"""
import os
import time
from celery import Celery, shared_task
import dotenv

dotenv.load_dotenv()
# -------------------------- 关键修改：远程Redis带密码配置 --------------------------
# 1. 替换 remote_redis_ip 为实际远程Redis的IP/域名（如 192.168.1.100 或 redis.your-domain.com）
# 2. 替换 your_redis_password 为实际Redis密码（若密码为空，去掉 :your_redis_password 即可）
# 3. 端口 6379 若修改过，需同步替换

# 构建带密码的Redis连接URL
broker = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:6379/0"  # broker用数据库1
backend = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_HOST')}:6379/1"  # backend用数据库2
# ----------------------------------------------------------------------------------

app = Celery('sync_task_demo', broker=broker, backend=backend)

@shared_task
def add(a, b):
    time.sleep(1)
    print(f'myResult: {a + b + 2}')  # 优化打印格式（原代码拼接易出错）
    return a + b + 2

# 测试任务（注意：Celery任务需通过worker执行，直接运行脚本仅提交任务，需启动worker才能执行）
if __name__ == "__main__":
    res = add.delay(3, 2)
    print(f"任务提交成功，任务ID：{res.id}")