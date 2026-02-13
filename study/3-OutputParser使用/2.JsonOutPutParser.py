#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/2/13 17:08
@Author  : yps302@163.com
@File    : 2.JsonOutPutParser.py
"""
import dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic.v1 import BaseModel, Field

dotenv.load_dotenv()


# 1.创建一个JSON数据结构
class Joke(BaseModel):
    # 冷笑话
    joke: str = Field(description="回答用户的冷笑话")
    # 冷笑话的笑点
    punchline: str = Field(description="这个冷笑话的笑点")


# 2.创建字符串解析器
parser = JsonOutputParser(pydantic_object=Joke)
print(parser.get_format_instructions())

# 3.编排提示模板
prompt = ChatPromptTemplate.from_template("请根据用户的提问进行回答。\n {format_instruction} \n {query}").partial(
    format_instruction=parser.get_format_instructions)

print(prompt)

# 4.构建大语言模型
llm = ChatOpenAI(model="LongCat-Flash-Lite", )

# 5.调用llm生成结果和解析
joke = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于程序员的冷笑话"})))
print(type(joke))
print(joke.get("punchline"))
print(joke)
