from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import uuid

def get_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")
    
   
    collection_name = f"doc_collection_{str(uuid.uuid4()).replace('-', '_')}"
    
    return FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=None 
    )

