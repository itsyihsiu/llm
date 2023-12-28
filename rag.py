from params import *
from rich.console import Console
import os
from getpass import getpass
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.document_loaders.csv_loader import CSVLoader

console = Console()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass(prompt='OpenAI API Key: ')

llm_openai = ChatOpenAI(temperature=0, model='gpt-4-1106-preview')

llm_llama2 = llm_openai

prompt = PromptTemplate.from_template(template='請用{lang}回答下列問題，問題：\n{question}\n')
prompt = prompt.partial(lang='中文')

loaders = [
    CSVLoader(file_path = './docs/pests_and_diseases.csv', encoding = 'UTF-16', csv_args={
        'fieldnames': ['圖片', '病蟲害名稱', '危害作物/防治對象', '危害徵狀']
    }),
    CSVLoader(file_path = './docs/product.csv', encoding = 'UTF-16', csv_args={
        'fieldnames': ['產品', '植物', '病蟲害']
    }),
]

documents = []

for loader in loaders:
    documents.extend(loader.load())

def query(question, rag_mode='RAG OFF', llm_mode='OPENAI'):

    llm = llm_openai if llm_mode == LLM_MODE['openai'] else llm_llama2

    if rag_mode == RAG_MODE['rag_only']:
        chain = prompt | llm | StrOutputParser()
    elif rag_mode == RAG_MODE['rag_on']:
        chain = prompt | llm | StrOutputParser()
    else:
        chain = prompt | llm | StrOutputParser()
        
    answer = chain.invoke({'question': question})
    
    return answer
