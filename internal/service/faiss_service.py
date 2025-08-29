#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/8/23 21:25
#Author  :Emcikem
@File    :faiss_service.py
"""
import os.path

from injector import inject
from langchain_core.tools import BaseTool, tool
from pydantic import BaseModel, Field
from typing import Any

from internal.lib.helper import combine_documents
from internal.service import EmbeddingsService
from internal.core.agent.entities.agent_entity import DATASET_RETRIEVAL_TOOL_NAME


@inject
class FaissService:
    """Faiss向量数据库服务"""
    faiss: Any
    embeddings_service: EmbeddingsService

    def __init__(self, embeddings_service: EmbeddingsService):
        """构造函数，完成Faiss向量数据库的初始化"""
        self.embeddings_service = embeddings_service

        # 2.获取internal路径并计算本地数据库的实际路径
        internal_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        faiss_vector_store_path = os.path.join(internal_path, "core", "vector_store")

        # 3.初始化faiss向量数据库（延迟导入，避免启动时依赖faiss）
        try:
            from langchain_community.vectorstores import FAISS
            self.faiss = FAISS.load_local(
                folder_path=faiss_vector_store_path,
                embeddings=self.embeddings_service.embeddings,
                allow_dangerous_deserialization=True,
            )
        except Exception:
            # 启动阶段未安装faiss或相关依赖时，先置空，实际调用工具时再报错
            self.faiss = None

    def convert_faiss_to_tool(self) -> BaseTool:
        """将Faiss向量数据库检索器转换成LangChain工具"""
        # 1.将Faiss向量数据库转换成检索器
        if self.faiss is None:
            # 延迟失败，提示需要安装依赖
            raise RuntimeError("FAISS 向量数据库未初始化，请安装所需依赖并构建本地索引后重试")

        retrieval = self.faiss.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 5, "fetch_k": 20}
        )

        # 2.构建检索链，并将检索的结果合并成字符串
        search_chain = retrieval | combine_documents

        class DatasetRetrievalInput(BaseModel):
            """知识库检索工具输入结构"""
            query: str = Field(description="知识库检索query语句，类型为字符串")

        @tool(DATASET_RETRIEVAL_TOOL_NAME, args_schema=DatasetRetrievalInput)
        def dataset_retrieval(query: str) -> str:
            """如果需要检索扩展的知识库内容，当你觉得医护的提问超过你的知识库范围时，可以尝试调用该工具，输入为搜索query语句，返回数据为搜索内容字符串"""
            return search_chain.invoke(query)

        return dataset_retrieval