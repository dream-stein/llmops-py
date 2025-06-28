#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/28 11:38
#Author  :Emcikem
@File    :office文档加载器.py
"""
from langchain_community.document_loaders import (
UnstructuredExcelLoader,
UnstructuredWordDocumentLoader,
UnstructuredPowerPointLoader,
)

excel_loader = UnstructuredExcelLoader("./员工考勤表.xlsx", mode="elements")

excel_documents = excel_loader.load()
print(excel_documents)
print(len(excel_documents))
print(excel_documents[0].metadata)

word_loader = UnstructuredWordDocumentLoader("./喵喵.docx")

word_documents = word_loader.load()
print(word_documents)
print(len(word_documents))
print(word_documents[0].metadata)

ppt_loader = UnstructuredPowerPointLoader("./章节介绍.pptx")
ppt_documents = ppt_loader.load()
print(ppt_documents)
print(len(ppt_documents))
print(ppt_documents[0].metadata)