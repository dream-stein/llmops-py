#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/10 11:11
@Author  : yps302@163.com
@File    : 1.问题分解策略.py
"""
import os
from json import dumps, loads
from operator import itemgetter
from typing import List

import dotenv
import weaviate
from langchain.retrievers import MultiQueryRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

def format_qa_pairs(question:str, answer:str):
    """格式化传递的问题+答案为单个字符串"""
    return f"Question: {question}\nAnswer: {answer}\n\n".strip()

# 1.定义分解子问题的prompt
decomposition_prompt=ChatPromptTemplate.from_template(
    "你是一个乐于助人的AI助理，可以针对一个输入问题生成多个相关的子问题。\n"
    "目标是将输入问题分解成一组可以独立回答的子问题或者子任务。\n"
    "生成与以下问题相关的多个搜索查询：{question}\n"
    "并使用换行符进行分割，输出（三个子问题/子查询）："
)

# 2.构建分解问题链
decomposition_chain=(
    {"question":RunnablePassthrough()}
    |decomposition_prompt
    |ChatOpenAI(model="LongCat-Flash-Chat",temperature=0)
    |StrOutputParser()
    |(lambda x:x.strip().split("\n"))
)

# 3.构建向量数据库和检索器
client = weaviate.connect_to_wcs(
    cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
    auth_credentials=AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
)

embedding = OpenAIEmbeddings(
    model="Qwen/Qwen3-Embedding-8B",
    # 使用 os.getenv 读取，即使源码要求 SecretStr，这里直接传字符串即可
    api_key=os.getenv("SILICONFLOW_API_KEY"),
    base_url=os.getenv("SILICONFLOW_BASE_URL")
)

db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemoQwen1",
    text_key="text",
    embedding=embedding,
)
retriever = db.as_retriever(search_type="mmr")

# 4.执行提问获取子问题
question="关于LLMOps应用配置的文档有哪些"
sub_questions=decomposition_chain.invoke(question)

# 5.构建迭代问答链：提示模板+链
prompt=ChatPromptTemplate.from_template("""这是你需要回答的问题：
---
{question}
---
这是所有可用的背景问题和答案对：
---
{qa_pairs}
---

这是与问题相关的额外背景信息：
---
{context}
---
""")
chain=(
    {
        "question":itemgetter("question"),
        "qa_pairs":itemgetter("qa_pairs"),
        "context":itemgetter("question")|retriever,
    }
    |prompt
    |ChatOpenAI(model="LongCat-Flash-Chat",temperature=0)
    |StrOutputParser()
)

# 6.循环遍历所有子问题进行检索并获取答案
qa_pairs=""
for sub_question in sub_questions:
    answer=chain.invoke({"question":sub_question,"qa_pairs":qa_pairs,})
    qa_pair=format_qa_pairs(question=sub_question,answer=answer)
    qa_pairs+="\n---\n"+qa_pair
    print(f"问题：{sub_question}")
    print(f"答案：{answer}")

