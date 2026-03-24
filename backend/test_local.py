import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"Testing model: {model_id}")

try:
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, device_map="cpu")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    print("Success loading model")
    res = pipe("Hello, how are you?", max_new_tokens=10)
    print(res)
except Exception as e:
    print(f"Error: {e}")
