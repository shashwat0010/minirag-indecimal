import os
from dotenv import load_dotenv

# Load .env locally
load_dotenv()

def get_config(key: str, default: str = None) -> str:
    """
    Retrieves a configuration value from Streamlit Secrets (if available) 
    or from Environment Variables.
    """
    # 1. Try Streamlit Secrets (Streamlit Cloud)
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
        
    # 2. Try Environment Variables (Local, Render, etc.)
    return os.getenv(key, default)
