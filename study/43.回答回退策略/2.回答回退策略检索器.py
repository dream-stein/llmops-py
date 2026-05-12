#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/10 17:10
@Author  : yps302@163.com
@File    : 2.回答回退策略检索器.py
"""
import os
from typing import List

import dotenv
from langchain_community.embeddings import OpenAIEmbeddings
import weaviate
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.language_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()
class StepBackRetriever(BaseRetriever):
    """回答回退检索器"""
    retriever :BaseRetriever
    llm:BaseLanguageModel

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """根据传递的query执行问题回退并检索"""
        # 1.构建少量提示模板
        example=[
            {"input":"慕课网上有关于AI开发的课程吗？","output":"慕课网上有哪些课程？"},
            {"input":"小明出生于哪个国家？","output":"小明的人生经历是什么样的？"},
            {"input":"司机可以开快车吗？","output":"司机可以做什么？"},
        ]
        example_prompt=ChatPromptTemplate.from_messages([
            ("human","{input}"),
            ("ai","{output}"),
        ])
        few_shot_prompt=FewShotChatMessagePromptTemplate(
            examples=example,
            example_prompt=example_prompt,
        )

        # 2.构建生成问题回退模板
        prompt=ChatPromptTemplate.from_messages([
            ("system","你是一个世界知识的专家。你的任务是回退问题，将问题改述为更一般或者前置问题，这样更容易回答，请参考示例来实现。"),
            few_shot_prompt,
            ("human","{question}"),
        ])

        # 3.构建链应用，生成回退问题，并执行相应检索
        chain=(
            {"question":RunnablePassthrough()}
            |prompt
            |self.llm
            |StrOutputParser()
            |self.retriever
        )

        return  chain.invoke(query)


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

# 2.构建问答回退检索器
step_back_retriever = StepBackRetriever(
    retriever=retriever,
    llm=ChatOpenAI(model="LongCat-Flash-Chat",temperature=0),
)


# 3.检索文档
documents=step_back_retriever.invoke("人工智能会让世界发生翻天覆地的变化吗？")
print(documents)
print(len(documents))