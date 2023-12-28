# from langchain.text_splitter import CharacterTextSplitter
# text_splitter = CharacterTextSplitter(
#     chunk_size = 500,
#     chunk_overlap  = 50,
#     length_function = len,
#     add_start_index = True,
# )
# documents = text_splitter.create_documents(documents)

# 🌿🌿🌿🌿🌿

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

try:
  chroma_db = Chroma.from_documents(documents, embedding=OpenAIEmbeddings())
except InvalidDimensionException:
  Chroma().delete_collection()
  chroma_db = Chroma.from_documents(documents, embedding=OpenAIEmbeddings())

retriever = chroma_db.as_retriever(max_tokens_limit=100)

retrieved_docs = retriever.invoke(
    "What did the president say about Ketanji Brown Jackson?"
)
print(retrieved_docs[0].page_content)

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

template = """Answer the question based only on the following context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI()


def format_docs(docs):
    return "\n\n".join([d.page_content for d in docs])


chain ={"context": retriever | format_docs, "question": RunnablePassthrough()} | prompt | model | StrOutputParser()

chain.invoke("What did the president say about technology?")




    
from langchain.embeddings import OpenAIEmbeddings
# openai_embeddings = OpenAIEmbeddings()

# embedded_docs = openai_embeddings.embed_documents
# embedded_query = openai_embeddings.embed_query("What was the name mentioned in the conversation?")


import chromadb
from chromadb.utils import embedding_functions

console.print('載入向量資料庫...')
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

