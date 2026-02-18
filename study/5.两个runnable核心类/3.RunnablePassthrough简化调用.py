#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/17 21:39
@Author  : yps302@163.com
@File    : 2.RunnableParallel模拟检索.py
"""

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()


def retrieval(query: str) -> str:
    """一个模拟的检索器函数"""
    print(query, "正在检索")
    return "我是野兽先辈"


# 1.编排prompt
prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答，可以参考对应的上下文进行生成

<context>
{context}
</context>

用户的提问是：{query}""")

# 2.创建llm
llm = ChatOpenAI(model="LongCat-Flash-Lite", )

# 3.创建输出解析器
parser = StrOutputParser()

# 4.编排链
# chain = {
#             "context": retrieval,
#             "query": RunnablePassthrough(),  # 直接使用RunnablePassthrough透传上下文
#         } | prompt | llm | parser  # 在链中使用不需要声明RunnableParallel 管道运算符会进行转换

chain = RunnablePassthrough.assign(context=lambda x: retrieval(x["query"])) | prompt | llm | parser

# 5.调用链
content = chain.invoke({"query": "你好，我是谁"})
print(content)
