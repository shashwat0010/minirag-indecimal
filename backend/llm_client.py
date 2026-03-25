import os
import httpx
import json
from typing import List, Dict
from config import get_config

class LLMClient:
    def __init__(self, api_key: str = None, model: str = None):
        # Fallback chain: provided arg -> config/env -> default
        self.api_key = api_key or get_config("OPENROUTER_API_KEY")
        self.model = model or get_config("MODEL_NAME", "meta-llama/llama-3-8b-instruct")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using Llama-3 via OpenRouter."""
        
        if not self.api_key:
            return f"Error: OPENROUTER_API_KEY is missing. Context found: {context[:100]}..."

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000", # OpenRouter requires a valid-ish referer
            "X-Title": "Mini RAG Assistant"
        }

        # Llama 3 works best when rules are clear and bulleted
        system_prompt = (
            "You are a helpful assistant that answers questions based ONLY on the provided context. "
            "If the answer isn't in the context, say 'Not specified in the provided documents.' "
            "Do not use outside knowledge. Do not mention the context itself."
        )

        # Structure the user message clearly for Llama 3
        user_content = f"CONTEXT:\n{context}\n\nUSER QUESTION: {prompt}"

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.1,  # Llama 3 can get 'creative' at 0.0; 0.1 is safer
            "top_p": 0.9,
            "max_tokens": 512
        }

        async with httpx.AsyncClient() as client:
            try:
                # Increased timeout as OpenRouter routing to Llama providers can take time
                response = await client.post(
                    self.url, 
                    headers=headers, 
                    content=json.dumps(data), 
                    timeout=30.0
                )
                
                # Check for HTTP errors (401, 404, 429, etc)
                if response.status_code != 200:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', 'Unknown Error')
                    return f"OpenRouter Error ({response.status_code}): {error_msg}"

                result = response.json()
                return result["choices"][0]["message"]["content"]

            except httpx.TimeoutException:
                return "Error: The request to OpenRouter timed out."
            except Exception as e:
                return f"LLM Client Error: {str(e)}"