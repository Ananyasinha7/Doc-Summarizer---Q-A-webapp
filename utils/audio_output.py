import streamlit as st
from speech.tts import speak

def display_output_with_controls(content, output_format, content_type="Answer"):
    """
    Display content based on output format selection
    
    Args:
        content (str): The content to display/speak
        output_format (str): Selected output format
        content_type (str): Type of content (Answer, Summary, etc.)
    """
    
   
    if "Text" in output_format:
        st.write(f"**{content_type}:**", content)
    
   
    if "Audio" in output_format:
        col1, col2 = st.columns([4, 1])
        
        with col1:
            if "Text" not in output_format: 
                st.write(f"**{content_type} (Audio):**")
                st.info("Audio will play when you click the button below.")
        
        with col2:
            if st.button(f" Play", key=f"play_{content_type}"):
                speak(content)
        
       
        if "Audio Only" in output_format:
            speak(content)

def show_output_format_help():
    """Display helpful information about output formats"""
    with st.expander("Output Format Guide", expanded=False):
        st.write("""
        **Text Only**: Display answers/summaries as text on screen
        - Good for reading, copying text, quiet environments
        
        ** Audio Only**: Play answers/summaries as speech
        - Good for hands-free operation, multitasking
        - No text displayed
                 
        ** Text + Audio**: Both text display and audio playback
        - Best of both worlds - read along while listening
        
        **Note**: Audio uses your system's text-to-speech engine.
        """)