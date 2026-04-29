#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/4/28 16:39
@Author  : yps302@163.com
@File    : 2.configurable_fields替换提示词.py
"""
from langchain.chains.qa_with_sources.stuff_prompt import template
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField

prompt=PromptTemplate.from_template("请写一篇关于{subject}主题的冷笑话").configurable_fields(
    template=ConfigurableField(id="prompt_template",),
)


content=prompt.invoke(
    {"subject":"程序员"},
    config={"configurable":{"prompt_template":"请写一篇关于{subject}主题的藏头诗"}}
).to_string()
print(content)

print("==============")

content=prompt.invoke(
    {"subject":"程序员"},
).to_string()
print(content)

