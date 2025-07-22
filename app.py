import os
import tempfile
import streamlit as st
#import whisper
from utils.document_loader import load_and_split, extract_preview
from utils.vector_store import get_vector_store
from utils.summarizer import generate_summary
from utils.quick_summarizer import generate_quick_summary, generate_full_summary
from utils.performance_monitor import timed_summary, show_performance_tips
from utils.qa_chain import get_qa_chain
# from utils.voice_input import transcribe_audio  
from speech.tts import speak

st.set_page_config(page_title="Document Summarizer & Q&A", layout="wide")
st.title("Document Summarizer & Q&A")




uploaded_file=st.file_uploader("Upload a document (PDF, TXT, DOCX)", type=["pdf", "txt", "docx"])
if uploaded_file:
    st.subheader("Document Preview")
    st.text_area("Preview", extract_preview(uploaded_file),height=200)

    st.subheader("Generate Summary")
    
    show_performance_tips()
    
    summary_type = st.radio(
        "Choose summary type:",
        ["Quick Summary (30 seconds)", "Full Summary (2-3 minutes)"],
        help="Quick summary processes first few sections only. Full summary processes entire document."
    )
    
    
    summary_output = st.radio(
        "Summary output format:",
        ["Text Only", "Audio Only", "Text + Audio"],
        help="Choose how to receive the summary",
        key="summary_output"
    )
    
    if st.button("Generate Summary"):
        docs = load_and_split(uploaded_file)
        
        st.session_state['docs'] = docs
        st.session_state['vectordb'] = get_vector_store(docs)
        
        if "Quick" in summary_type:
            summary = timed_summary(generate_quick_summary, docs)
        else:
            summary = timed_summary(generate_full_summary, docs)
        
        st.subheader("Summary")
        
        
        if "Text" in summary_output:
            st.text_area("Summary", summary, height=200, key="summary_text")
            
        
        if "Audio" in summary_output:
            st.write("Playing summary audio...")
            speak(summary)
            
        if summary_output == "Audio Only":
            st.info("Summary played as audio. Enable 'Text + Audio' to see the written summary too.")

    st.subheader("Ask Questions from the Document")
    
    
    if 'docs' not in st.session_state:
        if st.button("Process Document for Q&A"):
            with st.spinner("Processing document for questions..."):
                st.session_state['docs'] = load_and_split(uploaded_file)
                st.session_state['vectordb'] = get_vector_store(st.session_state['docs'])
            st.success("Document processed! You can now ask questions.")
    
   
    if 'vectordb' in st.session_state:
       
        st.subheader("Output Settings")
        output_format = st.radio(
            "Choose output format:",
            ["Text Only", "Audio Only", "Text + Audio"],
            help="Select how you want to receive answers"
        )
        
       
        mode = "Text Input"  
        qa_chain = get_qa_chain(st.session_state['vectordb'])

        question = st.text_input("Enter your question here")
        if st.button("Ask"):
            if question.strip():
                with st.spinner("Getting answer..."):
                    answer = qa_chain.invoke({"input": question})
                    
                    if isinstance(answer, dict):
                        answer_text = answer.get('answer', str(answer))
                    else:
                        answer_text = str(answer)
                
                
                if "Text" in output_format:
                    st.write("**Answer:**", answer_text)
                
                if "Audio" in output_format:
                    st.write("Playing audio response...")
                    speak(answer_text)
                    
                if output_format == "Audio Only":
                    st.info("Audio response played. Enable 'Text + Audio' to see the written answer too.")
            else:
                st.warning("Please enter a question first.")
        
        # Voice Input Section - Commented Out will be developed later
        """
        if mode == "Voice Input":
            st.subheader("Speak Your Question")
            
            transcript = transcribe_audio()

            if transcript:
                st.success("Transcription complete!")
                st.write("**You asked:**", transcript)
                with st.spinner("Getting answer..."):
                    answer = qa_chain.invoke({"input": transcript})

                    if isinstance(answer, dict):
                        answer_text = answer.get('answer', str(answer))
                    else:
                        answer_text = str(answer)

                if "Text" in output_format:
                    st.write("**Answer:**", answer_text)
                
                if "Audio" in output_format:
                    st.write("Playing audio response...")
                    speak(answer_text)
                    
                if output_format == "Audio Only":
                    st.info("Audio response played. Enable 'Text + Audio' to see the written answer too.")
        """
    else:
        st.info("Please process the document first (either generate a summary or click 'Process Document for Q&A')")


