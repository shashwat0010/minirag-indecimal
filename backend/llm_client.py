import os
import httpx
from typing import List, Dict

from config import get_config

class LLMClient:
    def __init__(self, api_key: str = None, model: str = None):
        # Centralized config: st.secrets -> os.getenv
        self.api_key = api_key or get_config("OPENROUTER_API_KEY")
        self.model = model or get_config("MODEL_NAME", "mistralai/mistral-7b-instruct:free")
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
            "You are a strict RAG assistant. "
            "Your task is to answer the user's question using ONLY the provided context. "
            "Rules you MUST follow:\n"
            "1. Base your entire answer on the provided context. Do NOT use external knowledge.\n"
            "2. If the answer is not contained within the context, respond EXACTLY with: 'Not specified in the provided documents.'\n"
            "3. Do not mention the context or the documents in your response (e.g., don't say 'Based on the context...'). Just provide the answer.\n"
            "4. Be concise and factual.\n"
            "5. If the question is a general greeting like 'hi' or 'hello', you can respond briefly but then remind the user you are here to answer questions about the documents."
        )
        
        # Cleaned up: Use only the user question here, since context is in system or explicitly separated
        user_content = f"Context:\n{context}\n\nQuestion: {prompt}"
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.0, # Zero temperature for absolute factual grounding
            "top_p": 1.0
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
