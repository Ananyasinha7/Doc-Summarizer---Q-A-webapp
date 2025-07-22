import os
from dotenv import load_dotenv
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
TOGETHER_API_HOST = os.getenv("TOGETHER_API_HOST")
#GROQ_API_KEY = os.getenv("GROQ_API_KEY")
