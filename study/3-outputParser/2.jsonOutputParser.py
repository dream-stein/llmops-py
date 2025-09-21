#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/6/18 00:04
#Author  :Emcikem
@File    :1.StrOutputParser.py
"""
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import JsonOutputParser

# 加载环境变量（包含API密钥等配置）
dotenv.load_dotenv()

# 定义输出模型：明确要求生成3个问题，每个不超过50字符
class SuggestedQuestions(BaseModel):
    questions: list[str] = Field(
        description="人类最可能会问的三个问题，每个问题不超过50个字符，以列表形式呈现"
    )

human = "什么是LLMOps?"
answer = """关于LLMOps的概念，目前我无法提供详细的专业解释，因为相关的知识库检索工具暂时不可用。

LLMOps（Large Language Model Operations）通常指的是大型语言模型的运维和管理流程，包括模型的部署、监控、版本控制、性能优化等环节。这是机器学习运维（MLOps）在大型语言模型领域的具体应用。

如果您需要更详细和准确的信息，建议您：

查阅相关的技术文档或专业书籍
参考AI/机器学习领域的权威网站和博客
咨询专业的AI工程师或研究人员
我主要专注于应用创建和基础的问题解答，对于这种专业的技术概念，建议您通过其他专业渠道获取更全面的信息。"""

histories = f"Human: {human}\nAI: {answer}"

# 创建解析器，关联到定义的模型
parser = JsonOutputParser(pydantic_object=SuggestedQuestions)

SUGGESTED_QUESTIONS_TEMPLATE = """你需要根据用户的输入，生成3个最可能被问到的相关问题。
要求：
1. 每个问题不超过50个字符
2. 输出必须符合以下JSON格式（由模型定义）：
{format_instructions}
3. 问题需与用户输入内容紧密相关"""

# 构建提示词模板：明确任务目标和格式要求
prompt = ChatPromptTemplate.from_messages([
    ("system", SUGGESTED_QUESTIONS_TEMPLATE),
    ("human", "{histories}")
]).partial(format_instructions=parser.get_format_instructions())

# 初始化模型（使用DeepSeek）
llm = ChatOpenAI(
    model="deepseek-chat",
    temperature=0
)

# 构建处理链：提示词 → 模型 → 解析器
chain = prompt | llm | parser

# 执行生成（以"程序员冷笑话"为例）
result = chain.invoke({"histories": histories})

# 输出结果
print(result)