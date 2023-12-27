import time
from rich.console import Console

import os
from getpass import getpass

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass(prompt='OpenAI API Key: ')

from langchain.chat_models import ChatOpenAI

openai = ChatOpenAI(temperature=0, model='gpt-4-1106-preview')

console = Console()

from langchain.prompts import PromptTemplate
prompt = PromptTemplate.from_template(template='請用{lang}回答下列問題，問題：\n{question}\n')

from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from langchain.document_loaders.csv_loader import CSVLoader
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

# from langchain.text_splitter import CharacterTextSplitter
# text_splitter = CharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap  = 50,
#     length_function = len,
#     add_start_index = True,
# )
# documents = text_splitter.create_documents(documents)
    
from langchain.embeddings import OpenAIEmbeddings
# openai_embeddings = OpenAIEmbeddings()

# embedded_docs = openai_embeddings.embed_documents
# embedded_query = openai_embeddings.embed_query("What was the name mentioned in the conversation?")


import chromadb
from chromadb.utils import embedding_functions

console.print('向量化資料庫...')
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=os.environ["OPENAI_API_KEY"], # Replace with your own OpenAI API key
#     model_name="gpt-4-1106-preview"
# )
# client = chromadb.PersistentClient(path="./chromadb/")

# collection = client.get_or_create_collection(name="plant", embedding_function=openai_ef)
# # collection = client.get_or_create_collection("plant")
# collection.add(
#     ids=[str(i) for i in range(0, len(documents))],
#     documents=documents
# )
# results = collection.query(
#     query_texts=["查詢會議記錄"],
#     n_results=10
# )
# results = collection.query(
#     query_texts=dataset["question"][:10],
#     n_results=1)

# from langchain.vectorstores import Chroma
# from chromadb.errors import InvalidDimensionException
# try:
#     db = Chroma.from_documents(documents, embedding=OpenAIEmbeddings())
# except InvalidDimensionException:
#     Chroma().delete_collection()
#     db = Chroma.from_documents(documents, embedding=OpenAIEmbeddings())

# query = "What did the president say about Ketanji Brown Jackson"
# docs = db.similarity_search(query)

def query(question, rag_mode='RAG OFF', llm_mode='OPENAI'):
    # if rag_mode == RAG_MODE['rag_only']:
    #     chain = db.similarity_search(query)
    chain = prompt.partial(lang='中文') | openai |StrOutputParser()
    answer = chain.invoke({'question': question})
    # console.log(type(answer))
    return answer

def main():
    query(input())

if __name__ == '__main__':
    main()