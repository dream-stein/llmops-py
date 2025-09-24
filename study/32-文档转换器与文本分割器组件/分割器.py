#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/9/24 22:08
#Author  :Emcikem
@File    :分割器.py
"""
import os
import stat
import tempfile
from typing import Union
from pathlib import Path

import dotenv
from langchain_community.document_loaders import UnstructuredFileLoader, UnstructuredXMLLoader, \
    UnstructuredPowerPointLoader, UnstructuredCSVLoader, UnstructuredHTMLLoader, UnstructuredMarkdownLoader, \
    UnstructuredPDFLoader, UnstructuredExcelLoader, TextLoader
from langchain_core.documents import Document as LCDocument
from qcloud_cos import CosConfig, CosS3Client

dotenv.load_dotenv()

conf = CosConfig(
            Region=os.getenv("COS_REGION"),
            SecretId=os.getenv("COS_SECRET_ID"),
            SecretKey=os.getenv("COS_SECRET_KEY"),
            Token=None,
            Scheme=os.getenv("COS_SCHEME", "https"),
        )
client = CosS3Client(conf)
bucket = os.getenv("COS_BUCKET")


def load_from_file(
        file_path: str,
        return_text: bool = False,
        is_unstructured: bool = True,
) -> Union[list[LCDocument], str]:
    """从本地文件中加载数据，返回LangChain文档列表或者字符串"""
    # 1.获取文件的扩展名
    delimiter = "\n\n"
    file_extension = Path(file_path).suffix.lower()

    # 2.根据不同的文件扩展名去加载不同的加载器
    if file_extension in [".xlsx", ".xls"]:
        loader = UnstructuredExcelLoader(file_path)
    elif file_extension == ".pdf":
        loader = UnstructuredPDFLoader(file_path)
    elif file_extension in [".md", ".markdown"]:
        loader = UnstructuredMarkdownLoader(file_path)
    elif file_extension in [".htm", ".html"]:
        loader = UnstructuredHTMLLoader(file_path)
    elif file_extension == ".csv":
        loader = UnstructuredCSVLoader(file_path)
    elif file_extension in [".ppt", "pptx"]:
        loader = UnstructuredPowerPointLoader(file_path)
    elif file_extension == ".xml":
        loader = UnstructuredXMLLoader(file_path)
    else:
        loader = UnstructuredFileLoader(file_path) if is_unstructured else TextLoader(file_path)

    # 3.返回加载的文档列表或者文本
    return delimiter.join([document.page_content for document in loader.load()]) if return_text else loader.load()


def load(
        key: str,
        return_text: bool = False,
        is_unstructured: bool = True
) -> Union[list[LCDocument], str]:
    """加载传入的upload_file记录，返回Langchain文档列表或者字符串"""
    # 1.创建一个临时的文件夹
    with tempfile.TemporaryDirectory() as temp_dir:
        # 2.构建一个临时文件路径（关键：打印完整路径，确认路径是否正确）
        file_basename = os.path.basename(key)
        file_path = os.path.join(temp_dir, file_basename)

        # -------- 添加调试日志：确认临时文件路径和状态 --------
        print(f"✅ 临时目录路径: {temp_dir}")
        print(f"✅ 临时文件完整路径: {file_path}")
        print(f"✅ 待下载的COS文件Key: {key}")

        # 3.将COS中的文件下载到本地（下载后先检查文件是否存在、大小是否正常）
        client.download_file(bucket, key, file_path)

        # -------- 检查下载后的文件状态 --------
        # ① 确认文件是否存在
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"❌ 临时文件不存在！路径：{file_path}")
        # ② 确认文件大小（排除“空文件”情况，比如下载失败但没报错）
        file_size = os.path.getsize(file_path)
        print(f"✅ 临时文件大小: {file_size} 字节")
        if file_size == 0:
            raise ValueError(f"❌ 临时文件为空！可能是COS下载失败（Key可能错误/权限不足）")
        # ③ （可选）打印前100个字符，确认文件内容是否正常（排除乱码/空白）
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            first_100_chars = f.read(100)
            print(f"✅ 临时文件前100字符: {first_100_chars}")
        os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)  # 给当前用户读、写权限
        # 4.从指定的路径中去加载文件
        return load_from_file(file_path, return_text, is_unstructured)

documents = load('2025/09/24/9fc48a97-5d28-47b0-98d3-21728253d4b6.md', False, True)
# print(documents)

# client.download_file(bucket, '2025/09/24/290aa50c-f432-4fd2-a460-3f4be886447c.md', "/Users/linyongqi/PycharmProjects/llmops-py/study/32-文档转换器与文本分割器组件/uuu.md")


