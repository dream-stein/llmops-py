#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2026/5/6 16:05
@Author  : yps302@163.com
@File    : 1.问答转换器.py
"""
import asyncio
import json
from typing import List

import dotenv

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

class SimpleQATransformer:
    """使用当前 LangChain 栈实现一个简化版问答转换器"""

    def __init__(self, model: str = "LongCat-Flash-Chat"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = ChatPromptTemplate.from_template(
            """请根据给定文档内容，提取 5 组高质量的问答对，并且严格输出 JSON。

要求：
1. 问题必须可以仅依据文档回答。
2. 答案必须简洁、准确，不要编造。
3. 保留文档中的关键信息，比如日期、人物、职责、联系方式、活动安排。
4. 输出语言使用中文。
5. 只返回 JSON，不要返回解释说明、markdown 代码块或额外文本。

输出格式如下：
[
  {{"question": "问题1", "answer": "答案1"}},
  {{"question": "问题2", "answer": "答案2"}}
]

文档内容如下：
<document>
{page_content}
</document>"""
        )

    async def atransform_documents(self, documents: List[Document]) -> List[Document]:
        transformed_documents = []
        chain = self.prompt | self.llm | StrOutputParser()

        for document in documents:
            result = await chain.ainvoke({"page_content": document.page_content})
            questions_and_answers = self._parse_qa_result(result)
            metadata = dict(document.metadata)
            metadata["questions_and_answers"] = questions_and_answers
            transformed_documents.append(
                Document(page_content=document.page_content, metadata=metadata)
            )
        return transformed_documents

    @staticmethod
    def _parse_qa_result(result: str) -> List[dict]:
        """解析模型返回的 JSON 文本"""
        result = result.strip()
        if result.startswith("```json"):
            result = result.removeprefix("```json").removesuffix("```").strip()
        elif result.startswith("```"):
            result = result.removeprefix("```").removesuffix("```").strip()

        questions_and_answers = json.loads(result)
        if not isinstance(questions_and_answers, list):
            raise ValueError("模型返回的问答结果不是列表")
        return questions_and_answers


async def main():
    # 1.构建文档列表
    page_content = """机密文件 - 仅供内部使用
日期：2023年7月1日
主题：各种话题的更新和讨论
亲爱的团队，
希望这封邮件能找到你们一切安好。在这份文件中，我想向你们提供一些重要的更新，并讨论需要我们关注的各种话题。请将此处包含的信息视为高度机密。
安全和隐私措施
作为我们不断致力于确保客户数据安全和隐私的一部分，我们已在所有系统中实施了强有力的措施。我们要赞扬IT部门的John Doe（电子邮件：john.doe@example.com）在增强我们网络安全方面的勤奋工作。未来，我们提醒每个人严格遵守我们的数据保护政策和准则。此外，如果您发现任何潜在的安全风险或事件，请立即向我们专门的团队报告，联系邮箱为security@example.com。
人力资源更新和员工福利
最近，我们迎来了几位为各自部门做出重大贡献的新团队成员。我要表扬Jane Smith（社保号：049-45-5928）在客户服务方面的出色表现。Jane一直受到客户的积极反馈。此外，请记住我们的员工福利计划的开放报名期即将到来。如果您有任何问题或需要帮助，请联系我们的人力资源代表Michael Johnson（电话：418-492-3850，电子邮件：michael.johnson@example.com）。
营销倡议和活动
我们的营销团队一直在积极制定新策略，以提高品牌知名度并推动客户参与。我们要感谢Sarah Thompson（电话：415-555-1234）在管理我们的社交媒体平台方面的杰出努力。Sarah在过去一个月内成功将我们的关注者基数增加了20%。此外，请记住7月15日即将举行的产品发布活动。我们鼓励所有团队成员参加并支持我们公司的这一重要里程碑。
研发项目
在追求创新的过程中，我们的研发部门一直在为各种项目不懈努力。我要赞扬David Rodriguez（电子邮件：david.rodriguez@example.com）在项目负责人角色中的杰出工作。David对我们尖端技术的发展做出了重要贡献。此外，我们希望每个人在7月10日定期举行的研发头脑风暴会议上分享他们的想法和建议，以开展潜在的新项目。
请将此文档中的信息视为最机密，并确保不与未经授权的人员分享。如果您对讨论的话题有任何疑问或顾虑，请随时直接联系我。
感谢您的关注，让我们继续共同努力实现我们的目标。
此致，
Jason Fan
联合创始人兼首席执行官
Psychic
jason@psychic.dev"""
    documents = [Document(page_content=page_content)]

    # 2.构建问答转换器并转换
    qa_transformer = SimpleQATransformer(model="LongCat-Flash-Chat")
    transformed_documents = await qa_transformer.atransform_documents(documents)

    for qa in transformed_documents[0].metadata.get("questions_and_answers", []):
        print("问答数据：", qa)


if __name__ == "__main__":
    asyncio.run(main())
