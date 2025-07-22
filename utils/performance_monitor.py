import time
import streamlit as st
from functools import wraps

def monitor_performance(func):
    """Decorator to monitor function performance"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = end_time - start_time
            
            st.success(f" {func.__name__} completed in {duration:.1f} seconds")
            return result
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            st.error(f"{func.__name__} failed after {duration:.1f} seconds: {str(e)}")
            raise
            
    return wrapper

@monitor_performance
def timed_summary(summary_func, docs):
    """Wrapper to time summary generation"""
    return summary_func(docs)

def show_performance_tips():
    """Display performance optimization tips"""
    with st.expander(" Performance Tips"):
        st.write("""
        **Summary Speed Options:**
        
        - ** Quick Summary**: ~30 seconds
          - Processes first 3 document sections only
          - Good for getting main ideas quickly
          - Best for documents > 10 pages
        
        - ** Full Summary**: 2-3 minutes  
          - Processes entire document
          - More comprehensive and detailed
          - Uses optimized chunking strategy
        
        **Speed Factors:**
        - Document size (larger = slower)
        - API response time (~2-5 seconds per chunk)
        - Number of chunks created
        - Network connection quality
        
        **Tips for Faster Processing:**
        - Use Quick Summary first to get overview
        - Split very large documents into sections
        - Ensure stable internet connection
        """)
