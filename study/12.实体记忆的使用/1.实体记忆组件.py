import dotenv
from langchain.chains.conversation.base import ConversationChain
from langchain.memory import ConversationEntityMemory
from langchain.memory.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()
llm=ChatOpenAI(model="LongCat-Flash-Chat",temperature=0)

chain=ConversationChain(
    llm=llm,
    prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
    memory=ConversationEntityMemory(llm=llm),
)

print(chain.invoke({"input":"你好 我是小明 我在学习LangChain"}))
print(chain.invoke({"input":"我最喜欢的编程语言是python"}))
print(chain.invoke({"input":"我住在上海"}))

res=chain.memory.entity_store.store
print(res)

