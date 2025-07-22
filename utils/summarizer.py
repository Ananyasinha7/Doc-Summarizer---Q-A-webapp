from langchain.chains.summarize import load_summarize_chain
from get_llm import get_togetherllm

def generate_summary(docs):
    llm=get_togetherllm()
    chain=load_summarize_chain(llm=llm, chain_type="map_reduce")
    result = chain.invoke({"input_documents":docs})
    
    
    if isinstance(result, dict) and 'output_text' in result:
        return result['output_text']
    elif hasattr(result, 'content'):
        return result.content
    else:
        return str(result)


