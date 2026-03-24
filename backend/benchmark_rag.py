import os
# Force transformers to use PyTorch
os.environ["USE_TORCH"] = "1"
os.environ["USE_TF"] = "0"

import asyncio
import time
from rag_engine import RAGEngine
from local_llm_client import LocalLLMClient
from llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

# Evaluation Questions based on documents
TEST_QUESTIONS = [
    "What is the one-line summary of Indecimal?",
    "What are the three package pricing levels per sqft?",
    "What does Indecimal promise to build instead of just contracts?",
    "What are the specification wallets for flooring in the Premier package?",
    "What is the booking amount for the design phase?",
    "What is the 'Premier' package price per sqft including GST?",
    "What are the internal reference details for the Audience of the documents?",
    "How does Indecimal handle project tracking from inquiry to handover?",
    "What is the audience for the Package Comparison document?",
    "What is the last updated date of the documents?"
]

async def run_benchmark():
    print("Starting RAG Benchmarking...")
    
    # Initialize RAG Engine
    rag_engine = RAGEngine()
    rag_engine.initialize()
    
    # Initialize Clients
    openrouter_client = LLMClient()
    local_llm_client = LocalLLMClient() # Phi-2 is lightweight and effective for testing
    
    results = []
    
    for q_idx, question in enumerate(TEST_QUESTIONS):
        print(f"\n[{q_idx + 1}/{len(TEST_QUESTIONS)}] Question: {question}")
        
        # 1. Test OpenRouter
        print("Testing OpenRouter...")
        start_time = time.time()
        or_result = await rag_engine.answer_question(question)
        or_latency = time.time() - start_time
        
        # 2. Test Local LLM
        print("Testing Local LLM...")
        # Temporarily swap LLM client for benchmarking
        original_client = rag_engine.llm_client
        rag_engine.llm_client = local_llm_client
        
        start_time = time.time()
        local_result = await rag_engine.answer_question(question)
        local_latency = time.time() - start_time
        
        # Restore client
        rag_engine.llm_client = original_client
        
        results.append({
            "question": question,
            "openrouter": {
                "answer": or_result["response"],
                "latency": or_latency,
                "chunks": or_result["chunks"]
            },
            "local_llm": {
                "answer": local_result["response"],
                "latency": local_latency
            }
        })
        
    # Output Summary Table
    print("\n" + "="*80)
    print(f"{'Question':<40} | {'OR Latency (s)':<15} | {'Local Latency (s)':<15}")
    print("-" * 80)
    
    for res in results:
        print(f"{res['question'][:37]+'...':<40} | {res['openrouter']['latency']:<15.2f} | {res['local_llm']['latency']:<15.2f}")
    
    # Save Detailed Report to Markdown
    with open("BENCHMARK_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# RAG Benchmark Report: OpenRouter vs Local LLM (TinyLlama)\n\n")
        f.write("## Summary Statistics\n")
        avg_or_lat = sum(r['openrouter']['latency'] for r in results) / len(results)
        avg_local_lat = sum(r['local_llm']['latency'] for r in results) / len(results)
        f.write(f"- **Avg OpenRouter Latency:** {avg_or_lat:.2f}s\n")
        f.write(f"- **Avg Local LLM Latency:** {avg_local_lat:.2f}s\n\n")
        
        f.write("## Detailed Comparison\n\n")
        for res in results:
            f.write(f"### {res['question']}\n")
            f.write(f"**OpenRouter Answer (Latency: {res['openrouter']['latency']:.2f}s):**\n{res['openrouter']['answer']}\n\n")
            f.write(f"**Local LLM Answer (Latency: {res['local_llm']['latency']:.2f}s):**\n{res['local_llm']['answer']}\n\n")
            f.write(f"**Retrieved Chunks Used:** {len(res['openrouter']['chunks'])}\n\n")
            f.write("---\n\n")
            
    print("\nBenchmark completed. Report saved to BENCHMARK_REPORT.md")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
