#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/25 22:11
#Author  :Emcikem
@File    :faiss.py
"""
import dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

dotenv.load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

db = FAISS.from_texts([
    "笨笨是一只很喜欢睡觉的猫咪",
    "我喜欢在夜晚听音乐，这让我感到放松",
    "喵咪在窗台上打滚，看起来非常可爱",
], embeddings)

print(db.index.ntotal)

db.similarity_search_with_relevance_scores()