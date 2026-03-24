import os
import httpx
from typing import List, Dict

class LLMClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
        self.url = "https://openrouter.ai/api/v1/chat/completions"

    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using the LLM through OpenRouter."""
        if not self.api_key:
            return f"No OPENROUTER_API_KEY found. Here's the retrieved context:\n\n{context}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = (
            "You are a RAG assistant. "
            "Answer the question ONLY using the provided context. "
            "Do NOT use any external knowledge. "
            "Do NOT make assumptions or add extra information. "
            "Structure your answer using clear bullet points where appropriate for readability. "
            "If the answer is not explicitly present in the context, say: "
            "\"Not specified in the provided documents.\""
        )
        
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": full_prompt}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
