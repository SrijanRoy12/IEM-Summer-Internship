import os
from dotenv import load_dotenv

load_dotenv()

def gemini_llm(prompt, model=None):
    # Dummy LLM function to keep the app running without google.generativeai
    return "[LLM functionality is disabled. Please install google-generativeai to enable Gemini integration.]"
