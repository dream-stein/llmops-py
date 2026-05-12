#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/7 17:06
@Author  : yps302@163.com
@File    : 1.RAG多查询结果融合策略.py
"""
import os
from json import dumps, loads
from typing import List

import dotenv
import weaviate
from langchain.retrievers import MultiQueryRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from weaviate.auth import AuthApiKey

dotenv.load_dotenv()

def rrf(results:List[List])->List:
    """RRF算法 对传递的二层嵌套文档列表进行去重合并，并返回排名高的数据"""
    # 1.定义一个变量存储每个文档的得分信息
    fused_result={}

    # 2.循环两层获取每一个文档信息
    for docs in results:
        for rank,doc in enumerate(docs):
            # 3.使用dump函数将类实例转换为字符串
            doc_str=dumps(doc)
             # 4.判断下该文档的字符串是否已经计算过得分
            if doc_str not in fused_result:
                fused_result[doc_str]=0
            # 5.计算新得分
            fused_result[doc_str]+=1/(rank+60)

    # 6.执行排序操作，获取相应的数据，使用降序
    reranked_result=[
        (loads(doc),score)
        for doc,score in sorted(fused_result.items(),key=lambda x:x[1],reverse=True)
    ]

    return reranked_result

class RAGFusionRetriever(MultiQueryRetriever):
    """RAG多查询结果融合策略检索器"""
    k:int=4

    def retrieve_documents(
        self, queries: List[str], run_manager: CallbackManagerForRetrieverRun
    ) -> List[List]:
        """重写检索文档函数，返回值变成嵌套列表"""
        documents = []
        for query in queries:
            docs = self.retriever.invoke(
                query, config={"callbacks": run_manager.get_child()}
            )
            documents.append(docs)
        return documents

    def unique_union(self, documents: List[List]) -> List[Document]:
        """使用RRF算法：完全基于'代号'进行计算"""
        fused_result = {}  # 记录 [代号 -> 得分]
        doc_map = {}  # 记录 [代号 -> 文档实体]

        for docs in documents:
            for rank, doc in enumerate(docs):

                # 1. 分配/获取代号 (Code)
                # 如果你的 metadata 里有数据库生成的唯一 id，直接用：doc.metadata.get('id')
                # 如果没有，我们可以用 Python 的 hash() 函数给内容生成一个极其轻量的数字代号
                doc_code = hash(doc.page_content)

                # 2. 存入映射表 (只在第一次遇到时保存实体)
                if doc_code not in doc_map:
                    doc_map[doc_code] = doc
                    fused_result[doc_code] = 0

                # 3. 只对“代号”进行纯数学计算
                fused_result[doc_code] += 1 / (rank + 60)

        # 4. 对代号的分数进行排序
        sorted_codes = sorted(fused_result.items(), key=lambda x: x[1], reverse=True)

        # 5. 计算完事后，拿着排好序的代号，去“仓库”里把真正的文档提取出来交差
        return [doc_map[code] for code, score in sorted_codes[:self.k]]

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

# 2.创建向量数据库实例
db = WeaviateVectorStore(
    client=client,
    index_name="DatasetDemoQwen1",
    text_key="text",
    embedding=embedding,
)
retriever = db.as_retriever(search_type="mmr")

rag_fusion_retriever = RAGFusionRetriever.from_llm(
    retriever=retriever,
    llm=ChatOpenAI(model="LongCat-Flash-Chat", temperature=0),
    include_original=True,
)


docs = rag_fusion_retriever.invoke("关于LLMOps应用配置的文档有哪些")
print(docs)
print(len(docs))
