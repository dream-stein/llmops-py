#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/8 16:54
@Author  : yps302@163.com
@File    : 4.复用提示模板.py
"""
from langchain_core.prompts import PromptTemplate, PipelinePromptTemplate

full_template = PromptTemplate.from_template("""{instruction}

{example}


{start}
""")

# 描述模板
instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

# 示例模板
example_prompt = PromptTemplate.from_template("""下面是一个交互例子：

Q：{example_question}
A：{example_answer}""")

# 开始模板
start_prompt = PromptTemplate.from_template("""现在你是一个真实的人，请回答用户的问题：

Q：{input}
A：""")

pipeline_prompts = [
    ("instruction", instruction_prompt),
    ("example", example_prompt),
    ("start", start_prompt),
]

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_template,
    pipeline_prompts=pipeline_prompts,
)
print(pipeline_prompt.invoke({
    "person": "雷军",
    "example_question": "你最喜欢的汽车是什么？",
    "example_answer": "小米SU7",
    "input": "你最喜欢的手机是什么？"
}
).to_string())
