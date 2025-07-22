from langchain_together import ChatTogether
import os
from dotenv import load_dotenv  
load_dotenv()

def get_togetherllm():
    return ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        api_key=os.getenv("TOGETHER_API_KEY"),
        temperature=0.3,
        max_tokens=2048,
        timeout=30,  
    )

def get_fast_llm():
    """Faster model for quick summaries"""
    return ChatTogether(
        model="meta-llama/Llama-3.2-3B-Instruct-Turbo", 
        api_key=os.getenv("TOGETHER_API_KEY"),
        temperature=0.3,
        max_tokens=1024,
        timeout=15,  
    )

def get_assemblyai_llm():
    return os.getenv("ASSEMBLY_API_KEY")  
