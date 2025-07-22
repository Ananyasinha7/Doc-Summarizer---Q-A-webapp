import streamlit as st
from get_llm import get_togetherllm, get_fast_llm

def generate_quick_summary(docs):
    """Generate a quick summary using first few chunks"""
    llm = get_fast_llm()
    
   
    quick_docs = docs[:2] if len(docs) > 2 else docs

    text_parts = []
    total_chars = 0
    max_chars = 3000  
    
    for doc in quick_docs:
        if total_chars + len(doc.page_content) <= max_chars:
            text_parts.append(doc.page_content)
            total_chars += len(doc.page_content)
        else:
           
            remaining_chars = max_chars - total_chars
            if remaining_chars > 100: 
                text_parts.append(doc.page_content[:remaining_chars] + "...")
            break
    
    text = "\n\n".join(text_parts)
    
    prompt = f"""Summarize this document in 3-4 sentences:

{text}

Summary:"""
    
    try:
        response = llm.invoke(prompt)
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    except Exception as e:
        st.error(f"Error generating quick summary: {e}")
        return "Error generating summary. Please try again."

def generate_full_summary(docs):
    """Generate a comprehensive summary using all chunks"""
    llm = get_togetherllm()
    
    text = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""
    Provide a comprehensive summary of the following document:
    
    {text}
    
    Please provide a detailed summary covering all key points:
    """
    
    try:
        response = llm.invoke(prompt)
       
        if hasattr(response, 'content'):
            return response.content
        else:
            return str(response)
    except Exception as e:
        st.error(f"Error generating full summary: {e}")
        return "Error generating summary. Please try again."