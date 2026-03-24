import os
os.environ["USE_TORCH"] = "1"
os.environ["USE_TF"] = "0"

import asyncio
import time
from local_llm_client import LocalLLMClient
from llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

async def test_clients():
    print("Initializing Local LLM...")
    local_client = LocalLLMClient()
    
    print("Initializing OpenRouter Client...")
    or_client = LLMClient()
    
    context = "Indecimal is a company that builds products, not just contracts."
    question = "What does Indecimal build?"
    
    print("\nTesting Local LLM...")
    start = time.time()
    local_resp = await local_client.generate_response(question, context)
    print(f"Local Response: {local_resp}")
    print(f"Local Latency: {time.time() - start:.2f}s")
    
    print("\nTesting OpenRouter...")
    start = time.time()
    or_resp = await or_client.generate_response(question, context)
    print(f"OR Response: {or_resp}")
    print(f"OR Latency: {time.time() - start:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_clients())
