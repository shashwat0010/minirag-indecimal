import os
from typing import Dict, List

from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm_client import LLMClient


from config import get_config


class RAGEngine:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # Try to find the data directory relative to this file
            base_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(base_dir, "data")
            
        self.doc_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        self.llm_client = LLMClient()
        self.local_llm_client = None  # Lazy‑loaded
        self.data_dir = data_dir

    def initialize(self):
        """Initializes the RAG engine by processing all PDFs in the data directory."""
        print(f">>> RAG ENGINE: Initializing from directory '{self.data_dir}'...")
        if os.path.exists(self.data_dir) and os.path.isdir(self.data_dir):
            chunks = self.doc_processor.process_directory(self.data_dir)
            if chunks:
                print(f">>> RAG ENGINE: Found {len(chunks)} chunks across documents. Adding to vector store...")
                self.vector_store.add_documents(chunks)
                print(">>> RAG ENGINE: Vector store updated.")
            else:
                print(">>> RAG ENGINE: No documents found in data directory.")
        else:
            print(f">>> RAG ENGINE ERROR: Data directory '{self.data_dir}' does not exist or is not a directory.")

    async def answer_question(self, question: str) -> dict:
        """Retrieves context and generates an answer."""
        # Handle simple greetings without RAG
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon"]
        if question.lower().strip() in greetings:
            return {
                "response": "Hello! I am your Indecimal RAG Assistant. How can I help you today?",
                "chunks": []
            }

        print(f">>> RAG ENGINE: Searching for context for question: '{question}'")
        relevant_chunks = self.vector_store.search(question)
        print(f">>> RAG ENGINE: Found {len(relevant_chunks)} relevant chunks.")
        
        context = "\n\n".join([chunk["content"] for chunk in relevant_chunks]) if relevant_chunks else "No relevant context found."
        
        try:
            print(">>> RAG ENGINE: Requesting answer from Cloud LLM...")
            # Changed: Only pass the raw question and context, llm_client will handle formatting
            response = await self.llm_client.generate_response(
                prompt=question,
                context=context,
            )
            return {
                "response": response,
                "chunks": relevant_chunks
            }
        except Exception as e:
            print(f">>> RAG ENGINE: Cloud LLM failed: {e}.")
            
            # Disable local fallback on Render to avoid OOM
            if get_config("ENVIRONMENT") == "production":
                print(">>> RAG ENGINE: Production mode detected. Skipping local fallback to save memory.")
                return {
                    "response": "The cloud LLM service is currently unavailable. Local fallback is disabled in production to save memory.",
                    "chunks": relevant_chunks,
                }
            
            print(">>> RAG ENGINE: Falling back to local model...")
            if self.local_llm_client is None:
                print(">>> RAG ENGINE: Loading local model for the first time...")
                from local_llm_client import LocalLLMClient
                self.local_llm_client = LocalLLMClient()
            
            response = await self.local_llm_client.generate_response(prompt=prompt, context=context)
            
            return {
                "response": response,
                "chunks": relevant_chunks
            }
