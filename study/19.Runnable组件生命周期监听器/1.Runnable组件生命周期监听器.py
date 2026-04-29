#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/29 16:31
@Author  : yps302@163.com
@File    : 1.Runnable组件生命周期监听器.py
"""
import time

from langchain_core.runnables import RunnableLambda, RunnableConfig
from langchain_core.tracers.schemas import Run

def on_start(run_obj:Run,config:RunnableConfig)->None:
    print("on_start")
    print("run_obj:",run_obj)
    print("config:",config)
    print("==============")

def on_end(run_obj:Run,config:RunnableConfig)->None:
    print("on_end")
    print("run_obj:",run_obj)
    print("config:",config)
    print("==============")

def on_error(run_obj:Run,config:RunnableConfig)->None:
    print("on_error")
    print("run_obj:",run_obj)
    print("config:",config)
    print("==============")


runnable = RunnableLambda(lambda x: time.sleep(x)).with_listeners(
    on_start=on_start,
    on_end=on_end,
    on_error=on_error,
)
chain = runnable

chain.invoke(2,config={"configurable":{"name":"小明"}})