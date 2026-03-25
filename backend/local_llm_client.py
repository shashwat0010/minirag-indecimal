import os
from typing import List, Dict

class LocalLLMClient:
    def __init__(self, model_id: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
        self.model_id = model_id
        print(f"Loading local model: {model_id}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            torch_dtype=torch.float32, 
            device_map="cpu",
            trust_remote_code=True
        )
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=256,
            temperature=0.01, # Transformers requires > 0 for temperature
            do_sample=False, # Disable sampling for greedy decoding (factual)
            repetition_penalty=1.2
        )
        print("Local model loaded successfully.")

    async def generate_response(self, prompt: str, context: str) -> str:
        """Generates a response using the local LLM."""
        
        system_instruction = (
            "You are a RAG assistant. Answer the question ONLY using the provided context. "
            "Do NOT use external knowledge. Structure your answer in bullet points. "
            "If the answer is not in the context, say 'Not specified in the provided documents.'"
        )
        
        formatted_prompt = f"System: {system_instruction}\n\nContext: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        
        outputs = self.pipe(formatted_prompt, do_sample=True)
        response = outputs[0]["generated_text"]
        
        # Extract only the answer part after "Answer:"
        if "Answer:" in response:
            return response.split("Answer:")[-1].strip()
        return response.strip()
