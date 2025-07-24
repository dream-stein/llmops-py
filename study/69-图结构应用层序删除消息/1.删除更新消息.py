#!/usr/bin/eny python
# -*- coding: utf-8 -*-
"""
@Time    :2025/7/25 00:17
#Author  :Emcikem
@File    :1.删除更新消息.py
"""
from typing import Any

from langchain_core.messages import RemoveMessage, AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
import dotenv
from langgraph.graph import MessagesState, StateGraph

dotenv.load_dotenv()

llm = ChatOpenAI(model="deepseek-chat")

def chatbot(state: MessagesState, config: RunnableConfig) -> Any:
    """聊天机器人"""
    return {"messages": [llm.invoke(state["messages"])]}

def delete_human_message(state: MessagesState, config: RunnableConfig) -> Any:
    """删除人类消息节点"""
    human_message = state["messages"][-1]
    return {"messages": [RemoveMessage(id=human_message.id)]}

def update_human_message(state: MessagesState, config: RunnableConfig) -> Any:
    """更新人类消息节点"""
    human_message = state["messages"][-1]
    return {"messages": [AIMessage(id=human_message.id, content="更新后的AI消息" + human_message.content)]}


# 1.创建图构建器
graph_builder = StateGraph(MessagesState)

# 2.添加节点
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("update_human_message", update_human_message)

# 3.添加边
graph_builder.set_entry_point("chatbot")
graph_builder.add_edge("chatbot", "update_human_message")
graph_builder.set_finish_point("update_human_message")

# 4.编译图
graph = graph_builder.compile()

# 5.调页图应用程序
print(graph.invoke({"messages": [("human", "你好，你是？")]}))