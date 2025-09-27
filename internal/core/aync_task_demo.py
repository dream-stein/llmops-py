#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/28 00:10
#Author  :Emcikem
@File    :aync_task_demo.py
"""
#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/27 15:24
#Author  :Emcikem
@File    :sync_task_demo.py
"""
import time

from celery import Celery, shared_task

broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'
app = Celery('sync_task_demo', broker=broker, backend=backend)

@shared_task
def add(a, b):
    time.sleep(1)
    print('myResult' + str(a) + str(b))
    return a + b + 2

res = add.delay(3, 2)
# print(res)

# celery -A sync_task_demo worker -l info
