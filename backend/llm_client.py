import os
import httpx
from typing import List, Dict

class LLMClient:
    def __init__(self, api_key: str = None, model: str = None):
        # Try to get API key from streamlit secrets first, then environment variable
        try:
            import streamlit as st
            self.api_key = api_key or st.secrets.get("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        except Exception:
            self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
            
        self.model = model or os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using the LLM through OpenRouter."""
        if not self.api_key:
            return f"No OPENROUTER_API_KEY found. Here's the retrieved context:\n\n{context}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/shashwat0010/minirag-indecimal", # Optional, for OpenRouter analytics
            "X-Title": "Mini RAG Assistant" # Optional
        }
        
        system_prompt = (
            "You are a helpful and precise RAG assistant. "
            "Answer the user's question ONLY using the provided context. "
            "If the answer is not in the context, say: 'Not specified in the provided documents.' "
            "Structure your answer clearly with bullet points if it helps readability."
        )
        
        # Cleaned up: Use only the user question here, since context is in system or explicitly separated
        user_content = f"Context: {context}\n\nQuestion: {prompt}"
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1 # Low temperature for factual RAG
        }
        
        async with httpx.AsyncClient() as client:
            try:
                print(f">>> LLM CLIENT: Requesting {self.model} via OpenRouter...")
                response = await client.post(self.url, headers=headers, json=data, timeout=45.0)
                
                if response.status_code != 200:
                    print(f">>> LLM CLIENT ERROR: {response.status_code} - {response.text}")
                
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                print(f">>> LLM CLIENT HTTP ERROR: {e}")
                raise
            except Exception as e:
                print(f">>> LLM CLIENT ERROR: {e}")
                raise
