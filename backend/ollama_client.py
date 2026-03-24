import ollama
from typing import List, Dict

class OllamaClient:
    def __init__(self, model_id: str = "tinyllama"):
        self.model_id = model_id
        print(f"Initializing Ollama client with model: {model_id}...")
        
    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using Ollama."""
        
        system_instruction = (
            "You are a RAG assistant. Answer the question ONLY using the provided context. "
            "Do NOT use external knowledge. Structure your answer in bullet points. "
            "If the answer is not in the context, say 'Not specified in the provided documents.'"
        )
        
        full_prompt = f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        
        try:
            response = ollama.generate(
                model=self.model_id,
                prompt=full_prompt,
                system=system_instruction,
                options={
                    "temperature": 0.1,
                    "num_predict": 256
                }
            )
            return response['response'].strip()
        except Exception as e:
            return f"Ollama Error: {str(e)}"
