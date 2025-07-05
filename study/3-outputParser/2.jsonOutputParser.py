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

dotenv.load_dotenv()

class Joke(BaseModel):
    joke: str = Field(description="回答用户的冷笑话")
    punchline: str = Field(description="这个冷笑话的笑点")

parser = JsonOutputParser(pydantic_object=Joke)
prompt = ChatPromptTemplate.from_template("请根据用户提问回答。\n{format_instructions}\n {query}").partial(format_instructions=parser.get_format_instructions())

llm = ChatOpenAI(model="deepseek-chat")

joke = parser.invoke(llm.invoke(prompt.invoke({"query": "请讲一个关于程序员的冷笑话"})))
print(joke)