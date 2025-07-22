from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from get_llm import get_togetherllm

def get_qa_chain(vector_store):
    llm=get_togetherllm()
    prompt=ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers questions based on the provided context. \n\n{context}"),
        ("human","{input}")
    ])

    chain=create_stuff_documents_chain(llm=llm, prompt=prompt)
    retriever= vector_store.as_retriever()
    return create_retrieval_chain(retriever=retriever,combine_docs_chain=chain)

