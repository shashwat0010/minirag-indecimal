import os
from google import genai
from google.genai import types
from config import get_config

class LLMClient:
    def __init__(self, api_key: str = None, model: str = None):
        # 1. Load config
        self.api_key = api_key or get_config("GEMINI_API_KEY")
        # Defaulting to gemini-2.0-flash (fast and smart)
        self.model_id = model or get_config("MODEL_NAME", "gemini-2.0-flash")
        
        # 2. Initialize the official Google GenAI Client
        # It handles the base URL and headers for you.
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using the Gemini SDK."""
        
        if not self.api_key or not self.client:
            return f"No GEMINI_API_KEY found. Here's the retrieved context:\n\n{context}"

        # 3. System Instruction (Defining the 'Persona')
        system_prompt = (
            "You are a strict RAG assistant. "
            "Your task is to answer the user's question using ONLY the provided context. "
            "Rules:\n"
            "1. Base your answer ONLY on the context. No external knowledge.\n"
            "2. If the answer is missing, say EXACTLY: 'Not specified in the provided documents.'\n"
            "3. Do not mention 'the context' or 'the documents'. Just answer.\n"
            "4. Be concise.\n"
            "5. Brief greetings are okay, then remind them of your purpose."
        )

        # 4. User Content
        user_content = f"Context:\n{context}\n\nQuestion: {prompt}"

        # 5. Configuration (Temperature 0 for RAG accuracy)
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,
            top_p=1.0,
            max_output_tokens=1000
        )

        try:
            print(f">>> GEMINI CLIENT: Requesting {self.model_id}...")
            
            # Using the asynchronous 'aio' property of the client
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=user_content,
                config=config
            )
            
            return response.text

        except Exception as e:
            print(f">>> GEMINI CLIENT ERROR: {e}")
            # Fallback/Safety
            if "finish_reason" in str(e):
                return "The model could not generate a response (safety filter or limit)."
            raise e