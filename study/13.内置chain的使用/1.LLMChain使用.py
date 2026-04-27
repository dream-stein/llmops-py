import dotenv
from langchain.chains.base import Chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
prompt=ChatPromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
llm=ChatOpenAI(model="LongCat-Flash-Chat")

chain=LLMChain(prompt=prompt,llm=llm)

print(chain("程序员"))
print(chain.invoke({"subject":"程序员"}))